# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class MafiashareSpiderItem(Item):
    title       = Field()
    image_url   = Field()
    content     = Field()
    link_demo   = Field()
    download_url= Field()
    crawled_link= Field()

    pass
