from googleapiclient.discovery import build
import pprint
from numpy import random
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
import re
import sys
import string
from lxml import html
from pyvi import ViTokenizer
from utils import PreProcess

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

    # for i in range(0,len(paragraphs)):
    #     sents = []
    #     text_chunks = list(chunks(paragraphs[i],100000))
    #     for chunk in text_chunks:
    #         # print(chunk)
    #         sents += ViTokenizer.tokenize(chunk)
    #         print(sents)
    #     # print(sents)
    #     sents = [s for s in sents if len(s) > 2]
    #     sents = ' . '.join(sents)
    #     paragraphs[i] = sents
    return ' '.join(paragraphs)
    # return paragraphs
def create_token(mess):
    # input: câu nhập vào của người dùng
    # return: token(_) loại bỏ những special token
    mess_rmspectoken = re.findall(r'(?i)\b[a-záàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệóòỏõọôốồổỗộơớờởỡợíìỉĩịúùủũụưứừửữựýỳỷỹỵđ0-9]+\b', mess)
    mess_norm = ' '.join(mess_rmspectoken)
    mess_token = ViTokenizer.tokenize(mess_norm)
    mess_lower = mess_token.lower()
    tokens = mess_lower.split()
    table = str.maketrans('', '', string.punctuation.replace("_", ""))
    tokens = [w.translate(table) for w in tokens]
    tokens = [word for word in tokens if word]
    return tokens

def print_50_tokens(para):
    tokens = create_token(para)
    if len(tokens) < 50:
        rs =  tokens
    else:
        rs =  tokens[:50]
    return ' '.join(rs)
def norm_text(mess):
    pp = PreProcess()
    norm_mess = pp.process(mess)
    return norm_mess
def major_vote(tit_tokens,list_phrase):
    mask = [0]*len(list_phrase)
    for i in range(len(list_phrase)):
        for token in tit_tokens:
            if token in list_phrase[i]:
                mask[i] +=1
    for i in range(len(mask)):
        if mask[i] == max(mask):
            vote = list_phrase[i]
            break
    return vote


if __name__=="__main__":
    question = 'ai là người giàu nhất việt nam'
    norm_question = norm_text(question)
    # norm_question = question
    # print(norm_question)
    results = google_search(norm_question, api_key, cse_id, num=10)
    result = results[0]
    # print(result)
    title = result['title']
    tit_tokens = create_token(title)
    print(tit_tokens)
    doc = get_content_from_url(result['link']).lower()
    list_phrase = doc.split('\n')
    # print(list_content)
    # print(title)
    # para = 'Chỉ hơn 1 tháng sau khi Fores công bố danh sách tỉ phú thế giới ngày 6-4-2021, đến nay tài sản của tỉ phú Phạm Nhật Vượng đã được cộng thêm 1 tỉ USD, tăng lên 8,3 tỉ USD. Ông Vượng tiếp tục giữ vững vị trí người giàu nhất Việt Nam'
    # token = print_50_tokens(doc) # ket qua sau khi lay 50 tokens 
    # print(title+": "+ token)
    content_vote = major_vote(tit_tokens,list_phrase)
    print("Câu trả lời: {}".format(content_vote))
