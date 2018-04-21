# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class FormItem(scrapy.Item):
    url = scrapy.Field()
    form_id = scrapy.Field()

class InputItem(scrapy.Item):
    url = scrapy.Field()
    form_id = scrapy.Field()
    complete = scrapy.Field()
    type_attr = scrapy.Field()