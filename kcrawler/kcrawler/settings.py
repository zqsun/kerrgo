# -*- coding: utf-8 -*-

# Scrapy settings for kcrawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'kcrawler'

SPIDER_MODULES = ['kcrawler.spiders']
NEWSPIDER_MODULE = 'kcrawler.spiders'
USER_AGENT = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
DOWNLOAD_DELAY = 1
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'kcrawler (+http://www.yourdomain.com)'
