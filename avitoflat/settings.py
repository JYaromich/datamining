# Scrapy settings for avitoflat project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'avitoflat'

SPIDER_MODULES = ['avitoflat.spiders']
NEWSPIDER_MODULE = 'avitoflat.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# FAKEUSERAGENT_PROVIDERS = [
#     'scrapy_fake_useragent.providers.FakeUserAgentProvider',  # this is the first provider we'll try
#     'scrapy_fake_useragent.providers.FakerProvider',
    # if FakeUserAgentProvider fails, we'll use faker to generate a user-agent string for us
    # 'scrapy_fake_useragent.providers.FixedUserAgentProvider',  # fall back to USER_AGENT value
# ]

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36'
# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 16

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs

# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 5
# CONCURRENT_REQUESTS_PER_IP = 5

# Disable cookies (enabled by default)
COOKIES_ENABLED = True
COOKIES_DEBUG = True

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    # 'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    # 'Host': 'www.avito.ru',
    # 'Accept-Encoding': 'gzip, deflate, br',
    # 'Connection': 'keep-alive',
    # 'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
    # 'sec-ch-ua-mobile': '?0',
    # 'sec-fetch-dest': 'document',
    # 'sec-fetch-mode': 'navigate',
    # 'sec-fetch-site': 'same-origin'
    # 'Cookie': 'v=1618904415; _ga=GA1.2.1262986010.1618738183; _gid=GA1.2.789642832.1618738183; _gat_UA-2546784-1=1; __gads=ID=4442a95965ca95c9-22d1673d28bb00d4:T=1618738184:RT=1618910437:S=ALNI_MZ4PZmYv9lUhEIaLTLG8PMV96rVWg; buyer_from_page=vertical; _dc_gtm_UA-2546784-1=1; _fbp=fb.1.1618738183852.717434837; _ym_visorc=b; no-ssr=1; st=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjoidko0TkJ5SlU2TElJTGRDY3VNTkdBYnlzVGk3VTVKRW8wVkZQNXBSVll0ZVlpM0lxVUJ1Q2JQVUtjS0FnSGJvRUYxRjNYQUNvWWVzbWJwRkxZYWtreW9nTW1aZ2puTmlMc0RmVGRoUi8wTmh3ZHQ3dVZ5eW1TME5ManBYQnNrdTBxaEVEZVBUTXhxN2E5UEdHT2Q4VGRJc0VYT3JYSElzOERhZ2dFa1EwMTRMM0FIamdJQkVRQzl6ZVM4OS9pZ25YTGJ3czZPeVVFREhiT1JFU1dueWJKVFU4d1Q4TzQvMnRGZVhWdlRpL1htVU1rOUl1RnFTMzBOYSs0Z0N0MUVhTGVoY1R6S3MxbGg4TnFIVWdhNkYrdUF1MVU3WGJrM1kyaXQ1RVJ6bHYxalNtdXpqZnV5bituZmppMEpYS1AwYloiLCJpYXQiOjE2MTg3MzgxODAsImV4cCI6MTYxOTk0Nzc4MH0.uIe7iOeCNp2-py29u22bUmgBdHrNt5C6ST2XLekzsDw; buyer_location_id=633340; dfp_group=68; sx=H4sIAAAAAAACA53PQY7CMAyF4btkzcJRneJym%2BJSw7gQOi41FHH3CYtKsB0puyhf3v8Me83Nsd9Oy%2BwIQiQMnIXZw%2B4Z5rAL09EwpvHw6BHFrBxigCyoSAoSNuEQdrGO1KRUYXptAi2d9no7P0CMBTC7ZyNjWkk1z3e7XKxckmYHJUBzUWUm4A%2ByAYpvkodhGa99nfZavkdgYicqb1aybfPhhr%2FjnNRJUMARmTkbKgvlr5XbCgrZXGW8jyc4nzCXb9mQjNxQVnIY2hSn0zxdkLF0u5YcUxJQcfHPlTVV75Vdmru4be8LQKHEwMmgpOeVjPAz8t6o7SpEKxku2crSMlc8f4VXMVWFTNaPw9Ua6LBgLqXdAcjxX2RNr9cfTSvex%2FMBAAA%3D; abp=0; SEARCH_HISTORY_IDS=1; _ym_isad=2; __utma=99926606.1262986010.1618738183.1618753724.1618868959.2; __utmc=99926606; __utmz=99926606.1618757272.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); f=5.cc913c231fb04cedfe85757b7948761ec1e8912fd5a48d02c1e8912fd5a48d020d9c6ee1a76cd5990d9c6ee1a76cd599c1e8912fd5a48d02c1e8912fd5a48d02c1e8912fd5a48d02c1e8912fd5a48d02c1e8912fd5a48d02c1e8912fd5a48d0246b8ae4e81acb9fa143114829cf33ca746b8ae4e81acb9fad99271d186dc1cd062a5120551ae78ed10ccd2dbdc934178cdb5f5818d21c228e5938715442e605abed76bde8afb15d2fb0fb526bb39450a46b8ae4e81acb9fae2415097439d4047d50b96489ab264edc772035eab81f5e1e992ad2cc54b8aa8d99271d186dc1cd03de19da9ed218fe23de19da9ed218fe23de19da9ed218fe2e992ad2cc54b8aa846b8ae4e81acb9fa24a135baa76198dec65ae03f9a26adaec4ed941cada6237aad337132ee4c0597f7f4d5e422becca59bedcbc25bfebb75976e1a45efa94ebfd3e75091b84097b72d57da0d3d3274b10616349da3da33c3b59f191313adc1ea46b8ae4e81acb9fa46b8ae4e81acb9fa02c68186b443a7acf8b817f3dc0c3f2103de54f981657f912da10fb74cac1eab2da10fb74cac1eab00b11584c9fb93e03bbd3bcc750a84cd807b091b4f68e13ae4700427b080c933; ft="DRqU1Ieya9HzVMNBmb2M/XhPORIgRvWrQD3h4OTCbeTo4Zvb2ZaCsKFV+mS9q7/WTWWnwuC1tDME2+yNGmV8JOGcIvQr2nBgZ2p30B9JVUJsqGbiZvSg+hLyQjZEIyFaNGeAaBghXxiZju5oIuoLQUlsEcyjFIAV1XoogmkCfPnWahVv+ThurZIM/rPc7mEN"; buyer_local_priority_v2=0; buyer_selected_search_radius4=0_general; luri=krasnodar; buyer_laas_location=633540; cto_bundle=rNNNP185SnluUzZTMllnTWJyeUR0ZjB4a2ZsNkVuZDZsazByRlhqd2olMkJVTlI1UDl5a0JHYTV5T20zQ0dqOTFBRUFQWWltVFdaWExRUGRTU0YlMkJnVXZmbSUyQmpIOWdDcnR0T0slMkZBeENrb3k5MVA1RkxldmlvcWlMMkZ1QjFRVFl3V0tZRyUyQjlhRE5XRVIlMkYxTk4wWTVCVlhSc3Zad0kwbGxLY3lEelJiY3FPMjE3Vkw3SzQlM0Q; lastViewingTime=1618749379916; showedStoryIds=63-62-61-58-50-49-48-47-42-32; _ym_d=1618738183; _ym_uid=1618738183650299472; _gcl_au=1.1.1772951910.1618738181; __cfduid=df286f39ad9bf521667c8eed93c2a3cd21618738179; u=2onxhzm2.ahv7ib.d2og7ex0kq80',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Host': 'www.avito.ru',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
    'Accept-Language': 'ru',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
}

# ROTATING_PROXY_LIST_PATH = '/Users/janeyaromich/Учеба/Datamining/datamining/proxy_list'

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'avitoflat.middlewares.AvitoflatSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # 'avitoflat.middlewares.AvitoflatDownloaderMiddleware': 543,
    # 'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    # 'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    # 'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
    # 'scrapy_fake_useragent.middleware.RetryUserAgentMiddleware': 401,
    # 'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    # 'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'avitoflat.pipelines.AvitoflatPipeline': 300
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
DOWNLOAD_DELAY = 3

# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 10
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = True

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
