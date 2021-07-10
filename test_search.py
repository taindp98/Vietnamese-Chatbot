from googleapiclient.discovery import build
import pprint
from numpy import random
import requests
from bs4 import BeautifulSoup
import timeout_decorator
# from nltk import sent_tokenize
from multiprocessing import Pool
import re
import sys
import string
from lxml import html
from pyvi import ViTokenizer
# import nltk
# nltk.download('punkt')
from utils import create_token

api_key = 'AIzaSyBBdsq3wrFdDqMZZQZLt1qUBZeiVUNtIkE'
cse_id = 'f4d69fe0222dc82dd'
def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]
def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']

# print(results[0])
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
    return ' '.join(rs)
if __name__=="__main__":

    results = google_search(
        '', api_key, cse_id, num=10)
    result = results[0]
    doc = get_content_from_url(result['link'])
    # print(doc)
    # token = print_50_tokens(doc) # ket qua sau khi lay 50 tokens 
    # print(token)
