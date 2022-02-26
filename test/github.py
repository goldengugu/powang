import re
from urllib import request

import requests
from lxml import html
import time

etree = html.etree

if __name__ == '__main__':

    # 需要设置UA
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
        # 'Authorization': 'token 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',
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }
    proxies = {
        "http" : "http://127.0.0.1:1087",
        "https": "http://127.0.0.1:1087"
    }


    # 搜索的关键词
    keyword = "梯子"

    # 设置一个通用的url模板
    url = 'https://github.com/search?p=%d&q={}'.format(keyword)

    # 查询的页数（左闭右开区间）
    for pageNum in range(1,11):
        time.sleep(3)
        # 对应页码的url
        new_url = format(url%pageNum)
        print("===================================================")
        print("第" + str(pageNum) + "页：" + new_url)
        print("===================================================")

        # 使用通用爬虫对url对应的一整张页面进行爬取
        response = requests.get(url=new_url, headers=headers,proxies = proxies)
        # print(response.headers.)
        print(response.status_code)
        page_text = response.text
        tree = etree.HTML(page_text)
        li_list = tree.xpath('//*[@id="js-pjax-container"]/div/div[3]/div/ul/li')

        for li in li_list:
            name = li.xpath('.//a[@class="v-align-middle"]/@href')[0].split('/',1)[1]
            link = 'https://github.com' + li.xpath('.//a[@class="v-align-middle"]/@href')[0]
            print("名称：" + name + "\t链接：" + link)
