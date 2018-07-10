# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

from scrapy.conf import settings

from anjuke.items import AnjukeItem, AnjukeOldItem, AnjukeRenItem

# 新房
class AnjukePipeline(object):
    def process_item(self, item, spider):
        return item

class PymongoAnJuKePipeline(object):

    def __init__(self):

        conn = pymongo.MongoClient(host=settings['MONGODB_HOST'],
                                   port=settings['MONGODB_PORT'])
        db = conn[settings['MONGODB_DB']]
        self.collection = db[AnjukeItem.collections]

    def process_item(self, item, spider):
        if isinstance(item, AnjukeItem):

            self.collection.update({'id': item['id']}, {'$set': item}, True)

        return item
# 二手房
class AnjukeOldPipeline(object):
    def process_item(self, item, spider):
        return item

class PymongoAnJuKeOldPipeline(object):

    def __init__(self):

        conn = pymongo.MongoClient(host=settings['MONGODB_HOST'],
                                   port=settings['MONGODB_PORT'])
        db = conn[settings['MONGODB_DB']]
        self.collection = db[AnjukeOldItem.collections]

    def process_item(self, item, spider):
        if isinstance(item, AnjukeOldItem):

            self.collection.update({'id': item['id']}, {'$set': item}, True)

        return item
# 出租房
class AnjukeRenPipeline(object):
    def process_item(self, item, spider):
        return item

class PymongoAnJuKeRenPipeline(object):

    def __init__(self):

        conn = pymongo.MongoClient(host=settings['MONGODB_HOST'],
                                   port=settings['MONGODB_PORT'])
        db = conn[settings['MONGODB_DB']]
        self.collection = db[AnjukeRenItem.collections]

    def process_item(self, item, spider):
        if isinstance(item, AnjukeRenItem):

            self.collection.update({'id': item['id']}, {'$set': item}, True)

        return item