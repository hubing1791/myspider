# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MytorspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title =scrapy.Field()
    sale = scrapy.Field()
    price = scrapy.Field()
    seller = scrapy.Field()
    description = scrapy.Field()
