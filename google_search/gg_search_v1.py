from googleapiclient.discovery import build
from numpy import random
import requests
from bs4 import BeautifulSoup
import re
import sys
import string
from pyvi import ViTokenizer
import os
from utils import create_token
from dotenv import load_dotenv

load_dotenv()


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]
def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']

def get_content_from_url(url):
    html = requests.get(url)
    tree = BeautifulSoup(html.text,'lxml')
    for invisible_elem in tree.find_all(['script', 'style']):
            invisible_elem.extract()

    paragraphs = [p.get_text() for p in tree.find_all("p")]

    for para in tree.find_all('p'):
        para.extract()

    for href in tree.find_all(['a','strong']):
        href.unwrap()

    tree = BeautifulSoup(str(tree.html),'lxml')

    text = tree.get_text(separator='\n\n')
    text = re.sub('\n +\n','\n\n',text)

    paragraphs += text.split('\n\n')
    paragraphs = [re.sub(' +',' ',p.strip()) for p in paragraphs]
    paragraphs = [p for p in paragraphs if len(p.split()) > 10]

    return ' '.join(paragraphs)


def print_50_tokens(para):
    tokens = create_token(para)
    if len(tokens) < 50:
        rs =  tokens
    else:
        rs =  tokens[:50]

    token_space = [item.replace('_',' ') for item in rs]

    return ' '.join(token_space)

def pipeline_gg_search(mess,api_key,cse_id):
    results = google_search(mess, api_key, cse_id, num=10)
    ## get first result
    result = results[0]
    doc = get_content_from_url(result['link'])

    dict_search = {}
    dict_search['link'] = result['link']
    dict_search['content'] = print_50_tokens(doc)
    dict_search['title'] = result['title']

    return dict_search

if __name__ == '__main__':
    api_key = os.getenv('GG_API')
    cse_id = os.getenv('CUSTOM_SEARCH_ID')
    
    # mess = 'học bách khoa tphcm thì chỗ ăn chỗ ở thế nào'
    mess = 'quán cà phê gần bách khoa hcm'

    print(pipeline_gg_search(mess,api_key,cse_id))
