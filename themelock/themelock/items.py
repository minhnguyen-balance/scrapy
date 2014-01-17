# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class ThemelockSpiderItem(Item):
    title       = Field()
    image_url   = Field()
    content     = Field()
    download_url= Field()
    crawled_link= Field()

    pass
