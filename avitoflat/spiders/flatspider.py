import scrapy

from loader import AvitoFlatLoader


class FlatspiderSpider(scrapy.Spider):
    name = 'flatspider'
    allowed_domains = ['www.avito.ru']
    url = 'https://www.avito.ru/krasnodar/nedvizhimost'


    def start_requests(self):
        yield scrapy.Request(
            url=self.url,
            callback=self.parse
        )

    def _get_follow_xpath(self, response, selector, callback, **kwargs):
        for link in response.xpath(selector):
            yield response.follow(link, callback=callback, cb_kwargs=kwargs)

    _xpath_selector = {
        'target': '//a[contains(@title, "Все квартиры")]/@href',
        'flat': '//div[@data-marker="catalog-serp"]/div[@data-marker="item"]//div[contains(@class, "iva-item-body")]//a[@itemprop="url"]/@href',
        'pagination': '//div[contains(@class, "pagination-hidden")]//a[@class="pagination-page"]/@href',
    }

    def parse(self, response, **kwargs):
        yield from self._get_follow_xpath(response, self._xpath_selector['target'], callback=self.parse_target)

    def parse_target(self, response):
        yield from self._get_follow_xpath(response, self._xpath_selector['flat'], callback=self.flat_parse)
        yield from self._get_follow_xpath(response, self._xpath_selector['pagination'], callback=self.parse_target)

    _xpath_data_query = {
        'title': '//span[@class="title-info-title-text"]/text()',
        'price': '//head/meta[@property="product:price:amount"]/@content',
        'address': '//div[@class="item-map-location"]//span[@class="item-address__string"]/text()',
        'flat_params': '//div[@class="item-params"]/ul[@class="item-params-list"]/li',
        'author_url': '//div[@class="seller-info-value"]/div[@data-marker="seller-info/name"]/a/@href',
        # 'phone': '//script'
    }

    def flat_parse(self, response):
        loader = AvitoFlatLoader(response=response)
        loader.add_value('url', response.url)
        for key, xpath_query in self._xpath_data_query.items():
            loader.add_xpath(key, xpath_query)
        yield loader.load_item()
