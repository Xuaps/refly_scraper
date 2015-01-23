# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import html2text as html2text_orig
import re
import psycopg2
import sys
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

class ReflyPipeline(object):
    table_re = re.compile("<table((.|\n)*?)<\/table>")
    link_re = re.compile("( *\[\d*\]: (?:[\.:?=/\w\-@#~,\.; \(\)%]|(?:\\n))*)")
    title = re.compile("(title=(?:\"[^\"]*\"|'[^']*'))")
    connection_string = "host='localhost' dbname='slashdb' user='postgres'"
    def __init__(self):
        self.connection = psycopg2.connect(self.connection_string)
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def process_item(self, item, spider):
        item['docset'] = spider.name
        if type not in item:
            item['type'] = spider.resolveType(item['url'], item['name'])
        item['parent'] = spider.getSlashUrl(item['path'], '')
        item['type'] = spider.resolveType(item['url'], item['name'])
        item['parsed_url'] = spider.getSlashUrl(item['path'], item['alias'])
        item['content'] = self.html2text(item['content'])
        self.sendToDB(item)
        return item

    def html2text(self, html):
        """use html2text but repair newlines cutting urls and fix errors in links with code inside"""
        html = self.title.sub('', html)
        html = self.fixTables(html)
        h = html2text_orig.HTML2Text()
        h.body_width = 0

        h.inline_links = False
        txt = h.handle(html).replace('`[', '[`')


        return self.fixhtml2texterrors(self.removeBadChars(txt))

    def removeBadChars(self, content):
        return content.replace('\u2026', '...').replace('\u00a0',' ')

    def fixhtml2texterrors(self, txt):
        txt = re.sub('\[`(.*)\]\[(\d)\]`','[`\\1`][\\2])',txt).replace('\n>\n','')
        return txt

    def fixTables(self, txt):
        txt = txt.replace('<br>', ' ').replace('<br/>', ' ')
        for table in self.table_re.findall(txt):
            txt = txt.replace(table[0], table[0].replace('\n', ' '))
        return txt

    def sendToDB(self, item):
        pgcursor = self.connection.cursor()
        sqlinsertitem = "INSERT INTO temp_refs (reference, content, uri, parent, type, docset) VALUES (%s, %s, %s, %s, %s, %s)"
        pgcursor.execute(sqlinsertitem,[item['name'], item['content'], item['url'], item['parent'], item['type'], item['docset']])

    def spider_closed(self, spider):
        self.connection.commit()
