# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DataminningspiderItem(scrapy.Item):
    news_class = scrapy.Field()
    content = scrapy.Field()
