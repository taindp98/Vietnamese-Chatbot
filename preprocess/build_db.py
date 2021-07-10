from utils import *
import json
import pandas as pd
export_db_dqn = open('/home/taindp/PycharmProjects/thesis/data/db_hcmut_dqn.json','w')
export_db_mongo = open('/home/taindp/PycharmProjects/thesis/data/db_hcmut_mongo.json','w')
db = json.load(open('/home/taindp/PycharmProjects/thesis/data/db_hcmut.json','r'))
df = pd.DataFrame(db)
df['group'] = df['subject_group'] + df['typical_group']
del df['subject_group']
del df['typical_group']
del df['company']
del df['rate']
del df['tuition_avg_one_sem']
df.rename(columns={'group':'subject_group'},inplace=True)
# print(df.head())
dict_db = df.to_dict('records')
dict2str = str(dict_db).replace(r"'",r'"')
export_db_dqn.write(dict2str)
# print(dict_db)
## dùng đoạn dưới để định dạng import vào mongo
for item in dict_db:
    item2str = str(item)
    itemjson = item2str.replace(r"'",r'"').replace(r'"[',r'[').replace(r']"',r']')
    export_db_mongo.write(itemjson)
    export_db_mongo.write('\n')
