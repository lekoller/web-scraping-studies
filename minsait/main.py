import datetime
import pandas as pd

from persistence.repository import GenericRepository
from utils.get_web import get_web_page, get_web_text
from utils.get_text_after import get_text_after
from utils.transform_data import transform_data
from utils.download import download_xlsx_file
from utils.process import process_xlsx_file


repository = GenericRepository(db_name='minsait', collection_name='bulletins')
last_document = repository.get_last_document()
text = get_text_after('Últimos Boletins', get_web_text('https://www.conab.gov.br/info-agro/safras'))

if last_document == None or last_document['snippet'] != text:
    repository.insert_document({
        'snippet': text,
        'created_at': datetime.datetime.now(),
    })
    
    if last_document != None:
        repository.remove_document(last_document['_id'])
        print('Old bulletin removed')

    # get all xlsx files
    bs = get_web_page('https://www.conab.gov.br/info-agro/safras') 

    ems = bs.find('div', id='k2ModuleBox525').find_all('a')

    for em in ems:
        title = em.get('title')

        if title.endswith('.xlsx'):
            title = title[:-5]
            file_url = 'https://www.conab.gov.br'+em.get('href')
            file_path = 'xlsx/'+ title + '.xlsx'

            download_xlsx_file(file_url, file_path)
            process_xlsx_file(file_path)
