import scrapy
from bs4 import BeautifulSoup as bs
import re
from mytorspider.items import MytorspiderItem
import time
import random


# scrapy crawl darknetchina -o 15000_15674.json -s FEED_EXPORT_ENCODING=UTF-8

class DarknetchinaSpider(scrapy.Spider):
    name = 'darknetchina'
    allowed_domains = ['chinamwmpur6oszg.onion']
    start_urls = ['http://http://chinamwmpur6oszg.onion/']
    cookies_darknetchina = {
        '_csrf-f': '1cc572875e970200169ee684e20aaa3f227ddb0961da20a0d1da97be7a56b958a%3A2%3A%7Bi%3A0%3Bs%3A7%3A'
                   ' %22_csrf-f%22%3Bi%3A1%3Bs%3A32%3A%226_NyRX_UK_QhsSzUmfhkOg_LXabGTFJx%22%3B%7D',
        'prodatep': '1603372770',
        'prosctp': 'f24c4dbeba5b65c2ae2a26e453edbfad',
        'requestidp': '6152542108740502',
        'websitesess': 'af10d100d8f56f42710356b3a23322c5'
    }
    meta_para = {
        'dont_redirect': True,
        'handle_httpstatus_list': [302]}

    # 动态生成初始 URL
    def start_requests(self):
        for i in range(12500, 12000, -1):
            url = 'http://chinamwmpur6oszg.onion/goods/info?id={page}'.format(page=i)
            yield scrapy.Request(url=url, cookies=self.cookies_darknetchina, meta=self.meta_para, callback=self.parse,
                                 encoding='utf-8')

    def parse(self, response):
        sleep_time = random.random() * 5
        print(sleep_time)
        time.sleep(sleep_time)
        soup = bs(response.body, 'lxml')
        flag_invit = soup.i
        if flag_invit and response.status == 200:
            if len(soup.find_all('a')[-1].get_text()) <= 3:
                print("页面不存在\n")
                return None

            title = soup.h3.get_text()

            sale_txt = soup.find(name='a', href="#").get_text()
            sale = re.search(r'\d+', sale_txt).group()

            price_txt = soup.find(name='span', class_="regular-price").get_text()
            price = re.search(r'\d+\.?\d*', price_txt).group()

            seller = soup.find(name='span', style="color:red").get_text()

            description = soup.find(name='div', id="tab_one", class_="tab-pane fade show active",
                                    style="word-wrap: break-word; white-space: pre-line;").get_text()
            description = re.sub(r'\r|\n|\\s', '', description)
            description = re.sub('[ ]', '', description)
            item = MytorspiderItem()
            item['sale'] = sale
            item['title'] = title
            item['seller'] = seller
            item['price'] = price
            item['description'] = description
            yield item

            # file_object = open(self.file_path_json, 'wb')
            # str_json = '{\n\"sale\":\"' + sale + '\",' + '\n\"seller\":\"' + seller + '\",' + \
            #            '\n\"price\":\"' + price + '\",' + '\n\"title\":\"' + title + '\",' + \
            #            '\n\"description\":\"' + description + '\"\n},'
            # print(description)
            # file_object.write(bytes(str_json, encoding='utf-8'))
            # file_object.close()
            print("爬取成功\n")
        else:
            print("页面不存在\n")

        # print(html)
        # title = response.xpath('//*[@id="goodsorderid"]/h3').extract()
        # title = ''.join(title)
        # #title = title.replace('</h3>', '')
        # sale = response.xpath('//*[@id="goodsorderid"]/div[1]/div/span/a').extract()
        # sale = ''.join(sale)
        # money = response.xpath('//*[@id="goodsorderid"]/div[2]/span/text()').extract()
        # money = ''.join(money)
        # seller = response.xpath('//*[@id="tab_one"]/p[2]/span').extract()
        # seller = ''.join(seller)
        # describe = response.xpath('//*[@id="tab_one"]/text()').extract()
        # describe = ''.join(describe)
        # print(title+'\n'+sale+'\n'+money+'\n'+seller+"\n"+describe)
