# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PowangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    item_name = scrapy.Field()
    item_link = scrapy.Field()
    item_describe = scrapy.Field()
    item_stars = scrapy.Field()
    item_updated = scrapy.Field()
    pass
