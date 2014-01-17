# Scrapy settings for australia_wine project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'australia_wine'

SPIDER_MODULES      = ['australia_wine.spiders']
NEWSPIDER_MODULE    = 'australia_wine.spiders'
FEED_FORMAT         = "csv"
FEED_STORE_EMPTY    = True
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'australia_wine (+http://www.yourdomain.com)'
