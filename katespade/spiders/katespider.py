import json

from scrapy import Spider
import scrapy
from ..loader import ProductLoader
import datetime


class KateSpider(Spider):
    name = "katespider"

    start_urls = ["https://www.katespade.com/"]

    def parse(self, response):
        links = response.xpath(
            "//ul[@class='menu-category']/ul[@class='menu-category level-1 ']//li/a[@class='has-sub-menu expand']/@href"
        ).extract()
        print("1")
        print(links)
        for link in links:
            yield scrapy.Request(url=link, callback=self.item_link_parse)

    def item_link_parse(self, response):
        items_links = response.xpath(
            "//ul[@class='search-result-items tiles-container hide-compare ']//li[@class='grid-tile ']/div/div["
            "@class='product-name ']/h2/a/@href "
        ).extract()
        for item_link in items_links:
            yield scrapy.Request(url="https://www.katespade.com" + item_link, callback=self.item_parse)

    def item_parse(self, response):
        item = ProductLoader(response=response)

        item.add_xpath("title", "//div[@id='product-content']/h1[@class='product-name']/text()")
        item.add_value("brand", "kate spade")
        item.add_value("url", response.url)
        item.add_xpath("primary_image", "//a[@class='thumbnail-link']/@href")
        loop_info = response.xpath("//script[contains(text(), 'var loopInfo')]/text()").re_first(r'{.*}')
        loop_info = json.loads(loop_info)
        item.add_value("category", loop_info.get('category', ''))
        item.add_xpath("description", "//div[@id='small-details']/text()")
        price = response.xpath("//span[@class='price-standard']/text()").get()
        promo_price = response.xpath("//span[@class='price-sales']/text()").get()
        if not price:
            price, promo_price = promo_price, price
        item.add_value("price", price)
        item.add_value("promo_price", promo_price)
        item.add_value("retailer_site", "https://www.katespade.com/")
        item.add_value("crawl_date", datetime.datetime.now())
        item.add_xpath("color",
                       "//ul[@class='swatches Color clearfix']/li[@class='selected']/span[@class='title']/text()")

        return item.load_item()
