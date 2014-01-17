from scrapy.spider          import BaseSpider
from scrapy.selector        import Selector
from australia_wine.items   import AustraliaWineItem
from scrapy.http            import Request
import urlparse

class WineSpider(BaseSpider) :
    name            = "winespider"
    allowed_domains = ["nicks.com.au"]
    start_urls      = ["http://www.nicks.com.au/store/australian-wines/"]

    def __init__(self, *args, **kwargs):
        super(WineSpider, self).__init__(*args, **kwargs)
        self.current_product = 1
        from scrapy.conf import settings
        #get job_id parameter
        import os, sys
        print sys.argv

        if (len(sys.argv)>2):
            if ('_job' in sys.argv[3]):
                self.jobid = sys.argv[3].rsplit('=')[1]

        settings.overrides['FEED_URI'] ="/var/lib/scrapyd/items/australia_wine/%(name)s/"+self.jobid+".csv"
        settings.overrides['DOWNLOAD_TIMEOUT'] = 360


    def parse(self, response):
        hxs     = Selector(response)
        ul_products  = hxs.xpath('//div[@class="category-products"]/ul')

        for ul_product in ul_products:
            for li_product in ul_product.xpath('li'):
                try:
                    item = AustraliaWineItem()
                    item["name"]        = li_product.xpath('h5[@class="product-name"]/a/text()').extract()
                    item["price"]       = li_product.xpath('.//span[@class="regular-price"]/span[@class="dollars"]/text()').extract()[0] + \
                                            li_product.xpath('.//span[@class="regular-price"]/span[@class="cents"]/text()').extract()[0]
                    item["image_url"]   = li_product.xpath('div[@class="grid-view-image"]/a/img/@src').extract()
                    #link product detail
                    link = li_product.xpath('h5[@class="product-name"]/a/@href').extract()

                    #show current page
                    #print self.current_product
                    #self.current_product += 1

                    yield Request(urlparse.urljoin(response.url, link[0]), callback=self.get_product_detail, meta={'item':item})
                    pass
                except Exception, e:
                    pass
        #check if have next page
        next_page = hxs.select("//a[@class='next i-next']/@href").extract()[0]
        if next_page:
            yield Request(urlparse.urljoin(response.url, next_page), self.parse)

    def get_product_detail(self, response):
        hxs = Selector(response)
        item = response.request.meta['item']
        product_info = hxs.xpath('//div[@class="span9 product-info"]')

        item['description'] = product_info.xpath('.//div[@class="std span12"]/p/text()').extract()
        yield item;
