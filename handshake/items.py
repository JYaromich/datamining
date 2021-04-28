# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class InstagramItem(scrapy.Item):
    account_name = Field()
    user_name = Field()


class FollowingItem(InstagramItem):
    pass


class FollowersItem(InstagramItem):
    pass
