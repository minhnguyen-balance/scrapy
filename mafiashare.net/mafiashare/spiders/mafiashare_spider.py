from scrapy.spider          import BaseSpider
from scrapy.selector        import Selector
from mafiashare.items       import MafiashareSpiderItem
from scrapy.http            import Request
import urlparse

class ThemelockSpider(BaseSpider) :
    name            = "mafiasharespider"
    allowed_domains = ["mafiashare.net"]
    # start_urls      = ["http://www.themelock.com/wordpress/themeforest-wordpress/"]
    # start_urls      = ["http://www.themelock.com/ecommerce/magento/"]
    # start_urls      = ["http://www.themelock.com/cmstemplates/joomla/"]
    start_urls      = ["http://www.mafiashare.net/cat/wordpress/"]

    def __init__(self, *args, **kwargs):
        super(ThemelockSpider, self).__init__(*args, **kwargs)
        self.current_product = 1


    def parse(self, response):
        hxs     = Selector(response)
        products  = hxs.css("div.post_list")

        for product in products:
                print product.xpath('.//h4/a/text()').extract()[0]
                try:
                    item = MafiashareSpiderItem()
                    item["title"]       = product.xpath('.//h4/a/text()').extract()[0]

                    #count data
                    print self.current_product
                    self.current_product += 1

                    yield Request(urlparse.urljoin(response.url, product.xpath('.//h4/a/@href').extract()[0]), callback=self.get_product_detail, meta={'item':item})
                    pass
                except Exception, e:
                    pass
        #paging
        link_next = hxs.xpath("//a[@class='pagination-next']/@href").extract()
        if(len(link_next)>0):
            yield Request(urlparse.urljoin(response.url, link_next[0]), self.parse)


    def get_product_detail(self, response):
        hxs = Selector(response)
        #item data
        item = response.request.meta['item']
        item["crawled_link"]= response.url
        item["image_url"] = hxs.xpath('//img[@itemprop="image"]/@src').extract()[0]
        item["content"] = hxs.xpath('//div[@itemprop="description"]').extract()[0]
        item['link_demo'] = self.get_link_with_content(hxs, 'Live Demo')
        item['download_url'] = hxs.xpath('//code[@class="select"]/text()').extract()[0]

        links = hxs.xpath('//div[@class="quote"]/text()')
        for index, link in enumerate(links):
            if 'upl.me' in link.extract():
                item['download_url'] = link.extract()
        yield item;

    def get_link_with_content(self, maincontent, content):
        links = maincontent.xpath('//a')
        for link in links:

            if len(link.xpath('text()'))>0 and (content in link.xpath('text()').extract()[0]):
                return link.xpath('@href').extract()[0]
        return ''
