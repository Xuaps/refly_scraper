# -*- coding: utf-8 -*-

# Scrapy settings for refly_scrap project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'refly_scraper'

SPIDER_MODULES = ['refly_spiders']
NEWSPIDER_MODULE = 'refly_spiders'
ITEM_PIPELINES = {'refly_scraper.pipelines.ReflyPipeline': 100}
DOWNLOADER_MIDDLEWARES = {
			   'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
                           'scrapy.contrib.downloadermiddleware.redirect.RedirectMiddleware': None,
                           'refly_scraper.redirect.HandleHttpCodesMiddleware': 100,
}
EXTENSIONS = {
    'refly_scraper.errorcatcher.errorHandler': 100
}
REDIRECT_ENABLED = True
REDIRECT_MAX_TIMES = 20
REDIRECT_PRIORITY_ADJUST = +2
DUPEFILTER_CLASS = 'refly_scraper.customdupefilter.CustomFilter'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'refly_scrap (+http://www.yourdomain.com)'
