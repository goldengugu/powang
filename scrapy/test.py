import scrapy


class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['www.xxx.com']
    start_urls = ['http://www.xxx.com/']

    def parse(self, response):
        pass
