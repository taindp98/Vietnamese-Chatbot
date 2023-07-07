from utils import *
import json
db_path = '/home/taindp/PycharmProjects/thesis/data/db_hcmut_full.json'
db_path_import_mongo = '/home/taindp/PycharmProjects/thesis/data/db_hcmut_import_mongo.json'
db_path_train = '/home/taindp/PycharmProjects/thesis/data/db_hcmut_train.json'
db = json.load(open(db_path,encoding='utf-8'))
for item in db:
    for key in list(item.keys()):
        if key == 'duration_std' or key == 'point' or key == 'rate':
            value = str(item[key][0])
            item[key] = [value]
            print(value)
        # if type(value) != list:
        #     item[key] = [value]
# print(db)
# with open(db_path_train,'w') as fileout:
#     # for item in db:
#     db_str = str(db).replace(r"'",r'"')
#     fileout.write(db_str)
    # fileout.write('\n')

