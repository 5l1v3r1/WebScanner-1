# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class FormItem(scrapy.Item):
    action = scrapy.Field()
    method = scrapy.Field()
    inputs = scrapy.Field()

class InputItem(scrapy.Item):
    name = scrapy.Field()
