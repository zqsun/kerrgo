import scrapy
from scrapy.spider import Spider  
from scrapy.http import Request  
from scrapy.selector import Selector
from kcrawler.items import KcrawlerItem

class mnSpider(Spider):
    name = 'mnSpider_ex'
    allowed_domains = ['mergernetwork.com']
    start_urls = [
                'http://www.mergernetwork.com/index.cfm/fuseaction/browseBFS.search/index.htm?isSubmitted=true&method=SearchBar&resetSearch=true&bc_label=Quick+Search&bc_url=%2Fbuy-a-business-for-sale&indID=14', #health
                # 'http://www.mergernetwork.com/index.cfm/fuseaction/browseBFS.search/index.htm?isSubmitted=true&method=SearchBar&resetSearch=true&bc_label=Quick+Search&bc_url=%2Fbuy-a-business-for-sale&indID=8'   #Argricuture
    ]


    def parse(self, response):
        sel = Selector(response)
        lists = sel.xpath('//div[contains(@id,"listingInfo")]')
        # items = []
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
            # items.append(item)
            # print item ['title']
            yield item

        url = sel.xpath('string(//div[@id="nextprev" and @class="noprint"]/table/tr/td[3]/a/@href)').extract()
        url = "http://www.mergernetwork.com" + url[0]
        print url
        yield scrapy.Request(url, callback=self.parse)

        # return items

    # Determine the category based on the industry tag
    def category_det(dummy,tag):
        if ('Health Care' in tag):
            return 'health'.encode(encoding='UTF-8',errors='strict')
        elif('Agriculture' in tag):
            return 'agriculture'.encode(encoding='UTF-8',errors='strict')

