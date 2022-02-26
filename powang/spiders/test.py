import scrapy


class TestSpider(scrapy.Spider):
    name = 'test'
    start_urls = ['https://www.baidu.com/s?wd=ip']

    def parse(self, response):
        page_text = response.text

        with open('./ip.html','w',encoding='utf-8') as fp:
            fp.write(page_text)
