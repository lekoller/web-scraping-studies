import os
import requests

from constants.headers import headers


def download_xlsx_file(url: str, file_path: str):
    resp = requests.get(url, headers=headers)

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with open(file_path, 'wb') as file:
        file.write(resp.content)