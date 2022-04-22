import datetime
import csv
import time
from bs4 import BeautifulSoup as bs
import requests
import re
import pandas as pd

url_categorys = [
    {'type': "IT", 'column_name': 'it'}, {'type': "军事", 'column_name': 'mil'},
    {'type': "健康", 'column_name': 'jk'}, {'type': "国际", 'column_name': 'gj'},
    {'type': "娱乐", 'column_name': 'yl'}, {'type': "体育", 'column_name': 'ty'},
    {'type': "汽车", 'column_name': 'auto'}, {'type': "房产", 'column_name': 'estate'},
    {'type': "能源", 'column_name': 'ny'}, {'type': "文化", 'column_name': 'wh'}
]
url_categorys_2 =[
    {'type': "葡萄酒", 'column_name': 'wine'},{'type': "生活", 'column_name': 'life'},
    {'type': "国内", 'column_name': 'gn'},{'type': "社会", 'column_name': 'sh'},
    {'type': "港澳", 'column_name': 'ga'},{'type': "台湾", 'column_name': 'tw'},
    {'type': "华人", 'column_name': 'hr'},{'type': "财经", 'column_name': 'cj'},
    {'type': "金融", 'column_name': 'fortune'}
]

url_category = [
    {'type': "IT", 'column_name': 'it'}]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}


# 把栏目名和对应的中文类别对应一下


def get_data_list(start, end, type):
    url_list = []  # 获取滚动页列表
    date_start = datetime.datetime.strptime(start, '%Y-%m-%d')
    date_end = datetime.datetime.strptime(end, '%Y-%m-%d')
    while date_start <= date_end:
        temptime = date_end.strftime('/%Y/%m%d')
        tempurl = 'http://www.chinanews.com/scroll-news/' + type + temptime + '/news.shtml'
        url_list.append(tempurl)
        date_end = date_end - datetime.timedelta(1)
    return url_list


def get_url():
    total_count = 0
    for model in url_categorys_2:
        csv_path = './url_1/' + model['type'] + '.csv'
        csv_file = open(csv_path, 'a', newline='', encoding='utf-8')
        csv_write = csv.writer(csv_file, dialect='excel')
        # csv_write.writerow(['标题', '链接'])
        url_first_list = get_data_list('2008-08-01', '2020-11-20', model['column_name'])

        for page_url in url_first_list:
            # print(page_url)
            # request_url = request.Request(page_url, headers=headers)
            # reponse = request.urlopen(request_url)
            #
            # text = reponse.read()
            # print(text.decode('gbk'))
            # print(reponse.info())
            # fp = open('page.html', 'a', encoding='utf-8')
            # fp.write(str(text.decode('gbk').encode('utf-8').decode('utf-8')))
            # fp.close()
            try:
                reponse = requests.get(page_url)
                if reponse.apparent_encoding == 'Windows-1254':
                    reponse.encoding = 'utf-8'
                else:
                    reponse.encoding = 'gbk'
                text = reponse.text
                soup = bs(text, 'lxml')
                temp = soup.find_all(name='div', class_='dd_bt')
                if temp:
                    for temp_ in temp:
                        title = temp_.get_text()
                        url = temp_.find('a').get('href')
                        csv_write.writerow([title, url])
                        print(title + ' ' + url + '\n')
                        total_count += 1
                else:
                    div_block = soup.find_all(name='div', id='news_list')
                    div_block = div_block[0].find_all('li')
                    for temp_ in div_block:
                        title = temp_.get_text()
                        if title:
                            url = 'http://www.chinanews.com' + temp_.find('a').get('href')
                            csv_write.writerow([title, url])
                            total_count += 1
                            print(title + ' ' + url + '\n')
            except:
                file_handler = open('./url_csv/fail.txt', 'a', encoding='utf-8')
                page_url = page_url + '\n'
                file_handler.write(page_url)
                file_handler.close()
            if total_count // 100 % 2 == 0:
                print('已经获取%d个url' % total_count)
            #time.sleep(0.5)


def content_get(url_str):
    response = requests.get(url_str)
    print(response.apparent_encoding)
    if response.apparent_encoding == 'Windows-1254':
        response.encoding = 'utf-8'
    else:
        response.encoding = 'utf-8'
    text = response.text
    soup = bs(text, 'lxml')
    temp = soup.find_all(name='div', class_="left_zw")
    temp = temp[0].find_all(name='p')
    text_inte = ''
    for temp_ in temp:
        text_part = re.sub(r'\r|\n|\\s|\t| ', '', temp_.get_text())
        text_part = re.sub('　　', '', text_part)
        text_inte += text_part
    print(text_inte)


def content_get_old(url_str):
    response = requests.get(url_str)
    print(response.apparent_encoding)
    if response.apparent_encoding == 'Windows-1254':
        response.encoding = 'utf-8'
    else:
        response.encoding = 'gbk'
    text = response.text
    soup = bs(text, 'lxml')
    temp = soup.find_all(name='div', class_="left_zw")
    if temp:
        temp = temp[0].find_all(name='p')
    else:
        temp =soup.find_all(name='div', class_="font16Style")
        temp = temp[0].find_all(name='p')
    text_inte = ''
    for temp_ in temp:
        text_part = re.sub(r'\r|\n|\\s|\t| ', '', temp_.get_text())
        text_inte += text_part
    print(text_inte)


def pd_ead():
    csv_path = 'E:/code/pycode/dataming_project/dataminningspider/dataminningspider/url_csv/' + 'it' + '.csv'
    url_list = pd.read_csv(csv_path, usecols=[1], skiprows=0, nrows=10)
    print(url_list.values.tolist())


if __name__ == '__main__':
    get_url()
    #content_get_old('http://www.chinanews.com/jk/hyxw/news/2008/12-30/1509045.shtml')
    # file_handler = open('./hhh/hh.txt','a',encoding='utf-8')
    # file_handler.write('hhhh')
    # file_handler.close()
    # pd_ead()
    # content_get('http://www.chinanews.com/cul/news/2009/07-12/1771647.shtml')
    # content_get('http://www.chinanews.com/gj/oz/news/2008/10-15/1413535.shtml')
    # content_get('http://www.chinanews.com/cj/2020/11-21/9344255.shtml')
