import json
from pyvi import ViTokenizer
import pandas as pd
import csv
import re
import normalize_unicode
#1. Đọc các file json để tạo từ điển
with open('viettat.json') as file1:
    d1 = json.load(file1)
with open('teencode.json') as file2:
    d2 = json.load(file2)
with open('name_univ.json') as file3:
    d3 = json.load(file3)
with open('complete.json') as file4:
    d4 = json.load(file4)
data={}
data.update(d1)
data.update(d2)
data.update(d3)
data.update(d4)
#print(data)

#2. Đọc tập dữ liệu thô để chuẩn hóa
with open('dataset_raw.csv') as fraw:
    raw=pd.read_csv(fraw)
raw.columns=['Label','Content']
header=['Label','Content']
list_key=list(data.keys())
for t in range(len(list_key)):
    list_key[t]=list_key[t].lower()
dict=dict(zip(list_key,data.values()))
with open('data_edit.csv','w') as file_edit:
    writer=csv.writer(file_edit,delimiter=',',quotechar='"')
    writer.writerow(header)
    #writer=csv.DictWriter(file_edit,fieldnames=header)
    #writer.writeheader()
    for k in range(len(raw)):
        #if (k != 0):
        sent=raw['Content'].loc[k]
        label=raw['Label'].loc[k]
        #print(label)
        sent = normalize_unicode.convert_unicode(sent)
        sent = re.findall(r'(?i)\b[a-záàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệóòỏõọôốồổỗộơớờởỡợíìỉĩịúùủũụưứừửữựýỳỷỹỵđ]+\b', sent)
        sent=' '.join(sent)
        sent=ViTokenizer.tokenize(sent).lower()
        sent=nltk.word_tokenize(sent)
        for i,v in enumerate(sent):
            if v in dict.keys():
                new_v=v.replace(v,dict[v].lower())
                sent[i]=new_v
        #sent_new=(TreebankWordDetokenizer().detokenize(sent))
        sent_new=' '.join(sent)
        sent_new=sent_new.replace('_',' ')
        #print((sent_new))


        writer.writerow([label,sent_new])

