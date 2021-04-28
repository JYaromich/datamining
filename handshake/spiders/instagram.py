import json
from urllib.parse import urlencode

import scrapy

from handshake.items import FollowersItem, FollowingItem


class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['www.instagram.com']
    start_urls = ['https://www.instagram.com/']
    _login_url = 'accounts/login/ajax/'
    _follower_url = 'followers/'
    _following_url = 'following/'


    def __init__(self, login, password, usernames, *args, **kwargs):
        self.login = login
        self.password = password
        self.usernames = usernames
        self.token = dict()
        super().__init__(*args, **kwargs)

    @staticmethod
    def js_data_extract(response):
        script = response.xpath('//body/script[contains(text(), "window._sharedData =" )]/text()').extract_first()
        return json.loads(script.replace('window._sharedData = ', '')[:-1])

    def parse(self, response, **kwargs):
        try:
            js_data = self.js_data_extract(response)
            self.token = {'X-CSRFToken': js_data['config']['csrf_token']}
            yield scrapy.FormRequest(
                response.urljoin(self._login_url),
                method='POST',
                callback=self.parse,
                formdata={
                    'username': self.login,
                    'enc_password': self.password
                },
                headers=self.token)
        except AttributeError:
            if response.json()['authenticated']:
                for username in self.usernames:
                    yield response.follow(
                        f'https://www.instagram.com/{username}/',
                        callback=self.username_parse,
                        # cb_kwargs={'followers': list(), 'following': list()}
                        meta={'account_name': username}
                    )

    def username_parse(self, response):
        pagination_url = PaginationURL(response)
        yield response.follow(
            url=pagination_url.get_followers_url(first_entry=True),
            callback=self.followers_parse,
            # cb_kwargs={'followers': followers},
            meta={
                'pagination_url': pagination_url,
                'account_name': response.meta['account_name']
            }
        )
        yield response.follow(
            url=pagination_url.get_following_url(first_entry=True),
            callback=self.following_parse,
            # cb_kwargs={'following': following},
            meta={
                'pagination_url': pagination_url,
                'account_name': response.meta['account_name']
            }
        )

    @staticmethod
    def pagination_parse(response, func_pagination_url, callback, item_class):
        data = response.json()
        pagination_container = data['data']['user']['edge_followed_by'] if data['data']['user'].get(
            'edge_followed_by') else data['data']['user']['edge_follow']
        if pagination_container['page_info']['has_next_page']:
            end_cursor = pagination_container['page_info']['end_cursor']
            yield response.follow(
                url=func_pagination_url(
                    first_entry=False,
                    cursor=end_cursor
                ),
                callback=callback,
                # cb_kwargs={'followers': followers},
                meta={
                    'pagination_url': response.meta['pagination_url'],
                    'account_name': response.meta['account_name']
                }
            )
        for edge in pagination_container['edges']:
            item = item_class(
                account_name=response.meta['account_name'],
                user_name=edge['node']['username']
            )
            yield item

    def followers_parse(self, response):
        yield from self.pagination_parse(
            response=response,
            func_pagination_url=response.meta['pagination_url'].get_followers_url,
            callback=self.followers_parse,
            item_class=FollowersItem
        )

    def following_parse(self, response):
        yield from self.pagination_parse(
            response=response,
            func_pagination_url=response.meta['pagination_url'].get_following_url,
            callback=self.following_parse,
            item_class=FollowingItem
        )


class PaginationURL:
    _api_url = "/graphql/query/"

    def __init__(self, response):
        self.followers_query_hash = {'query_hash': '5aefa9893005572d237da5068082d8d5'}
        self.following_query_hash = {'query_hash': '3dec7e2c57367ef3da3d987d89f9dbc8'}
        js_data = InstagramSpider.js_data_extract(response)
        self.user_id = js_data['entry_data']['ProfilePage'][0]['graphql']['user']['id']

    def get_followers_url(self, first_entry=False, cursor=None):
        return self.__get_url(self.followers_query_hash, first_entry, cursor)

    def get_following_url(self, first_entry=False, cursor=None):
        return self.__get_url(self.following_query_hash, first_entry, cursor)

    def __get_url(self, query_hash, first_entry, cursor):
        # query example:
        # https://www.instagram.com/graphql/query/?query_hash=5aefa9893005572d237da5068082d8d5&
        # variables={"id":"267685466","include_reel":true,"fetch_mutual":true,"first":24}
        if first_entry:
            variables = {'variables': json.dumps({
                'id': self.user_id,
                'include_reel': True,
                'fetch_mutual': False,
                'first': 24
            })}
        else:
            # query_hash: 3dec7e2c57367ef3da3d987d89f9dbc8
            # variables: {"id":"929565597","include_reel":true,"fetch_mutual":false,"first":12,"after":"QVFDaUxoelVva1pJSnM3eFU0WEd3R3REbGxZYnpIa0lORExYS3EtU0JfX040QWlEYThQSzczTGdwNFV5YnZ5QTJzay1VRVZDR05TU0g0WkUwamlLQjdDTA=="}
            variables = {'variables': json.dumps({
                'id': self.user_id,
                'include_reel': True,
                'fetch_mutual': False,
                'first': 12,
                'after': cursor
            })}
        params = dict()
        params.update(query_hash)
        params.update(variables)
        return f'https://www.instagram.com{self._api_url}?{urlencode(params)}'
