import scrapy
from scrapy import Request, Spider
from selenium import webdriver
import time
from lxml import html

etree = html.etree

class TwitterSpider(scrapy.Spider):
    name = 'twitter'
    url_templat = "https://twitter.com/search?q={}&src=typed_query&f=user"
    keywords = ['vpn']

    def __init__(self):
        ChromeOptions = webdriver.ChromeOptions()
        ChromeOptions.add_argument("--proxy-server=http://127.0.0.1:1087")
        ChromeOptions.add_argument('headless')

        # 访问twitter
        self.browser = webdriver.Chrome(options=ChromeOptions)
        self.counter = 0

    def start_requests(self):
        for i in self.keywords:
            url = self.url_templat.format(i)
            self.browser.get(url)
            time.sleep(4)
            yield Request(url=url, callback=self.parse, meta={'mode': 'scroll'})

    def parse(self, response):
        if self.counter < 2:
            text = etree.HTML(response.body)

            urls = text.xpath(
                "//*[@class='css-4rbku5 css-18t94o4 css-1dbjc4n r-1loqt21 r-1wbh5a2 r-dnmrzs r-1ny4l3l']/@href")
            print(urls)
            self.counter += 1
            # time.sleep(2)
            yield Request(url='https://twitter.com/', callback=self.parse, dont_filter=True, meta={'mode': 'scroll'})

            for l in range(len(urls)):
                user_url = response.urljoin(urls[l])
                print(user_url)
                yield Request(url=user_url, callback=self.parse_usersdata, meta={'mode': 'access'})

        pass

    def parse_usersdata(self, response):
        print("------------------------------------")
        text = etree.HTML(response.body)
        # 设置各种xpath：
        xpath_name='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[1]/div/span[1]/span/text()'
        xpath_des='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div/div/div[3]/div/div/span/text()'
        xpath_place='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div/div/div[4]/div/span[1]/span/span/text()'
        xpath_ipaddress='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div/div/div[4]/div/a/span/text()'
        xpath_date='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div/div/div[4]/div/span[2]/span/text()'
        xpath_following='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div/div/div[5]/div[1]/a/span[1]/span/text()'
        xpath_followers='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div/div/div[5]/div[2]/a/span[1]/span/text()'
        xpath_imgurl='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/div[1]/div[2]/div/div[2]/div/a/@href'
        xpath_tweets='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[1]/div[1]/div/div/div/div/div[2]/div/div/text()'

        name=text.xpath(xpath_name)
        des=text.xpath(xpath_des)
        place=text.xpath(xpath_place)
        ipaddress=text.xpath(xpath_ipaddress)
        date=text.xpath(xpath_date)
        following=text.xpath(xpath_following)
        followers=text.xpath(xpath_followers)
        tweets=text.xpath(xpath_tweets)
        imgurl=text.xpath(xpath_imgurl)

        print(name,des,place,ipaddress,date,following,followers,tweets,imgurl)
        pass
