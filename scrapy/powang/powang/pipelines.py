# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import csv
import os

from itemadapter import ItemAdapter


class PowangPipeline:

    file = None # 文件

    def open_spider(self,spider):

        # 文件保存路径
        path = './data'

        isExist = os.path.exists(path)
        if not isExist:
            os.makedirs(path)

        print("开始爬取并写入文件....")
        self.file = open(path + '/github.csv','a', encoding='utf_8_sig', newline="")

    # 用于处理item类型对象
    # 该方法可以接收爬虫文件提交过来的item对象
    # 该方法每接收一个item就会被调用一次
    def process_item(self, item, spider):
        item_name = item['item_name']
        item_link = item['item_link']
        item_describe = item['item_describe']
        item_stars = item['item_stars']
        item_updated = item['item_updated']
        fieldnames = ['item_name', 'item_link', 'item_describe', 'item_stars', 'item_updated']
        w = csv.DictWriter(self.file, fieldnames=fieldnames)
        w.writerow(item)
        return item

    def close_spider(self,spider):
        print('爬取结束....')
        self.file.close()