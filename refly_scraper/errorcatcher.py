#!/usr/bin/python
#-*-coding:utf-8-*-

import urlparse
from scrapy.http import Request
from scrapy.http import HtmlResponse
from scrapy.utils.response import get_meta_refresh
from scrapy import signals
import csv


class errorHandler(object):
    
    spider_errors = []

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls()
        crawler.signals.connect(ext.spider_error, signal = signals.spider_error)
        crawler.signals.connect(ext.handle_spider_closed, signal = signals.spider_closed)
        return ext

    def spider_error(self, failure, response, spider):
            self.spider_errors.append(failure.getTraceback())

    def handle_spider_closed(self, spider, reason):
        if len(self.spider_errors)>0:
            spider.crawler.stats.set_value('spider_errors', ','.join(self.spider_errors))
