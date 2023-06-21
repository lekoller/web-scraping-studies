
from bs4 import BeautifulSoup
import requests

from constants.headers import headers


def get_web_text(url: str) -> str:
    resp = requests.get(url, headers=headers)

    bs = BeautifulSoup(resp.text, features='lxml')

    return bs.get_text()


def get_web_page(url: str) -> BeautifulSoup:
    resp = requests.get(url, headers=headers)

    return BeautifulSoup(resp.text, features='lxml')