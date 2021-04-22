from itemloaders.processors import MapCompose, TakeFirst, Identity
from scrapy.loader import ItemLoader


def get_tag_data(data):
    not_tag_information = ['top', 'recent']
    return {key: value for key, value in data.items() if key not in not_tag_information}


class TagInstagramLoader(ItemLoader):
    date_parse_out = TakeFirst()
    data_in = MapCompose(get_tag_data)
    data_out = Identity()


class PostInstagramLoader(ItemLoader):
    date_parse_out = TakeFirst()
    data_out = Identity()
