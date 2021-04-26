import os
import dotenv
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from instagram.spiders.instagram_l import InstagramLSpider

if __name__ == '__main__':
    dotenv.load_dotenv('.env')

    crawler_settings = Settings()
    crawler_settings.setmodule('instagram.settings')
    crawler_proc = CrawlerProcess(settings=crawler_settings)
    tags = ['python', 'programming']
    crawler_proc.crawl(
        InstagramLSpider,
        login=os.getenv('USERNAME'),
        password=os.getenv('ENC_PASSWORD'),
        tags=tags
    )
    crawler_proc.start()
