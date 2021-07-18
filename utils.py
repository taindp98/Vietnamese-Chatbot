from datetime import date
import string
import numpy as np
from pyvi import ViTokenizer
# import regex as re
import os
import re
import json
# from fastai.text import *
import pandas as pd
import pickle
from fuzzywuzzy import fuzz
from preprocess.normalize_typing import chuan_hoa_dau_cau_tieng_viet
# path = '/home/taindp/Database/intent/'
# path = 'data/'
path = './data'
def compare_word(token_rule,sentence):
    """
    compare 2 char
    params:
        character a, character b, threshold
    return:
        boolean, True if pass thresshold
    """
    token_set_ratio = fuzz.token_set_ratio(token_rule,sentence)

    token_set_ratio = float(token_set_ratio)/100
    return token_set_ratio
    
def normalize_format_number(mess):
    decmark_reg = re.compile('(?<=\d),(?=\d)')
    mess_norm = decmark_reg.sub('.',mess)
    return mess_norm

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

def remove_stopword(mess):
    # input: đường dẫn tới file chứa stopword
    # input: câu nhập vào của người dùng đã create_token thành token
    # return: câu tự nhiên đã loại bỏ stopword giúp bắt entity dễ dàng hơn
    mess_cleaned=create_token(mess)
    f=open(os.path.join(path,'stopword.txt'),'r')
    stopword=f.read()
    sw_word=stopword.split(',')
    stop_word=set(sw_word)
    mean_mess=[w for w in mess_cleaned if w not in stop_word]
    mess_std = []
    for item in mean_mess:
        item_std = item.replace('_',' ')
        mess_std.append(item_std)
    return ' '.join(mess_std)

uniChars = "àáảãạâầấẩẫậăằắẳẵặèéẻẽẹêềếểễệđìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵÀÁẢÃẠÂẦẤẨẪẬĂẰẮẲẴẶÈÉẺẼẸÊỀẾỂỄỆĐÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴÂĂĐÔƠƯ"
unsignChars = "aaaaaaaaaaaaaaaaaeeeeeeeeeeediiiiiooooooooooooooooouuuuuuuuuuuyyyyyAAAAAAAAAAAAAAAAAEEEEEEEEEEEDIIIOOOOOOOOOOOOOOOOOOOUUUUUUUUUUUYYYYYAADOOU"


def loaddicchar():
    dic = {}
    char1252 = 'à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ'.split(
        '|')
    charutf8 = "à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ".split(
        '|')
    for i in range(len(char1252)):
        dic[char1252[i]] = charutf8[i]
    return dic
dicchar = loaddicchar()
def convert_unicode(txt):
    return re.sub(
        r'à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ',
        lambda x: dicchar[x.group()], txt)
        
def norm_special(string):
    pattern = ["-","/","(",")","!","#","&","^","*","%","<",">","{","}",":",",",";","=","_","+","?","$","~","`","|","\\"]
    for p in pattern:
        if p in string:
            string = string.replace(p,f' {p} ')
#     string = string.replace('/','-')
    return string

def clean_mess(mess):
    # input: câu nhập vào của người dùng
    # return: câu đã loại bỏ special token
    mess_unic = chuan_hoa_dau_cau_tieng_viet(convert_unicode(mess)).lower()
    mess_norm = normalize_format_number(mess_unic)
    # mess_norm = mess_unic
    mess_rmspectoken = re.findall(r'(?i)\b[a-záàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệóòỏõọôốồổỗộơớờởỡợíìỉĩịúùủũụưứừửữựýỳỷỹỵđ0-9\/\-\.]+\b', mess_norm)
    mess_norm = ' '.join(mess_rmspectoken)
    return mess_norm

# print(clean_mess('Cho em hỏi ngành công nghệ kỹ thuật hóa học, xét bằng học bạ đc 84,6 thì có cơ hội không ạ, em cảm ơn ạ'))

def get_current_time():
    time= date.today()
    time_split = str(time).split('-')
    year = time_split[0]
    return year

def find_entity_equation(sentence,list_entity):
    #input câu nhập user nhập vào
    #output tất cả các thực thể trong list_entity có trong câu
    normalized_sentence=convert_unicode(sentence)
    list_token_sentence=normalized_sentence.split(' ')
    list_result_entity=[]
    list_normalized_entity=[convert_unicode(entity) for entity in list_entity]
    for entity in list_normalized_entity:
        list_token_entity=entity.split(' ')
        for i in range(len(list_token_sentence)-len(list_token_entity)+1):
            if list_token_entity==list_token_sentence[i:i+len(list_token_entity)]:
                list_result_entity.append(entity)
    return list_result_entity

def longest_common_sublist(a, b):
    #input list a, list b
    #output số item chung liền kề dài nhất và index item cuoi cung trong list item chung
    table = {}
    l = 0
    i_max = None
    j_max = None
    for i, ca in enumerate(a, 1):
        #enumerate(iter,start)
        for j, cb in enumerate(b, 1):
            if ca == cb:
                table[i, j] = table.get((i - 1, j - 1), 0) + 1
                if table[i, j] > l:
                    l = table[i, j]
                    i_max=i
                    j_max=j
    if i_max != None:
        return l,i_max - 1
    return l,i_max

def lcs_length(a, b):
    #input list a, list b
    #output max length cả liền kề / không liền kề
    table = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i, ca in enumerate(a, 1):
        for j, cb in enumerate(b, 1):
            table[i][j] = (
                table[i - 1][j - 1] + 1 if ca == cb else
                max(table[i][j - 1], table[i - 1][j]))
    return table[-1][-1]

