# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem

class UniquePipeline(object):
    def __init__(self):
        self.seen = set()

    def process_item(self, item, spider):
        if str(item) in self.seen:
            raise DropItem('Duplicate')
        self.seen.add(str(item))
        return item
