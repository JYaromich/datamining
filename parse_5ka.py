from pathlib import Path
import json
import requests
import time

class Parser5ka:
    headers = {
        "User-Agent": "Mask"
    }

    def __init__(self, start_url: str, save_path: Path):
        self.start_url = start_url
        self.save_path = save_path

    def _get_responce(self, url, *args, **kwargs) -> requests.Response:
        while True:
            responce = requests.get(url, *args, **kwargs, headers=self.headers)
            if responce.status_code in (200, 301, 304):
                return responce
            time.sleep(1)

    def run(self):
        for product in self._parse(self.start_url):
            product_path = self.save_path.joinpath(f"{product['id']}.json")
            self._save(product, product_path)

    def _parse(self, url):
        while url:
            response = self._get_responce(url)
            data: dict = response.json()
            url = data.get('next')
            for product in data.get('results', []):
                yield product

    def _save(self, data, file_path):
        file_path.write_text(json.dumps(data, ensure_ascii=False))


def get_save_path(dir_name):
    save_path = Path(__file__).parent.joinpath(dir_name)
    if not save_path.exists():
        save_path.mkdir()
    return save_path


if __name__ == '__main__':
    parser = Parser5ka("https://5ka.ru/api/v2/special_offers/", get_save_path('products'))
    parser.run()
