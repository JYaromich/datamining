import requests
from urllib.parse import urljoin
from collections import defaultdict
import datetime
import bs4
import time
import pymongo


class MagnitParse:
    def __init__(self, start_url, db_client):
        self.start_url = start_url
        db = db_client['gb_data_mining']
        self.collection = db['magnit']

    def _get_response(self, url, *args, **kwargs):
        try:
            responce = requests.get(url, *args, **kwargs)
            while True:
                if responce.status_code in (200, 301, 304):
                    return responce
                time.sleep(1)
        except Exception as ex:
            print(ex)

    def _get_soup(self, url, *args, **kwargs):
        try:
            return bs4.BeautifulSoup(self._get_response(url, *args, **kwargs).text, 'lxml')
        except Exception as ex:
            print(ex)

    def run(self):
        for product in self._parse(self.start_url):
            self._save(product)

    @classmethod
    def _parse_date(cls, input_str):
        try:
            if not input_str:
                return None

            _month_dict = {
                'января': 1,
                'февраля': 2,
                'марта': 3,
                'апреля': 4,
                'мая': 5,
                'июня': 6,
                'июля': 7,
                'августа': 8,
                'сентября': 9,
                'октября': 10,
                'ноября': 11,
                'декабря': 12
            }

            day = None
            month = None
            for part in input_str.split():
                if part.isdigit(): day = int(part)
                if part in _month_dict: month = _month_dict[part]

            return datetime.datetime(
                year=datetime.datetime.now().year,
                month=month,
                day=day
            )
        except Exception as ex:
            print(f"Error. Doesn't transform date. Input str: {input_str}")
            print(ex)

    def __get_price(self, tag, price_name: str):
        if prices := tag.find('div', attrs={'class': 'card-sale__price'}):
            if part_price := prices.find('div', attrs={'class': price_name}):
                if '%' not in part_price.text:
                    return float('.'.join(str.split(part_price.text)))
        return None

    def __get_date(self, tag, label):
        date_all = tag.find('div', attrs={'class': 'card-sale__date'}).find_all('p')
        date_dict = defaultdict(lambda: None)
        for i, value in enumerate(date_all):
            date_dict[i] = value.text

        return date_dict[label]

    @property
    def _template(self):
        return {
            'url': lambda tag: urljoin(self.start_url, tag.attrs.get('href', '')),
            'promo_name': lambda tag: promo_name.text if (
                promo_name := tag.find('div', attrs={'class': 'card-sale__header'})) else None,
            'product_name': lambda tag: product_name.text if (
                product_name := tag.find('div', attrs={'class': 'card-sale__title'})) else None,
            'old price': lambda tag: self.__get_price(tag, 'label__price_old'),
            'new price': lambda tag: self.__get_price(tag, 'label__price_new'),
            'image ulr': lambda tag: urljoin(self.start_url, tag.find('img').attrs['data-src']),
            'date from': lambda tag: MagnitParse._parse_date(self.__get_date(tag, 0)),
            'date to': lambda tag: MagnitParse._parse_date(self.__get_date(tag, 1))
        }

    def _parse(self, url):
        soup = self._get_soup(url)
        main_catalog = soup.find('div', attrs={'class': 'сatalogue__main'})
        main_catalog.find_all('a', recursive=False)
        product_tags = main_catalog.find_all('a', recursive=False)
        for product_tag in product_tags:
            product = {}
            for key, func in self._template.items():
                try:
                    product[key] = func(product_tag)
                except Exception as ex:
                    print(ex)
            yield product


    def _save(self, data):
        self.collection.insert_one(data)


if __name__ == '__main__':
    url = "https://magnit.ru/promo/?geo=moskva"
    db_client = pymongo.MongoClient("mongodb://localhost")
    parser = MagnitParse(url, db_client)
    parser.run()
