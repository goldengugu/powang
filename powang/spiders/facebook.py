import scrapy


class FacebookSpider(scrapy.Spider):
    name = 'facebook'
    allowed_domains = ['www.baidu.com']
    start_urls = ['http://www.baidu.com/']

    def parse(self, response):
        pass