def find_entity_longest_common(sentence,list_entity,entity_name):
    #input câu user nhập vào,list entity, entity được chọn để bắt
    #output index của entity bắt được trong list entity, chiều dài max, index last của token match trong câu nhập vào
    normalized_sentence=convert_unicode(sentence)
    list_token_sentence = normalized_sentence.split(' ')
    list_result_entity = []
    dict_max_len = {}
    list_normalized_entity = [str(entity) for entity in list_entity]
    result = []
    longest_common_length = None
    end_common_index = None
    for index, entity in enumerate(list_normalized_entity):
        list_token_entity = entity.split(' ')
        longest_common_length, end_common_index = longest_common_sublist(list_token_sentence,list_token_entity)
        if longest_common_length!=0:
            dict_max_len[(index)] = {'longest_common_length':longest_common_length,'end_common_index':end_common_index}
        # list_token_sentence = list_token_sentence[: end_common_index - longest_common_length] + list_token_sentence[end_common_index:]
    max_longest_common_length=0
    for k,v in dict_max_len.items():
        if v['longest_common_length']>max_longest_common_length:
            max_longest_common_length=v['longest_common_length']

    for k,v in dict_max_len.items():
        if v['longest_common_length']==max_longest_common_length:
            # if entity_name in ['register','reward','works']:
                # result.append({"longest_common_entity_index":int(k),"longest_common_length":v['max_length_in_sentence'],"end_common_index":v['end_common_index']})
            # else:
                result.append({"longest_common_entity_index":int(k),"longest_common_length":v['longest_common_length'],"end_common_index":v['end_common_index']})
    return result

def check_shorted_entity(path_db_entity):
    # input: path tới json chứa db toàn bộ entity
    # return: chiều dài ngắn nhất cho từng entity
    with open(path_db_entity,'r') as dict_file:
        dict = json.load(dict_file)
    len_dict={}
    for item in dict.keys():
        shorted=100
        for ele in dict[item]:
            ele_ap=[]
            ele_split=str(ele).split()
            for i in ele_split:
                if i != ' ':
                    ele_ap.append(i)
            ele_len=len(ele_ap)
            if ele_len < shorted :
                shorted = ele_len
        len_dict[item]=shorted
    return len_dict

def load_jsonfile(path):
    list_data = []
    for line in open(path, 'r'):
        list_data.append(json.loads(line))
    df = pd.DataFrame.from_dict(list_data)
    return df

def clean_mess_point(mess):
    # input: câu nhập vào của người dùng
    # return: câu đã loại bỏ special token
    mess_unic = convert_unicode(mess).lower()
    mess_rmspectoken = re.findall(r'(?i)\b[a-záàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệóòỏõọôốồổỗộơớờởỡợíìỉĩịúùủũụưứừửữựýỳỷỹỵđ0-9\.]+\b', mess_unic)
    # mess_rmspectoken = ' '.join(re.findall('[a-záàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệóòỏõọôốồổỗộơớờởỡợíìỉĩịúùủũụưứừửữựýỳỷỹỵđA-ZÁÀẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬÉÈẺẼẸÊẾỀỂỄỆÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÍÌỈĨỊÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴĐ0-9\,\.]+', mess_unic))
    mess_norm = ' '.join(mess_rmspectoken)
    return mess_norm

def export_pickle_file(data_dict,path):
    with open(path, 'wb') as handle:
        pickle.dump(data_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

    with open(path, 'rb') as handle:
        valid = pickle.load(handle)
    if data_dict == valid:
        print('export pickle file done')
def check_match_sublist_and_substring(list_children,list_parent):
        # print("match sublist")
        count_match=0
        # print('='*100)
        # print('list_children',list_children)

        ## check string
        list_child_check = []
        list_par_check = []

        for x in list_children:
            if type(x) is str:
                list_child_check.append(convert_unicode(x))
            else:
                list_child_check.append(x)

        for x in list_parent:
            if type(x) is str:
                list_par_check.append(convert_unicode(x))
            else:
                list_par_check.append(x)
        # list_children = [convert_unicode(x) for x in list_children]
        # list_parent = [convert_unicode(x) for x in list_parent]
        for children_value in list_child_check:
            for parent_value in list_par_check:
                if type(children_value) is str and type(parent_value) is str:
                    if children_value in parent_value:
                        count_match+=1
                        break
                elif type(children_value) is float and type(parent_value) is float:
                    # if children_value == parent_value:
                    if parent_value >= min(list_child_check) and  parent_value <= max(list_child_check):
                        # count_match+=1
                        return True
                        # break 
        if count_match==len(list_child_check):
            # print("match sublist")
            return True
        return False

def distance(s, w1, w2):

    if w1 == w2 :
       return 0

    ## check tokenize

    w1_tok = w1.split(' ')[0]
    w2_tok = w2.split(' ')[0]

    # get individual words in a list
    words = s.split(" ")

    # assume total length of the string as
    # minimum distance
    min_dist = len(words)+1

    # print("min_dist",min_dist)

    # traverse through the entire string
    for index in range(len(words)):

        if words[index] in w1_tok or w1_tok in words[index]:
            for search in range(len(words)):

                if words[search] in w2_tok or w2_tok in words[search]:

                    # the distance between the words is
                    # the index of the first word - the
                    # current word index
                    curr = abs(index - search) - 1;

                    # comparing current distance with
                    # the previously assumed distance
                    if curr < min_dist:
                       min_dist = curr

    # w1 and w2 are same and adjacent
    return min_dist



# print(check_match_sublist_and_substring(['b'],['b00', 'b']))

def flatten_lol(lol):
    sublist = []
    flat_list = [item for sublist in lol for item in sublist]
    return flat_list


