# Управляющий класс
from scrapy.crawler import CrawlerProcess

from scrapy.settings import Settings
from avitoflat.spiders.flatspider import FlatspiderSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule('avitoflat.settings')
    crawler_proc = CrawlerProcess(settings=crawler_settings)

    crawler_proc.crawl(FlatspiderSpider)  # запуск spider
    crawler_proc.start()
