# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

#新房
class AnjukeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    collections = 'xinfang'
    id = scrapy.Field()
    img = scrapy.Field()
    title = scrapy.Field()
    address = scrapy.Field()
    house_type = scrapy.Field()
    status_icon = scrapy.Field()
    tag = scrapy.Field()
    price = scrapy.Field()
    tel = scrapy.Field()
    name = scrapy.Field()
    area_name = scrapy.Field()
    type_name = scrapy.Field()
# 二手房
class AnjukeOldItem(scrapy.Item):
    collections = 'ershoufang'
    id = scrapy.Field()
    img = scrapy.Field()
    title = scrapy.Field()
    address = scrapy.Field()
    house_type = scrapy.Field()
    tag = scrapy.Field()
    price = scrapy.Field()
    name = scrapy.Field()
    area_name = scrapy.Field()
# 出租房
class AnjukeRenItem(scrapy.Item):

    collections = 'chuzufang'
    id = scrapy.Field()
    img = scrapy.Field()
    title = scrapy.Field()
    address = scrapy.Field()
    house_type = scrapy.Field()
    tag = scrapy.Field()
    price = scrapy.Field()
    name = scrapy.Field()
    area_name = scrapy.Field()
    type_name = scrapy.Field()