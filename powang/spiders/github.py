from scrapy import Request,Spider
import scrapy
from scrapy import Selector
from lxml import html
from powang.items import GithubItem
import time
etree = html.etree


class GithubSpider(scrapy.Spider):
    name = 'github'
    allowed_domains = ['github.com']
    # https://github.com/search?q=vpn&p=1
    urls = 'https://github.com/search?q=vpn&p={}'

    def start_requests(self):
        for pageNum in range(10):
            # time.sleep(5)

            yield Request(self.urls.format(pageNum),callback=self.parse,meta={'proxy':"http://127.0.0.1:1087"})

    def parse(self, response):


        page_text = response.text
        tree = etree.HTML(page_text)
        li_list = tree.xpath('//*[@id="js-pjax-container"]/div/div[3]/div/ul/li')
        for li in li_list:
            github_item = GithubItem()
            github_item['name'] = li.xpath('.//a[@class="v-align-middle"]/@href')[0].split('/', 1)[1]
            github_item['link'] = 'https://github.com' + li.xpath('.//a[@class="v-align-middle"]/@href')[0]
            # 解决没有star的问题
            try:
                github_item['star'] = li.xpath('.//a[@class="Link--muted"]/text()')[1].replace('\n', '').replace(' ', '')
            except IndexError:
                github_item['star'] = 0

            yield github_item
        #
        # selector = Selector(text=page_text)
        # next = selector.xpath('/html/body/div[4]/main/div/div[3]/div/div[2]/div/a[8]/@href')
        # url = response.urljion(next)
        # yield Request(url=url,callback=self.parse,meta={'proxy':"http://127.0.0.1:1087"})


