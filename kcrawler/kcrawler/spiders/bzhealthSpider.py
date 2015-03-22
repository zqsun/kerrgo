import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
# from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from kcrawler.items import KcrawlerItem

class bzhealthSpider(CrawlSpider):
    name = 'bzhealthSpider'
    allowed_domains = ['bizbuysell.com']
    start_urls = ['http://www.bizbuysell.com/health-care-companies-for-sale/']

    # rules = (
    #     # Extract links matching 'category.php' (but not matching 'subsection.php')
    #     # and follow links from them (since no callback means follow=True by default).
    #     Rule(LinkExtractor(allow=('category\.php', ), deny=('subsection\.php', ))),

    #     # Extract links matching 'item.php' and parse them with the spider's method parse_item
    #     Rule(LinkExtractor(allow=('item\.php', )), callback='parse_item'),
    # )

    rules = (
        Rule(LxmlLinkExtractor(allow=('/health-care-companies-for-sale'),restrict_xpaths=('//div[@class="pagination"]/ul/li/a[@title="Next Page"]')),callback='parse_items',follow=True),
        # Rule(LxmlLinkExtractor(allow=('/health-care-companies-for-sale')),callback='parse_item'),
    )

    def parse_items(self, response):
        sel = Selector(response)
        lists = sel.xpath('//a[contains(@id,"List") and not(contains(@id,"ListNumber"))]')
        items = []

        for li in lists:
            item = KcrawlerItem()
            item['source'] = u'bizbuysell'
            item['title'] = li.xpath('span[2]/b[@class="title"]/text()').extract()
            item['link'] = li.xpath('@href').extract()
            location = li.xpath('string(span[2]/p[@class="info"])').extract()
            location[0] = location[0].strip(' \t\n\r')
            # item['location'] = li.xpath('span[2]/p[@class="info"]/text()').extract()
            item['location'] = location
            # if(item['location']==[]):
            #     # location = 
            #     # location[0] = location[0].strip(' \t\n\r')
            #     item['location'] = li.xpath('span[2]/p[@class="info"]/text()').extract()
            item['desc'] = li.xpath('span[2]/p[@class="desc"]/text()').extract()

            # item['url'] = li.xpath('a/@href').extract()
            # item['description'] = li.xpath('text()').re('-\s[^\n]*\\r')
            items.append(item)
            print item ['title']

        return items