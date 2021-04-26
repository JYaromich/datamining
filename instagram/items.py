# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Field


class TagInstagramItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    date_parse = Field()
    data = Field()


class PostInstagramItem(scrapy.Item):
    date_parse = Field()
    data = Field()
    photos = Field()
