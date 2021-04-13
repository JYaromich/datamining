import urllib.parse as up
import scrapy
import pymongo



class AutoyoulaSpider(scrapy.Spider):
    name = 'autoyoula'
    allowed_domains = ['auto.youla.ru']
    start_urls = ['https://auto.youla.ru/']
    _css_selectors = {
        'brands': 'div.ColumnItemList_container__5gTrc a.blackLink',
        'pagination': 'div.Paginator_block__2XAPy a.Paginator_button__u1e7D',
        'car': '#serp article.SerpSnippet_snippet__3O1t2 a.SerpSnippet_name__3F7Yu'
    }
    collection = pymongo.MongoClient('mongodb://localhost')['gb_data_mining']['autoyoula']

    def _get_follow(self, response, selector_scc, callback, **kwargs):
        for link_selector in response.css(selector_scc):
            yield response.follow(link_selector.attrib.get('href'), callback=callback)

    def parse(self, response):
        yield from self._get_follow(response, self._css_selectors['brands'], callback=self.brand_parse)

    def brand_parse(self, response):
        yield from self._get_follow(response, self._css_selectors['pagination'], callback=self.brand_parse)
        yield from self._get_follow(response, self._css_selectors['car'], callback=self.car_parse)

    def car_parse(self, response):
        data = {
            'title': response.css('div.AdvertCard_advertTitle__1S1Ak::text').extract_first(),
            'url': response.url,
            'photos': self._get_photos(response),
            'characteristics': {
                characteristics_row.css('.AdvertSpecs_label__2JHnS::text').extract_first():
                    characteristics_row.css('.AdvertSpecs_data__xK2Qx::text').get()
                    or characteristics_row.css('.AdvertSpecs_data__xK2Qx .blackLink::text').get()
                for characteristics_row in response.css('.AdvertSpecs_row__ljPcX')},
            'describe': response.css('.AdvertCard_descriptionInner__KnuRi::text').get(),
            'author_url': self._get_author_url(response)

        }
        self._save(data)

    def _save(self, data):
        self.collection.insert_one(data)

    def _get_author_url(self, response):
        try:
            url_id = response.css('script::text').re(r"youlaId%22%2C%22([a-zA-Z|\d]+)%22%2C%22avatar")
            return response.urljoin(f'/user/{url_id[0]}')
        except Exception as ex:
            print(ex)

    def _get_photos(self, response):
        script_text = response.css('script').re('big%22%2C%22[a-zA-Z|\d|%|\.|\_]+%22%5D%5D%5D%5D%2C%22')
        return [up.unquote(url) for url in script_text[0].split('%22%2C%22') if 'http' in url][::4]
