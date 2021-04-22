import json
from datetime import datetime

import scrapy

from instagram.items import TagInstagramItem, PostInstagramItem
from loader import TagInstagramLoader, PostInstagramLoader


class InstagramLSpider(scrapy.Spider):
    name = 'instagram_l'
    allowed_domains = ['www.instagram.com']
    start_urls = ['https://www.instagram.com/']
    _login_url = 'accounts/login/ajax/'
    tag_path = '/explore/tags/'

    def __init__(self, login, password, tags, *args, **kwargs):
        self.login = login
        self.password = password
        self.tags = tags
        super().__init__(*args, **kwargs)

    def parse(self, response):
        try:
            js_data = self.js_data_extract(response)
            yield scrapy.FormRequest(
                response.urljoin(self._login_url),
                method='POST',
                callback=self.parse,
                formdata={
                    'username': self.login,
                    'enc_password': self.password
                },
                headers={'X-CSRFToken': js_data['config']['csrf_token']}
            )
        except AttributeError:
            if response.json()['authenticated']:
                for tag in self.tags:
                    yield response.follow(
                        f'{self.tag_path}{tag}/',
                        callback=self.tag_parse,
                        meta={'tag_name': tag}
                    )

    def tag_parse(self, response):
        js_data = self.js_data_extract(response)
        tag_loader = TagInstagramLoader(response=response, item=TagInstagramItem())
        tag_loader.add_value('date_parse', datetime.now())
        tag_loader.add_value('data', js_data['entry_data']['TagPage'][0]['data'])
        yield from self.post_parse(response)
        yield tag_loader.load_item()

    def js_data_extract(self, response):
        script = response.xpath('//body/script[contains(text(), "window._sharedData =" )]/text()').extract_first()
        return json.loads(script.replace('window._sharedData = ', '')[:-1])

    def pagination(self, response, js_data):
        try:
            next_max_id = js_data['entry_data']['TagPage'][0]['data']['recent']['next_max_id']
            next_page = js_data['entry_data']['TagPage'][0]['data']['recent']['next_page']
            request_url = f'https://i.instagram.com/api/v1/tags/{response.meta["tag_name"]}/sections/'
            yield scrapy.FormRequest(
                request_url,
                method='POST',
                callback=self.post_parse,
                formdata={
                    'max_id': f'{next_max_id}',
                    'page': str(next_page)
                }
            )
        except AttributeError:
            print('It was last page')

    def post_parse(self, response):
        yield from self.pagination(response, self.js_data_extract(response))
        js_data = self.js_data_extract(response)['entry_data']['TagPage'][0]['data']['recent']['sections']
        for item in js_data:
            for media in item['layout_content']['medias']:
                post_loader = PostInstagramLoader(response=response, item=PostInstagramItem())
                post_loader.add_value('date_parse', datetime.now())
                post_loader.add_value('data', media)
                yield post_loader.load_item()
