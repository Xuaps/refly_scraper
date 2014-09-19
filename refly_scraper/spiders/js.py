# -*- coding: utf-8 -*-
import scrapy
import urlparse
import re
from refly_scraper.items import ReferenceItem


class JsSpider(scrapy.Spider):
    name = 'JavaScript'
    excluded_path = ['MDN', 'Web technology for developers']
    allowed_domains = ['mozilla.org']
    start_urls = (
        'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference',
    )

    def parse(self, response):

        reference = ReferenceItem()
        reference['name'] = response.xpath('//h1/text()').extract()[0]
        reference['url'] = response.url
        reference['content'] = response.xpath('//article').extract()[0]
        reference['path'] = [p for p in response.css('.crumbs').xpath('.//a/text()').extract() if p not in self.excluded_path]

        yield reference

        for url in response.xpath('//a[re:test(@href, "^\/en-US\/docs\/Web\/JavaScript\/Reference((?!\\$|#).)*$")]/@href').extract():
              yield scrapy.Request(urlparse.urljoin(response.url, url), callback=self.parse)

    def resolveType(self, url, name):
        if re.search(r'^.*Statements\/((?!\/).)*$',url)!=None:
            return 'statement'
        elif re.search(r'^.*Operators\/((?!\/).)*$',url)!=None:
            return 'expression'
        elif re.search(r'^.*Global_Objects\/.*(?=\/).*$',url)!=None and re.search(r'^.*(?=\)$)',name)!=None:
            return 'method'
        elif re.search(r'^.*Global_Objects\/.*(?=\/).*$',url)!=None and re.search(r'^((?!\().)*$',name)!=None:
            return 'property'
        elif re.search(r'^.*Global_Objects\/((?!\/).)*$',url)!=None and re.search(r'^[A-Z]((?!\().)*$',name)!=None:
            return 'class'
        elif re.search(r'^.*Global_Objects\/((?!\/).)*$',url)!=None and re.search(r'^.*(?=\)$)',name)!=None:
            return 'function'
        elif re.search(r'^.*Global_Objects\/((?!\/).)*$',url)!=None and re.search(r'^[a-z]((?!\().)*$', name)!=None:
            return 'object'
    
        return None;

    def getSlashUrl(self,path, name):
        return '/'+('/'.join(path)+'/'+name).lower()
