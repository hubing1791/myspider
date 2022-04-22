# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
from bs4 import BeautifulSoup as bs
import re
from dataminningspider.items import DataminningspiderItem

url_class = ['IT', '军事', '健康', '国际', '娱乐',
             '体育', '汽车', '房产', '能源', '文化']
url_class_1 = ['国际', '体育', '文化', '娱乐', '房产','汽车']


def geturl(name, start=0, end=0):
    csv_path = 'E:/code/pycode/dataming_project/dataminningspider/dataminningspider/url_csv/' + name + '.csv'
    if start and end:
        url_list = pd.read_csv(csv_path, usecols=[1], skiprows=start - 1, nrows=(end - start + 1), header=None)
    else:
        url_list = pd.read_csv(csv_path, usecols=[1])
    return url_list


class ChinanewsSpider(scrapy.Spider):
    name = 'chinanews'
    allowed_domains = ['chinanews.com']

    def start_requests(self):
        for classname in url_class_1:
            url_list = geturl(classname, 110000, 160000)
            url_list = url_list.values.tolist()
            for url in url_list:
                yield scrapy.Request(url=url[0], meta={'class': classname}, callback=self.parse, encoding='utf-8')

    def parse(self, response):
        # if response.apparent_encoding == 'Windows-1254':
        #     response.encoding = 'utf-8'
        # else:
        #     response.encoding = 'gbk'
        text = response.text
        soup = bs(text, 'lxml')
        temp = soup.find_all(name='div', class_="left_zw")
        if temp:
            temp = temp[0].find_all(name='p')
        else:
            temp = soup.find_all(name='div', class_="font16Style")
            temp = temp[0].find_all(name='p')

        text_inte = ''
        for temp_ in temp:
            text_part = re.sub(r'\r|\n|\\s|\t| ', '', temp_.get_text())
            text_inte += text_part
        text_inte_noblank = ''.join(text_inte.split())
        item = DataminningspiderItem()
        item['news_class'] = response.meta['class']
        item['content'] = text_inte_noblank
        yield item
