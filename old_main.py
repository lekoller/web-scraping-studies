import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {
    'authority': 'www.residentevildatabase.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'accept-language': 'en-US,en;q=0.7',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '"Chromium";v="112", "Brave";v="112", "Not:A-Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'sec-gpc': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
}

def list_characters_urls() -> list:
    url = 'https://www.residentevildatabase.com/personagens/'

    resp = requests.get(url, headers=headers)

    bs = BeautifulSoup(resp.text, features='lxml')

    characters = bs.find('div', class_='td-page-content').find_all('a')

    return [char['href'] for char in characters]


def get_character_info(url: str) -> dict:
    d = {}
    d['Nome'] = url.split('/')[-2].replace('-', ' ').title()

    resp = requests.get(url, headers=headers)

    bs = BeautifulSoup(resp.text, features='lxml')

    ems = bs.find('div', class_='td-page-content').find_next('p').find_all('em')

    print('-------------------')
    print(d['Nome'])

    for em in ems:
        if len(em.text.split(':')) > 2:
            for e in em.text.split('.'):
                if len(e.split(':')) == 2:
                    k, v = e.split(':')
                    d[k.strip()] = v.strip()
        else:
            k, v = em.text.split(':')
            d[k.strip()] = v.strip()

    appearances = bs.find('div', class_='td-page-content').find_next('p').find_next('p').find_all('a')

    for ap in appearances:
        d['Aparições'] = d.get('Aparições', []) + [ap.text]

    series = pd.Series(d)
    print(series.to_frame().T)

    return d


characters = list_characters_urls()

for char in characters:
    get_character_info(char)