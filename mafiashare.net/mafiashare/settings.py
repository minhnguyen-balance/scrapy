# Scrapy settings for themelock project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'mafiashare'

SPIDER_MODULES = ['mafiashare.spiders']
NEWSPIDER_MODULE = 'mafiashare.spiders'
DEFAULT_ITEM_CLASS = 'mafiashare.items.MafiashareSpiderItem'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'themelock (+http://www.yourdomain.com)'
