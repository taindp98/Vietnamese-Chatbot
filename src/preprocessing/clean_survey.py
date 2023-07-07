from utils import *
import pandas as pd
import random
from datetime import date
# path_sent_crawl = '/home/taindp/PycharmProjects/thesis/data/hcmut_sent_norm.csv'
# path_sent_norm = '/home/taindp/PycharmProjects/thesis/data/hcmut_sent_norm_v0611.csv'
today = str(date.today().strftime("%d/%m/%Y")).replace(r'/',r'_')
# with open(path_sent_crawl,'r') as infile:
#     dataraw = pd.read_csv(infile)
# list_label = dataraw['label'].tolist()
# list_content = dataraw['content'].tolist()
# short_label = []
# short_content = []
# # print(list_label.count(0))
# class0_content = random.sample(list_content[0:253],80)
# class0_label = [0] * 80
# class1_content = list_content[254:]
# class1_lable = [1]* len(class1_content)
#
# label_synth = class0_label + class1_lable
# content_synth = class0_content + class1_content
# for index in list_content_random:

    # sent = str(list_content[index])
    # sent_lower = sent.lower()
    # sent_unic = convert_unicode(sent_lower)
    # token_clean = clean_mess(sent_unic)
    # word_clean = ' '.join(token_clean)
    # sent_clean = word_clean.replace('_',' ')
    # if sent_clean not in short_content:
    #     short_content.append(sent_clean)
    #     short_label.append(list_label[index])
# print((short_label.count(0)))
# print((short_label.count(1)))
# print((short_label.count(2)))
# print((short_label.count(3)))
# df = pd.DataFrame(list(zip(label_synth, content_synth)), columns =['label', 'content'])
# df.to_csv(path_sent_norm,index=False)

# print(today)
