# -*- coding: utf-8 -*-
import scrapy


class ExampleSpider(scrapy.Spider):
    name = 'spider'
    allowed_domains = ['icaew.com']
    start_urls = ['https://find.icaew.com/search?term=london#results']

    def parse(self, response):
        urls = response.xpath('//a[@class="card-link"]/@href').extract()
        for url in urls:
            full_url = response.urljoin(url)
            yield scrapy.Request(full_url, callback=self.individual_page)
        # Calling next page
        next_page_url = response.xpath('//ul[@class="pagination"]/li[last()]/a/@href').extract_first()
        yield scrapy.Request(response.urljoin(next_page_url), callback=self.parse)

    def individual_page(self, response):
        fields = dict()
        fields["url"] = response.url
        fields["name"] = response.xpath('//h1/text()').extract_first().strip()
        fields["address"] = response.xpath('//dl[@class="title-list"]/dd[1]/text()').extract_first()
        fields["phone"] = response.xpath('//dl[@class="title-list"]/dd[2]//text()').extract_first()
        fields["website"] = response.xpath('//dl[@class="title-list"]/dd[3]/p/a/@href').extract_first()

        yield fields