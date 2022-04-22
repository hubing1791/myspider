# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json


class DataminningspiderPipeline(object):
    def process_item(self, item, spider):
        item_json = json.dumps(dict(item), ensure_ascii=False)
        json_file = open('./json/'+item['news_class'] + '.json', 'a+',encoding='utf-8')
        json_file.write(str(item_json)+',\n')
        json_file.close()
