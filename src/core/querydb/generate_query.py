import pymongo
import re
import numpy as np

# data=mycol.find({
#   "$and": [
#     {
#     "$or":[
#   {"major_name": {"$all": [re.compile("máy tính")]}},
#   {"major_name": {"$all": [re.compile("kỹ thuật hóa")]}}
#     ]},
#   {"type_edu": {"$all": [re.compile("chất lượng cao")]}}
#   ]
# })
def convert_to_regex_constraint(key,values):
    or_list = []
    final_list = []
    or_dict = {}
    if key != 'point':
        if len(values) > 1:
            for value in values:
                all_dict = {}
                all_dict[key] = {"$all":[re.compile(value)]}
                or_list.append(all_dict)
            or_dict["$or"] = or_list
            final_list.append(or_dict)
        else:
            all_dict = {}
            all_dict[key] = {"$all":[re.compile(values[0])]}
            final_list.append(all_dict)
    else:
        all_dict = {}
        all_dict["point"] = {"$gte":values[0],"$lte":values[1]}
        final_list.append(all_dict)
    return final_list[0]


def convert_constraint(constraints,user_action):
    """
    input dict các thực thể theo từng slot {entity_slot:[entity_mess]}
    return câu query mongodb
    form của câu query: { "$and": [{entity_slot:{"$all":[re.compile("entity_mess")]}},{},{}] }
    """
    if user_action["intent"] == "request":
        listkeys = list(constraints.keys())
    and_list = []
    and_dict = {}
    for key in listkeys:
        values = constraints[key]
        and_list.append(convert_to_regex_constraint(key,values))
    and_dict["$and"] = and_list
    return and_dict

if __name__ == '__main__':
    client = pymongo.MongoClient("mongodb://taindp:chatbot2020@thesis-shard-00-00.bdisf.mongodb.net:27017,thesis-shard-00-01.bdisf.mongodb.net:27017,thesis-shard-00-02.bdisf.mongodb.net:27017/hcmut?ssl=true&replicaSet=atlas-12fynb-shard-0&authSource=admin&retryWrites=true&w=majority")
    db = client.hcmut
    collection = db['general'].find({})

#     constr = {'major_name': ['hóa'], 'year': ['2019','2020']}
    constraint = {'major_name': ['cơ khí'],'year':['2020'],'point':[0.0,27.0]}
    mycol = db['general']
    user_action = {}
    user_action['intent'] = 'request'
    data=mycol.find(convert_constraint(constraint,user_action))
    for x in data:
        # print(x['major_name'])
        print(x['point'])
