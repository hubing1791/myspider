# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup as bs
from mytorspider.items import MytorspiderItem
import random
import time
import re


# scrapy crawl teahorse -o 15000_15674.json

class TeahorseSpider(scrapy.Spider):
    name = 'teahorse'
    allowed_domains = ['7zj4oshsyhokgus6fyk7pmdiubu4mkjpjjprjkvopnhnwylr522tymqd.onion']
    cookies_teahorse = \
        {
            'sayhi': 'YkBsUfULaq5rJdISSHZZdwTOddARhWE55ZoPgGbQHBR5BB/fzTMCAeP4sr9+kIy5',
            'memberAuth': '652ba31xJDspAkS%2BARzsDd%2F4dp8064RXQjZNOio31JlAYbNx'
                          '%2BdcLvmmXwQwO08HWy4482mftMjsgiTMTffHEUHFPthg '
        }

    meta_para = {
        'dont_redirect': True,
        'handle_httpstatus_list': [302]}

    def start_requests(self):
        for i in range(9000,9,-1):
            url = 'http://7zj4oshsyhokgus6fyk7pmdiubu4mkjpjjprjkvopnhnwylr522tymqd.onion/info/{page}'.format(page=i)
            yield scrapy.Request(url=url, cookies=self.cookies_teahorse, meta=self.meta_para, callback=self.parse,
                                 encoding='utf-8')

    def parse(self, response):
        # with open('off_shelf','wb') as f:
        #     f.write(response.body)
        # sleep_time = random.random() * 5
        # print(sleep_time)
        # time.sleep(sleep_time)

        soup = bs(response.body, 'lxml')
        flag = soup.find(name='div',class_='title')#如果商品下架则为空
        if flag:
            print('商品已下架')
            return None
        title = soup.find(name='h2').get_text()
        sale_txt = soup.find_all(name='p')[3].get_text()
        sale = re.search(r'\d+', sale_txt).group()
        price_txt = soup.find(name='p', class_='product_price text-danger').get_text()
        price = re.search(r'\d+\.?\d*', price_txt).group()
        seller = soup.find_all(name='span')[3].get_text()
        description = soup.find(name='div', class_='product-content').get_text()
        description = re.sub(r'\r|\n|\\s|\t| ', '', description)

        item = MytorspiderItem()
        item['sale'] = sale
        item['title'] = title
        item['seller'] = seller
        item['price'] = price
        item['description'] = description
        yield item
