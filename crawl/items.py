# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item,Field

class CrawlItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class TaobaoLiveItem(NewsItem):
    user = Field()
    comment = Field()
