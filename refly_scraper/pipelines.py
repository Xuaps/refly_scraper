# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import html2text as html2text_orig
import re
import codecs

class ReflyPipeline(object):
    link_re = re.compile("( *\[\d*\]: (?:[\.:?=/\w\-#~,\.; \(\)%]|(?:\\n))*)")
    title = re.compile("(title=(?:\"[^\"]*\"|'[^']*'))")

    def process_item(self, item, spider):
        item['docset'] = spider.name
        if type not in item:
          item['type'] = spider.resolveType(item['url'], item['name'])
        item['parsed_url'] = spider.getSlashUrl(item['path'], item['alias'])
        item['parent'] = spider.getSlashUrl(item['path'], '')

        item['content'] = self.html2text(item['content'].replace(u'\u00a0', u' '))
        return item

    def html2text(self, html):
        """use html2text but repair newlines cutting urls and fix errors in links with code inside"""
        html = self.title.sub('', html)
        h = html2text_orig.HTML2Text()
        h.inline_links = False
        h.bypass_tables = True
        txt = h.handle(html).replace('`[', '[`')

        for l in self.link_re.findall(txt):
            txt = txt.replace(l, l.replace('\n', '').strip() + '\n\n')

        return txt
