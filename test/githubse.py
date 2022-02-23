# ！/usr/bin/python3
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import json
import requests
# from PIL import Image
import os
from lxml import html
import time
etree = html.etree


pattern = 0
option = webdriver.ChromeOptions()
# 静默模式启动selenium
if pattern == 1:
    option.add_argument('headless')
    option.add_argument('--window-size=1920,1080')
driver = webdriver.Chrome(options=option)
driver.maximize_window()
wait = WebDriverWait(driver, 10)

# 搜索的关键词
keyword = "vpn"

# 设置一个通用的url模板
url = 'https://github.com/search?p=%d&q={}'.format(keyword)

for pageNum in range(1,3):
    time.sleep(3)
    # 对应页码的url
    new_url = format(url % pageNum)
    print("===================================================")
    print("第" + str(pageNum) + "页：" + new_url)
    print("===================================================")

    driver.get(new_url)
    time.sleep(5)
    for i in range(1,11):
        star = driver.find_element_by_xpath('//*[@id="js-pjax-container"]/div/div[3]/div/ul/li[{}]/div[2]/div[2]/div/div[1]/a'.format(i))
        print(star.text)
    html = driver.execute_script("return document.documentElement.outerHTML")
    tree = etree.HTML(html)
    li_list = tree.xpath('//*[@id="js-pjax-container"]/div/div[3]/div/ul/li')

    for li in li_list:
        print(li)
        name = li.xpath('.//a[@class="v-align-middle"]/@href')[0].split('/',1)[1]
        star = li.xpath('.//div[2]/div[2]/div/div[1]/a/text()')
        print(star)
        link = 'https://github.com' + li.xpath('.//a[@class="v-align-middle"]/@href')[0]
        print("名称：" + name + "\t链接：" + link)



time.sleep(2000)



