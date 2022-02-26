import datetime

from lxml import html
etree = html.etree

import scrapy
from powang.items import PowangItem


class GithubSpider(scrapy.Spider):
    name = 'github'

    keyword = 'vpn' # 检索关键词
    # 查询的起始页数
    pageNum = 1

    start_urls = ['https://github.com/search?q={keyword}&p={pageNum}'.format(keyword=keyword, pageNum=pageNum)]

    # 通用url模板
    url = 'https://github.com/search?p=%d&q={}'.format(keyword)

    # 解析检索结果页（一级）
    def parse(self, response):

        status_code = response.status  # 状态码

        #========数据解析=========
        page_text = response.text
        tree = etree.HTML(page_text)
        li_list = tree.xpath('//*[@id="js-pjax-container"]/div/div[3]/div/ul/li')
        for li in li_list:
            # 创建item对象
            item = PowangItem()
            # 项目名称
            item_name = li.xpath('.//a[@class="v-align-middle"]/@href')[0].split('/', 1)[1]
            item['item_name'] = item_name
            # 项目链接
            item_link = 'https://github.com' + li.xpath('.//a[@class="v-align-middle"]/@href')[0]
            item['item_link'] = item_link
            # 项目最近更新时间
            item_updated = li.xpath('.//relative-time/@datetime')[0].replace('T', ' ').replace('Z', '')
            item_updated = str(datetime.datetime.strptime(item_updated, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(hours=8))  # 中国时间
            item['item_updated'] = item_updated
            # 项目stars（解决没有star的问题）
            try:
                item_stars = li.xpath('.//a[@class="Link--muted"]/text()')[1].replace('\n', '').replace(' ', '')
                item['item_stars'] = item_stars
            except IndexError:
                item_stars = 0
                item['item_stars'] = item_stars
            else:
                pass
            # 请求传参：meta={}，可以将meta字典传递给请求对应的回调函数
            yield scrapy.Request(item_link, callback=self.items_detail,meta={'item':item})

        # 分页操作
        new_url = format(self.url % self.pageNum)
        print("===================================================")
        print("第" + str(self.pageNum) + "页：" + new_url)
        print("状态码：" + str(status_code))
        print("===================================================")
        self.pageNum += 1
        yield scrapy.Request(new_url, callback=self.parse)

    # 解析项目详情页（二级）
    def items_detail(self, response):

        # 回调函数可以接收item
        item = response.meta['item']

        page_text = response.text
        tree = etree.HTML(page_text)
        # 项目描述
        item_describe = ''.join(tree.xpath('//*[@id="repo-content-pjax-container"]/div/div[3]/div[2]/div/div[1]/div/p//text()')).replace('\n', '').strip().rstrip();
        item['item_describe'] = item_describe

        yield item