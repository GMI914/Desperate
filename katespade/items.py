# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class KatespadeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    brand = scrapy.Field()
    url = scrapy.Field()
    primary_image = scrapy.Field()
    category = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()
    promo_price = scrapy.Field()
    retailer_site = scrapy.Field()
    crawl_date = scrapy.Field()
    color = scrapy.Field()
