# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import html2text
import json

class ReflyPipeline(object):
    def process_item(self, item, spider):
    	item['docset'] = spider.name
    	item['type'] = spider.resolveType(item['url'], item['name'])
    	item['parsed_url'] = spider.getSlashUrl(item['path'], item['name'])
    	item['parent'] = item['parsed_url'][0:item['parsed_url'].rfind('/')]
    	item['content'] = html2text.html2text(item['content'])
        return item


#     def close_spider(spider):
#        spider.log('spider closed')
