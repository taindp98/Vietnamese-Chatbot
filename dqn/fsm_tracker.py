import itertools
import pandas as pd

map_order_entity = {}
map_order_entity['major_name'] = ['point','subject_group']
map_order_entity['major_code']=['major_name']
map_order_entity['point']=['major_name','subject_group','year','type_edu','case']
map_order_entity['subject_group']=['major_name']
map_order_entity['subject']=['major_name','subject_group']
map_order_entity['tuition']=['major_name','type_edu']
map_order_entity['year'] = ['major_name','subject_group','point']
map_order_entity['object'] = ['case','type_edu','major_name']
map_order_entity['register'] = ['case','type_edu','major_name']
map_order_entity['criteria'] = ['major_name','case','type_edu']
# intent deep learning
# label = ['other','type_edu','case','career']
map_order_entity['type_edu']=['major_name','subject_group','case']
map_order_entity['case']=['major_name','type_edu']
map_order_entity['career']=['major_name']

map_order_entity['all_slot'] = ['major_name','type_edu','subject_group','year','case','point','career','subject','tuition','major_code','criteria','object','register']


list_define_target = []

for key in list(map_order_entity.keys()):

    if key != 'all_slot':

        list_slot = map_order_entity[key]
        list_permute = list(itertools.permutations(list_slot))
        list_permute_fix = [['initial',key] + list(item) for item in list_permute]

        for sublist_permute in list_permute_fix:

            for idx, slot in enumerate(sublist_permute):
                dict_target = {}
                if idx < len(sublist_permute) - 2:
                    dict_target['request'] = key
                    dict_target['input'] = sublist_permute[idx:idx+2]
                    dict_target['target'] = sublist_permute[idx+2]

                    if dict_target not in list_define_target:
                        list_define_target.append(dict_target)
df_define_target = pd.DataFrame(list_define_target)

list_request = list(df_define_target['request'])
list_input = list(df_define_target['input'])
list_target = list(df_define_target['target'])

def recursion_find_best_way(list_state_tracker,pattern_target,request_slot):

    ## last state is
#     last_state = list_state_tracker[-1]

    ## remove last state --> sucess rate
    # print('update list state tracker',list_state_tracker)
    for item in list_state_tracker:
        if item != 'initial' and item in pattern_target:
#             if last_state in pattern_target:
            pattern_target.remove(item)


    if len(pattern_target) == 0:
        print('sucess')
        return True

    for idx in range(len(list_state_tracker)):
        if idx < len(list_state_tracker) - 1:
            window = list_state_tracker[idx:idx+2]

            for idx, sublist in enumerate(list_input):
                if window == sublist and request_slot[0] == list_request[idx]:
                    target_match = list_target[idx]
                    ## update state tracker
                    if target_match not in list_state_tracker:
                        list_state_tracker.append(target_match)
#                         break
                        return True

    ## recursion
    recursion_find_best_way(list_state_tracker,pattern_target,request_slot)
