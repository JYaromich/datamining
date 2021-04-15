import scrapy
from scrapy.http.response import Response

class HeadHunterSpider(scrapy.Spider):
    name = 'head_hunter'

    def start_requests(self):
        urls = ['https://hh.ru/search/vacancy?schedule=remote&L_profession_id=0&area=113']

        for url in urls:
            yield Response.follow(url, callback=paggination_parse)

    def paggination_parse(self, response):
        pass