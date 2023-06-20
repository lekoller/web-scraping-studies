import datetime
import json
import math
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup

from persistence.repository import GenericRepository

headers = {
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

# copilot, please, help to declare a variable with Response type
def get_web_text(url: str) -> str:
    resp = requests.get(url, headers=headers)

    bs = BeautifulSoup(resp.text, features='lxml')

    return bs.get_text()

def get_web_page(url: str) -> BeautifulSoup:
    resp = requests.get(url, headers=headers)

    return BeautifulSoup(resp.text, features='lxml')

def get_text_after(snippet: str, text: str) -> str:
    list_text = text.split(' ')
    list_snippet = snippet.split(' ')
    words_in_snippet = len(list_snippet)

    for i, word in enumerate(list_text):
        word = word.lower()

        if word == list_snippet[0].lower():
            matches = 0

            for j, snippet_word in enumerate(list_snippet):
                if list_text[i + j].lower() != snippet_word.lower():
                    break

                matches += 1
            
            if matches == words_in_snippet:
                return ' '.join(list_text[i + matches:])

    return ''

def download_xlsx_file(url: str, file_path: str):
    resp = requests.get(url, headers=headers)

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with open(file_path, 'wb') as file:
        file.write(resp.content)

    sheets = pd.read_excel(file_path, sheet_name=None)

    for sheet_name, df in sheets.items():
        if sheet_name == list(sheets.keys())[0]:
            continue

        if sheet_name == list(sheets.keys())[1]:
            # df.columns = ['PRODUTO', 'SAFRAS_21/22',  'SAFRAS_22/23', 'Percentual', 'Absoluta', 'Variação', '']


            documents = df.to_dict(orient='records')
            print()
            print()
            print()
            print()
            print()
            print(file_path)
            print(sheet_name)
            # print(len(documents))
            # print('0', documents[0])
            # print('1', documents[1])
            # print('2', documents[2])
            # print('3', documents[3])
            # print('4', documents[4])
            # print('5', documents[5])
            # print('6', documents[6])
            # print('7', documents[7])
            # print('8', documents[8])
            # print()
            # print()
            # print()
            

            insert_dict = {}
            titles = []
            titles_index = 0
            table_index = 0
            
            for index, document in enumerate(documents):
                values = list(document.values())
                
                # check if all is nan
                if all([type(value) == float and value != value for value in values]):
                    continue

                if any([type(value) == float and value != value for value in values]):
                    big_one = ''
                    if type(values[0]) == str:
                        big_one = values[0]
                        insert_dict[big_one] = {}

                    # string_values = [value.strip().replace(" ", "") for value in values if type(value) == str]
                    string_values = []
                    
                    for value in values:
                        in_dict = {}

                        if type(value) == str and value != '' and value != big_one:
                            string_values.append(value.strip().replace(" ", ""))
                        elif value == big_one:
                            continue
                        else:
                            string_values.append('')

                    if len(string_values) > 1:
                        # check if all is empty string
                        if all([value == '' for value in string_values]):
                            continue

                        # title_values = string_values
                        title_values = {}

                        for i, value in enumerate(string_values):
                            if value != '':
                                title_values[value] = 0
                                continue

                            keys = list(title_values.keys())

                            if keys:
                                last_key = str(keys[-1])

                                title_values[last_key] += 1
                                
                        # print(title_values)
                        titles.append(title_values)
                        
                else:
                    titles_index += 1
                    keys = list(insert_dict.keys())

                    if keys:
                        last_key = str(keys[-1])

                        insert_dict[last_key][values[0]] = {}

                # check if at least one is nan
            # print()
            # print(titles)
            # print()
            # print(json.dumps(insert_dict, indent=2))
            # print()
            field_tree = {}

            for index, title in enumerate(titles):
                print(title)

                if index == 0 or all([value == 0 for value in title.values()]):
                    keys = list(title.keys())
                    # print(keys)
                    for key in keys:
                        field_tree[key] = {}

                    continue

                keys = list(title.keys())
                
                for key in keys:
                    for k in list(field_tree.keys()):
                        if titles[index - 1][k] != 0:
                            field_tree[k][key] = {}
                            # wrong
                            titles[index - 1][k] -= 1

            # for insert_dict_key in insert_dict.keys():
            #     for item_key in insert_dict[insert_dict_key].keys():

                

        documents = df.to_dict(orient='records')
        # collection_name = sheet_name.replace(' ', '_').lower()

        # repository = GenericRepository(db_name='brutes', collection_name=collection_name)

        # for document in documents:
        #     print(document)
        #     repository.insert_document(document)

repository = GenericRepository(db_name='minsait', collection_name='bulletins')

last_document = repository.get_last_document()

text = get_text_after('Últimos Boletins', get_web_text('https://www.conab.gov.br/info-agro/safras'))

if last_document == None or last_document['snippet'] != text:
    # here enters the new feature k2ModuleBox525
    repository.insert_document({
        'snippet': text,
        'created_at': datetime.datetime.now(),
    })
    
    if last_document != None:
        repository.remove_document(last_document['_id'])
        print('Old bulletin removed')
else:
    bs = get_web_page('https://www.conab.gov.br/info-agro/safras') 

    ems = bs.find('div', id='k2ModuleBox525').find_all('a')

    for em in ems:
        title = em.get('title')

        if title.endswith('.xlsx'):
            title = title[:-5]
            file_url = 'https://www.conab.gov.br'+em.get('href')
            file_path = 'xlsx/'+ title + '.xlsx'  # Specify the path where you want to save the file

            download_xlsx_file(file_url, file_path)
