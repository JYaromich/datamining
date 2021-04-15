import urllib.parse as up
import scrapy
import pymongo

from loaders import AutoyoulaLoader


class AutoyoulaSpider(scrapy.Spider):
    name = 'autoyoula'
    allowed_domains = ['auto.youla.ru']
    start_urls = ['https://auto.youla.ru/']

    _xpath_selector = {
        'brands': '//a[@data-target="brand"]/@href',
        'pagination': '//div[contains(@class, "Paginator_block")]/a[@data-target-id="button-link-serp-paginator"]/@href',
        'car': '//article[@data-target="serp-snippet"]//a[@data-target="serp-snippet-title"]/@href'
    }
    collection = pymongo.MongoClient('mongodb://localhost')['gb_data_mining']['autoyoula']

    def _get_follow_xpath(self, response, selector, callback, **kwargs):
        for link in response.xpath(selector):
            yield response.follow(link, callback=callback, cb_kwargs=kwargs)

    def parse(self, response):
        yield from self._get_follow_xpath(response, self._xpath_selector['brands'], callback=self.brand_parse)

    def brand_parse(self, response):
        yield from self._get_follow_xpath(response, self._xpath_selector['pagination'], callback=self.brand_parse)
        yield from self._get_follow_xpath(response, self._xpath_selector['car'], callback=self.car_parse)

    _xpath_data_query = {
        'title': '//div[@data-target="advert-title"]/text()',
        'price': '//div[@data-target="advert-price"]/text()',
        'photos': '//div[contains(@class, "PhotoGallery_block")]//figure/picture/img/@src',
        'characteristics': '//div[contains(@class, "AdvertCard_specs")]/div/div[contains(@class, "AdvertSpecs_row")]',
        'description': '//div[@data-target="advert-info-descriptionFull"]/text()',
        'author_url': '//body/script[contains(text(), "window.transitState = decodeURIComponent")]'

    }

    def car_parse(self, response):
        loader = AutoyoulaLoader(response=response)
        loader.add_value('url', response.url)
        for key, selector in self._xpath_data_query.items():
            loader.add_xpath(key, selector)
        yield loader.load_item()

    def _save(self, data):
        self.collection.insert_one(data)

    # def _get_photos(self, response):
    #     script_text = response.css('script').re('big%22%2C%22[a-zA-Z|\d|%|\.|\_]+%22%5D%5D%5D%5D%2C%22')
    #     return [up.unquote(url) for url in script_text[0].split('%22%2C%22') if 'http' in url][::4]
