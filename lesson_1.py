from pathlib import Path
import requests


url = "https://catalog.onliner.by/superprice"

headers = {
    "User-Agent": "Mask"
}

response = requests.get(url, headers=headers)

file = Path(__file__).parent.joinpath('onliner.html')

file.write_text(response.text, encoding='Utf-8')
