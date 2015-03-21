from scrapy.spider import Spider
from scrapy.selector import Selector

from kcrawler.items import KcrawlerItem


class bzsingleSpider(Spider):
    name = "bzsinglePage"
    allowed_domains = ["bizbuysell.com"]
    start_urls = [
        "http://www.bizbuysell.com/businesses-for-sale/?q=/wEFC2lyPTEmc3BpZD0z"
    ]

    def parse(self, response):
        """
        The lines below is a spider contract. For more info see:
        http://doc.scrapy.org/en/latest/topics/contracts.html
        @url http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/
        @scrapes name
        """
        sel = Selector(response)
        lists = sel.xpath('//a[contains(@id,"List") and not(contains(@id,"ListNumber"))]')
        items = []

        for li in lists:
            item = KcrawlerItem()
            item['title'] = li.xpath('span[2]/b[@class="title"]/text()').extract()
            item['link'] = li.xpath('@href').extract()
            item['source'] = 'bizbuysell'
            # item['url'] = li.xpath('a/@href').extract()
            # item['description'] = li.xpath('text()').re('-\s[^\n]*\\r')
            items.append(item)
            print item

        return items