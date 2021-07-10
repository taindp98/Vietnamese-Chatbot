import requests
from glob import glob
import os
import random
import pandas as pd
import json

FOLDER_PATH = './dqn'
CONSTANTS_FILE_PATH = f'{FOLDER_PATH}/constants.json'
# CONSTANT_FILE_PATH = 'constants.json'
with open(CONSTANTS_FILE_PATH) as f:
    constants = json.load(f)

path_weight = constants['agent']['load_weights_file_path'].split('/')[-1].replace('.h5','')

def get_bot_response(userText,user_id):
    # userText = request.args.get('msg')
    api_url = 'http://0.0.0.0:6969/api/convers-manager'
    # api_url = 'https://chatbot-hcmut.herokuapp.com/api/convers-manager'
    input_data = {}
    input_data['message'] = str(userText)
    # input_data['state_tracker_id'] = '1011'
    input_data['state_tracker_id'] = user_id
    r = requests.post(url=api_url, json=input_data)
    chatbot_respose = r.json()
    list_mess_response = chatbot_respose['message']
    list_mess_response = [item.replace('\n', r'').replace(r'"',r'') for item in list_mess_response]
    return list_mess_response

RULE_BASED = True

if RULE_BASED:
    use_case = 'rule_based'
else:
    use_case = path_weight

# list_case = [0,1,2,3,4]
# case_path = './test_case/{}'.format(use_case)
# list_case = glob(os.path.join(case_path,'*.txt'))
# list_num_case = [int(item.split('/')[-1].replace('.txt','').replace('case','')) for item in list_case]
# list_num_case_sort = sorted(list_num_case)



# print('----',use_case,'-----')
# for case_num in list_num_case_sort:
#     if case_num == 18:
#
#         print('='*50)
#         current_case = os.path.join(case_path,str('case'+str(case_num)+'.txt'))
#         # case_num = case.split('/')[-1].replace('.txt','')
#         print('case {}'.format(case_num))
#         file_input = open(current_case,'r').readlines()
#         list_text = []
#         user_id = random.randint(0,999)
#         for text in file_input:
#             text_input = text.replace('\n','')
#             print('User: {}'.format(text_input))
#             agent = get_bot_response(text_input,user_id)
#             print('Agent: {}'.format(agent))
#             # if str(agent[0]).startswith('Thông tin'):
#                 # print('----Pass----')
#                 # break
