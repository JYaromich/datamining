# Управляющий класс
from scrapy.crawler import CrawlerProcess

from scrapy.settings import Settings
from head_hunter.spiders.head_hunter_spider import HeadHunterSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule('head_hunter.settings')
    crawler_proc = CrawlerProcess(settings=crawler_settings)

    crawler_proc.crawl(HeadHunterSpider)  # запуск spider
    crawler_proc.start()
