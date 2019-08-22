from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Compose
from .items import KatespadeItem
import re


class Strip:
    def __call__(self, values):
        if isinstance(values, str):
            return values.strip()
        if isinstance(values, list):
            result = ''
            for value in values:
                result += value.strip()
            return result
        return values


class PriceLoader:
    def __call__(self, value):
        return re.search(r"[\d\.?]+", value).group(0)


class ProductLoader(ItemLoader):
    default_item_class = KatespadeItem
    default_output_processor = TakeFirst()
    title_out = Strip()
    description_out = Strip()
    price_out = Compose(TakeFirst(), PriceLoader())
    promo_price_out = Compose(TakeFirst(), PriceLoader())
    category_out = Compose(TakeFirst(), lambda value: ' '.join(value.split('-')[1:]))
