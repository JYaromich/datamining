from pathlib import Path
import json
import requests

url = "https://5ka.ru/api/v2/special_offers/"

headers = {
    "User-Agent": "Mask"
}

params = {
    "store": None,
    "records_per_page": 12,
    "page": 1,
    "categories": None,
    "ordering": None,
    "price_promo__gte": None,
    "price_promo__lte": None,
    "search": "молоко"
}

response = requests.get(url, headers=headers, cookies={'location_id': '1814'}, params=params)

file = Path(__file__).parent.joinpath('5ka.json')

file.write_text(response.text, encoding='Utf-8')
# data = json.loads(response.text)
response.json()

print(1)