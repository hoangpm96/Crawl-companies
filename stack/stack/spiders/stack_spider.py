from scrapy import Spider
from scrapy.selector import Selector

from stack.items import StackItem


class StackSpider(Spider):
    name = "company1"
    allowed_domains = ["diachicongty.net"]
    start_urls = [
        "http://diachicongty.net/page-50001-dia-chi-cong-ty.html",
    ]

    def parse(self, response):
        questions = Selector(response).xpath('//div[@class="news-v3 bg-color-white"]/div')
        for question in questions:
            href = question.xpath('h2/a/@href').extract()[0]
            yield response.follow(href, self.parse_company)
        num_now = int(Selector(response).xpath('//a[@class="page-nav-act active"]/text()').extract_first())
        if num_now < 55000:
            next_page = "http://diachicongty.net/page-" + str(num_now + 1) + "-dia-chi-cong-ty.html"
            yield response.follow(next_page, self.parse)
    def parse_company(self, response):
      phone = Selector(response).xpath('//li[@itemprop="telephone"]/b/font/text()').extract_first()
      # agent = Selector(response).xpath('//li[@itemprop="alumni"]/b/text()').extract_first()
      # address = Selector(response).xpath('//li[@itemprop="location"]/span[@itemprop="name"]/text()').extract_first()
      # name = Selector(response).xpath('//div[@class="alert alert-warning fade in"]/i/strong/text()').extract_first()
      # href_ = Selector(response).xpath('//link[@rel="canonical"]/@href').extract_first()
      item = StackItem()
      if phone is not None:
        item['name'] = Selector(response).xpath('//div[@class="alert alert-warning fade in"]/i/strong/text()').extract_first()
        item['address'] = Selector(response).xpath('//li[@itemprop="location"]/span[@itemprop="name"]/text()').extract_first()
        item['agent'] = Selector(response).xpath('//li[@itemprop="alumni"]/b/text()').extract_first()
        item['phone'] = phone
        item['href_'] = Selector(response).xpath('//link[@rel="canonical"]/@href').extract_first()
        yield item