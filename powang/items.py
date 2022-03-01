# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PowangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass



class GithubItem(scrapy.Item):
    # project's name
    name = scrapy.Field()

    link = scrapy.Field()

    star = scrapy.Field()

class GoogleItem(scrapy.Item):

    title = scrapy.Field()
    rawurl = scrapy.Field()
    url = scrapy.Field()
