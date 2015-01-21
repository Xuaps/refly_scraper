#!/usr/bin/python
#-*-coding:utf-8-*-

import urlparse
from scrapy.http import Request
from scrapy.exceptions import CloseSpider
from scrapy.http import HtmlResponse
from scrapy.utils.response import get_meta_refresh
import csv


class reflyScraperMiddleware(object):
    

    def __init__(self):
        self.errors404 = []

    def process_request(self, request, spider):
        return None 



    def process_response(self, request, response, spider):
        if response.status in [404]:
            self.errors404.append(response.url)
            self.log_errors([unicode('404'),urlparse.urlparse(response.url).path,''])
            #raise CloseSpider('Page not found')
        return response

    def log_errors(self, item):
        with open('urlerrors.csv', 'a') as csvfile:
            rowwriter = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
            rowwriter.writerow(item)
