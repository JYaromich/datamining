import typing
import requests
import bs4
from urllib.parse import urljoin
import datetime as dt
from database.database import Database


class GbBlogParse:
    def __init__(self, start_url, db):
        self.start_url = start_url
        self.tasks = []
        self.done_urls = set()
        self.db = db

    def _get_task(self, url, callback: typing.Callable) -> typing.Callable:
        def task():
            soup = self._get_soup(url)
            return callback(url, soup)

        if url not in self.done_urls:
            self.done_urls.add(url)
            return task

        return lambda: None

    def _get_response(self, url, *args, **kwargs) -> requests.Response:
        return requests.get(url=url, *args, **kwargs)

    def _get_soup(self, url) -> bs4.BeautifulSoup:
        return bs4.BeautifulSoup(self._get_response(url).text, 'lxml')

    def _parse_feed(self, url, soup):
        pag_ul = soup.find('ul', attrs={'class': 'gb__pagination'})
        pag_urls = set(
            urljoin(url, pag_a.attrs.get('href')) for pag_a in pag_ul.find_all('a') if pag_a.attrs.get('href'))

        for pag_url in pag_urls:
            self.tasks.append(self._get_task(pag_url, self._parse_feed))

        post_urls = [urljoin(url, post.attrs.get('href')) for post in
                     soup.find_all('a', attrs={'class': 'post-item__title'}) if post.attrs.get('href')]

        for post_url in post_urls:
            self.tasks.append((self._get_task(post_url, self._parse_post)))

    def __get_comments_parse_post(self, soup):
        if not int(soup.find('comments').attrs.get('total-comments-count')):
            return list()

        comment_id = int(soup.find('comments').attrs.get('commentable-id'))
        URL_COMENT_API = 'https://gb.ru/api/v2/comments'
        params = {"commentable_type": 'Post', "commentable_id": comment_id}
        response_list = self._get_response(URL_COMENT_API, params=params).json()

        def _get_comment_with_children(response_list:list):
            result = []
            for response in response_list:
                if not response['comment']['children']:
                    result.append({
                        'id': int(response['comment']['id']),
                        'parent_id': int(parent) if (parent:= response['comment']['parent_id']) else None,
                        'author': response['comment']['user']['full_name'],
                        'text': response['comment']['body']
                    })
                else:
                    result.extend(_get_comment_with_children(response['comment']['children']))

            return result
        return _get_comment_with_children(response_list)

    def _parse_post(self, url, soup):
        data = {
            "post_data": {
                "url": url,
                'title': soup.find('h1', attrs={'class': 'blogpost-title'}).text,
                'first_image_url': soup.find('img').attrs.get('src'),
                'date': dt.datetime.fromisoformat(
                    soup.find('div', attrs={'class': 'blogpost-date-views'}).find('time').attrs.get('datetime')),
            },
            'writer': {
                "url": urljoin(url, soup.find('div', attrs={"itemprop": "author"}).parent.attrs.get('href')),
                "name": soup.find('div', attrs={"itemprop": "author"}).text
            },

            'tags': [{'url': urljoin(url, tag.attrs.get('href')), 'name': tag.text} for tag in
                     soup.find_all('a', attrs={"class": "small"})],
            'comment': self.__get_comments_parse_post(soup)
        }
        return data

    def run(self):
        self.tasks.append(self._get_task(self.start_url, self._parse_feed))
        for task in self.tasks:
            task_result = task()
            if task_result:
                self._save(task_result)

    def _save(self, data):
        self.db.create_post(data)

if __name__ == '__main__':
    db = Database('sqlite:///db_blog.db')
    parser = GbBlogParse('https://gb.ru/posts', db)
    parser.run()
