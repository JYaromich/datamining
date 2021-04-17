import scrapy

from loader import HeadHunterLoader


class HeadHunterSpider(scrapy.Spider):
    name = 'head_hunter'
    start_urls = ['https://hh.ru/search/vacancy?schedule=remote&L_profession_id=0&area=113']

    _xpath_selector = {
        'pagination': '//div[@data-qa="pager-block"]//a[@class="bloko-button"]/@href',
        'vacancy': '//span[@class="resume-search-item__name"]//a[@class="bloko-link"]/@href',
        'author': '//a[@data-qa="vacancy-company-name"]/@href'
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _get_follow_xpath(self, response, selector, callback, **kwargs):
        for link in response.xpath(selector):
            yield response.follow(link, callback=callback, **kwargs)

    def parse(self, response, **kwargs):
        yield from self._get_follow_xpath(response, self._xpath_selector['pagination'], callback=self.parse)
        yield from self._get_follow_xpath(response, self._xpath_selector['vacancy'], callback=self.vacancy_parse)

    _xpath_vacancy_data_query = {
        'title': '//h1[@data-qa="vacancy-title"]/text()',
        'salary': '//p[@class="vacancy-salary"]/span[@data-qa="bloko-header-2"]',
        'description': '//div[@class="vacancy-description"]//div[@data-qa="vacancy-description"]',
        'skills': '//div[@class="vacancy-section"]//div[contains(@data-qa, "skills-element")]//text()',
        'author_url': '//a[@data-qa="vacancy-company-name"]/@href'
    }

    def vacancy_parse(self, response):
        loader = HeadHunterLoader(response=response)
        for key, selector in self._xpath_vacancy_data_query.items():
            loader.add_xpath(key, selector)

        yield from self._get_follow_xpath(
            response,
            self._xpath_selector['author'],
            callback=self.author_parse,
            meta={'item': loader.load_item()}
        )

    _xpath_query_author = {
        'author': '//div[@class="employer-sidebar-header"]//span[@class="company-header-title-name"]',
        'site_url': '//div[@class="employer-sidebar"]//a[@class="g-user-content"]/@href',
        'deal': '//div[contains(text(), "Сферы деятельности")]/../p/text()',
        'author_description': '//div[@class="sticky-container"]//div[@data-qa="company-description-text"]',
    }


    def author_parse(self, response):
        loader = HeadHunterLoader(item=response.meta['item'], response=response)
        for key, selector in self._xpath_query_author.items():
            loader.add_xpath(key, selector)

        loader.add_xpath('author_description', '//div[@class="tmpl_hh_wrapper"]//div[contains(@class, "description")]')
        loader.add_xpath('author_description', '//div[@class="tmpl_hh_wrapper"]//div[contains(@class, "about")]')



        yield scrapy.http.Request(
            url=f'https://hh.ru/shards/employerview/vacancies?currentEmployerId={response.url.split("/")[-1]}&json=true',
            meta={'item': loader.load_item()},
            # method='GET',
            callback=self._add_vacancy_author_list
        )

    def _add_vacancy_author_list(self, response):
        loader = HeadHunterLoader(item=response.meta['item'], response=response)
        json_data = response.json()
        loader.add_value('company_vacancy', [vacancy['name'] for vacancy in json_data['vacancies']])
        loader.add_value('author', json_data['vacancies'][0]['company']['name'])

        yield loader.load_item()
