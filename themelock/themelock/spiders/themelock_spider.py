from scrapy.spider          import BaseSpider
from scrapy.selector        import Selector
from themelock.items        import ThemelockSpiderItem
from scrapy.http            import Request
import urlparse

class ThemelockSpider(BaseSpider) :
    name            = "themelockspider"
    allowed_domains = ["themelock.com"]
    # start_urls      = ["http://www.themelock.com/wordpress/themeforest-wordpress/"]
    # start_urls      = ["http://www.themelock.com/ecommerce/magento/"]
    # start_urls      = ["http://www.themelock.com/cmstemplates/joomla/"]
    start_urls      = ["http://www.themelock.com/othertemplates/html/"]

    def __init__(self, *args, **kwargs):
        super(ThemelockSpider, self).__init__(*args, **kwargs)
        self.current_product = 1


    def parse(self, response):
        hxs     = Selector(response)
        products  = hxs.xpath("//div[@class='mcontent_inner']")

        for product in products:
                try:
                    item = ThemelockSpiderItem()
                    item["title"]       = product.xpath('.//h2[@class="post-title"]/a/text()').extract()[0]
                    item["content"]     = product.xpath('.//div[@class="article"]/div[1]/div').extract()
                    item["image_url"]   = product.xpath('.//img/@src').extract()[0]

                    #count data
                    print self.current_product
                    self.current_product += 1

                    yield Request(urlparse.urljoin(response.url, product.xpath('.//h2[@class="post-title"]/a/@href').extract()[0]), callback=self.get_product_detail, meta={'item':item})
                    pass
                except Exception, e:
                    pass
        #paging
        paging = hxs.xpath("//div[@class='navigation']/a");
        for index, link in enumerate(paging):
            if 'Next' in link.xpath('text()').extract()[0] :
                yield Request(urlparse.urljoin(response.url, link.xpath('@href').extract()[0]), self.parse)


    def get_product_detail(self, response):
        hxs = Selector(response)
        #item data
        item = response.request.meta['item']
        item["crawled_link"]= response.url

        links = hxs.xpath('//div[@class="quote"]/text()')
        for index, link in enumerate(links):
            if 'upl.me' in link.extract():
                item['download_url'] = link.extract()
        yield item;
