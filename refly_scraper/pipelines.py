# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import html2text as html2text_orig
import re

class ReflyPipeline(object):
    link_re = re.compile(r"\[\d*\]: (?:[\.:?=/\w \-#]|(?:\n))*", re.MULTILINE)

    def process_item(self, item, spider):
    	item['docset'] = spider.name
    	item['type'] = spider.resolveType(item['url'], item['name'])
    	item['parsed_url'] = spider.getSlashUrl(item['path'], item['name'])
    	item['parent'] = item['parsed_url'][0:item['parsed_url'].rfind('/')]
    	item['content'] = self.html2text(item['content'])
        return item

    def html2text(self, html):
        """use html2text but repair newlines cutting urls"""
        h = html2text_orig.HTML2Text()
        h.inline_links = False
        txt = h.handle(html).replace('`[', '[`')
        
        for l in self.link_re.findall(txt):
            txt=txt.replace(l, l.replace('\n',''))
    
        return txt
