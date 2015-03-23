import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
# from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from kcrawler.items import KcrawlerItem

class bzmulticatsSpider(CrawlSpider):
    name = 'bzmulticatsSpider'
    allowed_domains = ['bizbuysell.com']
    start_urls = ['http://www.bizbuysell.com/health-care-companies-for-sale/',
                'http://www.bizbuysell.com/agriculture-businesses-for-sale/'
    ]

    # rules = (
    #     # Extract links matching 'category.php' (but not matching 'subsection.php')
    #     # and follow links from them (since no callback means follow=True by default).
    #     Rule(LinkExtractor(allow=('category\.php', ), deny=('subsection\.php', ))),

    #     # Extract links matching 'item.php' and parse them with the spider's method parse_item
    #     Rule(LinkExtractor(allow=('item\.php', )), callback='parse_item'),
    # )

    rules = (
        Rule(LxmlLinkExtractor(allow=(''),restrict_xpaths=('//div[@class="pagination"]/ul/li/a[@title="Next Page"]')),callback='parse_start_url',follow=True),
        # Rule(LxmlLinkExtractor(allow=('/health-care-companies-for-sale')),callback='parse_item'),
    )

    def parse_start_url(self, response):
        sel = Selector(response)
        lists = sel.xpath('//a[contains(@id,"List") and not(contains(@id,"ListNumber"))]')
        items = []
        category = self.category_det(response.url)
        # print response.url
        for li in lists:
            item = KcrawlerItem()
            item['source'] = u'bizbuysell'
            item['title'] = li.xpath('span[2]/b[@class="title"]/text()').extract()
            link = li.xpath('@href').extract()
            link[0] = link[0][0:link[0].index('/?d=')] #remove the tails of link
            item['link'] = link
            location = li.xpath('string(span[2]/p[@class="info"])').extract()
            location[0] = location[0].strip(' \t\n\r') #remove space, /r,/n
            item['location'] = location
            item['desc'] = li.xpath('span[2]/p[@class="desc"]/text()').extract()
            item['category'] = category
            items.append(item)
            # print item ['title']

        return items

    # Determine the category based on the response's url
    def category_det(dummy,url):
        if ('health-care' in url):
            return u'health'
        elif('agriculture' in url):
            return u'agriculture'

