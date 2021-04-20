# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import time

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from scrapy.exceptions import IgnoreRequest


class AvitoflatSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class AvitoflatDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called

        raw_cookie = 'v=1618904415; _ga=GA1.2.1262986010.1618738183; _gid=GA1.2.789642832.1618738183; _gat_UA-2546784-1=1; __gads=ID=4442a95965ca95c9-22d1673d28bb00d4:T=1618738184:RT=1618910437:S=ALNI_MZ4PZmYv9lUhEIaLTLG8PMV96rVWg; buyer_from_page=vertical; _dc_gtm_UA-2546784-1=1; _fbp=fb.1.1618738183852.717434837; _ym_visorc=b; no-ssr=1; st=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjoidko0TkJ5SlU2TElJTGRDY3VNTkdBYnlzVGk3VTVKRW8wVkZQNXBSVll0ZVlpM0lxVUJ1Q2JQVUtjS0FnSGJvRUYxRjNYQUNvWWVzbWJwRkxZYWtreW9nTW1aZ2puTmlMc0RmVGRoUi8wTmh3ZHQ3dVZ5eW1TME5ManBYQnNrdTBxaEVEZVBUTXhxN2E5UEdHT2Q4VGRJc0VYT3JYSElzOERhZ2dFa1EwMTRMM0FIamdJQkVRQzl6ZVM4OS9pZ25YTGJ3czZPeVVFREhiT1JFU1dueWJKVFU4d1Q4TzQvMnRGZVhWdlRpL1htVU1rOUl1RnFTMzBOYSs0Z0N0MUVhTGVoY1R6S3MxbGg4TnFIVWdhNkYrdUF1MVU3WGJrM1kyaXQ1RVJ6bHYxalNtdXpqZnV5bituZmppMEpYS1AwYloiLCJpYXQiOjE2MTg3MzgxODAsImV4cCI6MTYxOTk0Nzc4MH0.uIe7iOeCNp2-py29u22bUmgBdHrNt5C6ST2XLekzsDw; buyer_location_id=633340; dfp_group=68; sx=H4sIAAAAAAACA53PQY7CMAyF4btkzcJRneJym%2BJSw7gQOi41FHH3CYtKsB0puyhf3v8Me83Nsd9Oy%2BwIQiQMnIXZw%2B4Z5rAL09EwpvHw6BHFrBxigCyoSAoSNuEQdrGO1KRUYXptAi2d9no7P0CMBTC7ZyNjWkk1z3e7XKxckmYHJUBzUWUm4A%2ByAYpvkodhGa99nfZavkdgYicqb1aybfPhhr%2FjnNRJUMARmTkbKgvlr5XbCgrZXGW8jyc4nzCXb9mQjNxQVnIY2hSn0zxdkLF0u5YcUxJQcfHPlTVV75Vdmru4be8LQKHEwMmgpOeVjPAz8t6o7SpEKxku2crSMlc8f4VXMVWFTNaPw9Ua6LBgLqXdAcjxX2RNr9cfTSvex%2FMBAAA%3D; abp=0; SEARCH_HISTORY_IDS=1; _ym_isad=2; __utma=99926606.1262986010.1618738183.1618753724.1618868959.2; __utmc=99926606; __utmz=99926606.1618757272.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); f=5.cc913c231fb04cedfe85757b7948761ec1e8912fd5a48d02c1e8912fd5a48d020d9c6ee1a76cd5990d9c6ee1a76cd599c1e8912fd5a48d02c1e8912fd5a48d02c1e8912fd5a48d02c1e8912fd5a48d02c1e8912fd5a48d02c1e8912fd5a48d0246b8ae4e81acb9fa143114829cf33ca746b8ae4e81acb9fad99271d186dc1cd062a5120551ae78ed10ccd2dbdc934178cdb5f5818d21c228e5938715442e605abed76bde8afb15d2fb0fb526bb39450a46b8ae4e81acb9fae2415097439d4047d50b96489ab264edc772035eab81f5e1e992ad2cc54b8aa8d99271d186dc1cd03de19da9ed218fe23de19da9ed218fe23de19da9ed218fe2e992ad2cc54b8aa846b8ae4e81acb9fa24a135baa76198dec65ae03f9a26adaec4ed941cada6237aad337132ee4c0597f7f4d5e422becca59bedcbc25bfebb75976e1a45efa94ebfd3e75091b84097b72d57da0d3d3274b10616349da3da33c3b59f191313adc1ea46b8ae4e81acb9fa46b8ae4e81acb9fa02c68186b443a7acf8b817f3dc0c3f2103de54f981657f912da10fb74cac1eab2da10fb74cac1eab00b11584c9fb93e03bbd3bcc750a84cd807b091b4f68e13ae4700427b080c933; ft="DRqU1Ieya9HzVMNBmb2M/XhPORIgRvWrQD3h4OTCbeTo4Zvb2ZaCsKFV+mS9q7/WTWWnwuC1tDME2+yNGmV8JOGcIvQr2nBgZ2p30B9JVUJsqGbiZvSg+hLyQjZEIyFaNGeAaBghXxiZju5oIuoLQUlsEcyjFIAV1XoogmkCfPnWahVv+ThurZIM/rPc7mEN"; buyer_local_priority_v2=0; buyer_selected_search_radius4=0_general; luri=krasnodar; buyer_laas_location=633540; cto_bundle=rNNNP185SnluUzZTMllnTWJyeUR0ZjB4a2ZsNkVuZDZsazByRlhqd2olMkJVTlI1UDl5a0JHYTV5T20zQ0dqOTFBRUFQWWltVFdaWExRUGRTU0YlMkJnVXZmbSUyQmpIOWdDcnR0T0slMkZBeENrb3k5MVA1RkxldmlvcWlMMkZ1QjFRVFl3V0tZRyUyQjlhRE5XRVIlMkYxTk4wWTVCVlhSc3Zad0kwbGxLY3lEelJiY3FPMjE3Vkw3SzQlM0Q; lastViewingTime=1618749379916; showedStoryIds=63-62-61-58-50-49-48-47-42-32; _ym_d=1618738183; _ym_uid=1618738183650299472; _gcl_au=1.1.1772951910.1618738181; __cfduid=df286f39ad9bf521667c8eed93c2a3cd21618738179; u=2onxhzm2.ahv7ib.d2og7ex0kq80'
        cookies = {}
        for cookie in raw_cookie.split('; '):
            cookies[cookie.split('=')[0]] = cookie.split('=')[-1]
        return request.cookies.update(cookies)


    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        if response.status in [403, 429]:
            time.sleep(10)
            raise request
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
