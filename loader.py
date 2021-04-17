from itemloaders.processors import TakeFirst, MapCompose, Identity
from scrapy.loader import ItemLoader
from scrapy.selector import Selector


def _get_joined_text(text):
    selector = Selector(text=text)
    return ''.join(selector.xpath('//text()').extract()).replace('\xa0', ' ').strip()


def _get_author_url(text):
    selector = Selector(text=text)
    path = selector.xpath('//text()').extract_first()
    return f"http://hh.ru{path}"


class HeadHunterLoader(ItemLoader):
    default_item_class = dict
    default_output_processor = TakeFirst()

    salary_in = MapCompose(_get_joined_text)
    description_in = MapCompose(_get_joined_text)
    skills_out = Identity()
    company_vacancy_out = Identity()
    skills_in = MapCompose(lambda text: text.replace('\xa0', ' '))
    author_url_in = MapCompose(_get_author_url)
    author_in = MapCompose(_get_joined_text)
    author_description_in = MapCompose(_get_joined_text)
