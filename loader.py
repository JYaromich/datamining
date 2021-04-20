from scrapy.loader import ItemLoader
from scrapy.selector import Selector
from itemloaders.processors import Identity, MapCompose, TakeFirst

def _get_flat_params(text):
    selector = Selector(text=text)
    value = ''.join(selector.xpath('//li/text()').extract()).strip()
    return {
        selector.xpath('//li/span/text()').extract_first().strip()[:-1]: value
    }

def _get_phone_number(text):
    selector = Selector(text=text)
    id_client = selector.re('"itemID":[\d]{1,}')[0].split(':')[-1]
    link = f'https://www.avito.ru/web/1/items/phone/{id_client}'


class AvitoFlatLoader(ItemLoader):
    default_item_class = dict
    default_output_processor = TakeFirst()

    title_in = MapCompose(lambda text: text.replace('\xa0', ' '))
    address_in = MapCompose(lambda text: text.strip())
    flat_params_in = MapCompose(_get_flat_params)
    flat_params_out = Identity()
    author_url_in = MapCompose(lambda text: f'https://www.avito.ru{text}')



