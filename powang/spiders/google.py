from scrapy import Request, Spider
import scrapy
from scrapy import Selector
from lxml import html
import time
from powang.items import GoogleItem

etree = html.etree
import random


class GoogleSpider(scrapy.Spider):
    name = 'google'
    # 搜索参数
    # hl : 语言设置，如（cn,en）
    #
    # https://www.google.com/search?gbv=1&q=vpn&oq=&aqs=&hl=cn
    #
    url = 'https://{}/search?q={}&gbv=1&sei=1hcfYs2gOYykoAT0tbGADQ&hl='
    #
    keywords = ["vpn", "翻墙"]

    def start_requests(self):
        for word in self.keywords:
            domain = random.choice(self.random_admin())
            # time.sleep(5)
            url = self.url.format(domain, word)
            print(url)
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        # print("状态码：",response.status)
        # print(response.headers)

        page_text = response.text
        tree = etree.HTML(page_text)

        divs = tree.xpath('//div[@class="v5yQqb jqWpsc"]')
        for div in divs:
            # div = divs[i]
            # rawurl = response.urljoin(str(div.xpath('./a/@href'))[0])
            rawurl = div.xpath('./a/@href')[0]
            title = div.xpath('./a/div[1]/span/text()')[0]
            print(title, rawurl)
            yield Request(rawurl, callback=self.parse_url, meta={'title': title, 'rawurl': rawurl})

        divs = tree.xpath('//div[@class="egMi0 kCrYT"]')
        for div in divs:
            # rawurl = response.urljoin(str(div.xpath('./a/@href'))[0])
            rawurl = "https://www.google.com" + div.xpath('./a/@href')[0]
            title = div.xpath('./a/h3/div/text()')[0]
            print(title, rawurl)
            yield Request(rawurl, callback=self.parse_url, meta={'title': title, 'rawurl': rawurl})

        pass

    # response.headers
    def parse_url(self, response):
        item = GoogleItem()

        item['title'] = response.meta['title']
        item['rawurl'] = response.meta['rawurl']
        item['url'] = response.url
        print(item['url'])
        # yield item
        pass

    def random_admin(self):
        text_list = []
        with open("powang/data/google_domins.txt", encoding="utf-8") as fp:
            for line in fp:
                line = line.replace("\n", "").strip()
                if line:
                    text_list.append(line)

        return text_list
