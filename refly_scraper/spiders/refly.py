# -*- coding: utf-8 -*-
import scrapy
import urlparse
from scrapely import Scraper
from scrapely.htmlpage import HtmlPage
from w3lib.encoding import html_to_unicode
from refly_scraper.items import ReferenceItem


class ReflySpider(scrapy.Spider):
    name = "refly"
    allowed_domains = ["mozilla.org"]
    start_urls = (
        'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference',
    )
    scraper = Scraper.fromfile(open('javascript.json'))

    def parse(self, response):
        items = self.scraper.scrape_page(HtmlPage(url=response.url, headers=response.headers, body=response.body_as_unicode()))

        reference = ReferenceItem()
        reference['name'] = items[0]['name']
        reference['url'] = response.url
        reference['content'] = items[0]['content']
        reference['path'] = items[0]['path']

        yield reference

        for url in response.xpath('//a/@href').extract():
              yield scrapy.Request(urlparse.urljoin(response.url, url), callback=self.parse)
