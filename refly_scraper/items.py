# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ReferenceItem(scrapy.Item):
  name = scrapy.Field()
  alias = scrapy.Field()
  content = scrapy.Field()
  path = scrapy.Field()
  url = scrapy.Field()

  docset = scrapy.Field()
  type =scrapy.Field()
  parsed_url = scrapy.Field()
  parent = scrapy.Field()
