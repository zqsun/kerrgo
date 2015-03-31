import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
# from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from kcrawler.items import KcrawlerItem

class mnSpider(CrawlSpider):
    name = 'mnSpider'
    allowed_domains = ['mergernetwork.com']
    start_urls = [
                'http://www.mergernetwork.com/index.cfm/fuseaction/browseBFS.search/index.htm?isSubmitted=true&method=SearchBar&resetSearch=true&bc_label=Quick+Search&bc_url=%2Fbuy-a-business-for-sale&indID=14',
                # 'http://www.mergernetwork.com/index.cfm/fuseaction/browseBFS.search/index.htm?isSubmitted=true&method=SearchBar&resetSearch=true&bc_label=Quick+Search&bc_url=%2Fbuy-a-business-for-sale&indID=8'
    ]

    # rules = (
    #     # Extract links matching 'category.php' (but not matching 'subsection.php')
    #     # and follow links from them (since no callback means follow=True by default).
    #     Rule(LinkExtractor(allow=('category\.php', ), deny=('subsection\.php', ))),

    #     # Extract links matching 'item.php' and parse them with the spider's method parse_item
    #     Rule(LinkExtractor(allow=('item\.php', )), callback='parse_item'),
    # )

    rules = (
        Rule(LxmlLinkExtractor(allow=(''),restrict_xpaths=('//div[@id="nextprev" and @class="noprint"]/table/tr/td[3]/a')),callback='parse_start_url',follow=True),
        # Rule(LxmlLinkExtractor(allow=('/health-care-companies-for-sale')),callback='parse_item'),
    )

    def parse_start_url(self, response):
        sel = Selector(response)
        lists = sel.xpath('//div[contains(@id,"listingInfo")]')
        items = []
        # category = self.category_det(response.url)
        # print response.url
        for li in lists:
            item = KcrawlerItem()
            item['source'] = 'mergernetwork'
            item['title'] = li.xpath('h3/a/text()').extract()
            # link = li.xpath('h3/a/@href').extract()
            # link[0] = link[0][0:link[0].index('/?d=')] #remove the tails of link
            item['link'] = li.xpath('h3/a/@href').extract()
            industry = li.xpath('dl/dd[1]/text()').extract()
            item['category'] = self.category_det(industry[0])
            # location = li.xpath('dl/dd[2]/text()').extract()
            # location[0] = location[0].strip(' \t\n\r') #remove space, /r,/n
            item['location'] = li.xpath('dl/dd[2]/text()').extract()
            item['desc'] = li.xpath('p/text()').extract()
            # item['category'] = category
            items.append(item)
            # print item ['title']

        return items

    # Determine the category based on the industry tag
    def category_det(dummy,tag):
        if ('Health Care' in tag):
            return 'health'.encode(encoding='UTF-8',errors='strict')
        elif('Agriculture' in tag):
            return 'agriculture'.encode(encoding='UTF-8',errors='strict')

