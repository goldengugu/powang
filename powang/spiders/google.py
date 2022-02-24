import scrapy


class GoogleSpider(scrapy.Spider):
    name = 'google'
    allowed_domains = ['google']
    start_urls = ['http://google/']

    def parse(self, response):
        pass
