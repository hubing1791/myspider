# -*- coding: utf-8 -*-
import scrapy


class CctvSpider(scrapy.Spider):
    name = 'cctv'
    allowed_domains = ['news.cctv.com']
    start_urls = ['https://news.cctv.com/']

    def parse(self, response):
        pass
