import scrapy


class FlatspiderSpider(scrapy.Spider):
    name = 'flatspider'
    allowed_domains = ['https://www.avito.ru']
    start_urls = ['https://www.avito.ru/krasnodar/kvartiry/prodam/']

    def _get_follow_xpath(self, response, selector, callback, **kwargs):
        for link in response.xpath(selector):
            yield response.follow(link, callback=callback, cb_kwargs=kwargs)

    _xpath_selector = {
        'flat': '//div[@data-marker="catalog-serp"]/div[@data-marker="item"]//div[contains(@class, "iva-item-body")]//a[@itemprop="url"]/@href',

    }

    def parse(self, response):
        yield from self._get_follow_xpath(response, self._xpath_selector['flat'], callback=self.flat_parse)

    def flat_parse(self, response):
        pass
