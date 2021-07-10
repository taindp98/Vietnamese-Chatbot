from utils import *
# import json
from intent.intent_regconize import catch_intent
from entity.confirm_object import catch_point
from collections import OrderedDict

from entity.constants_ner import map_order_entity,list_entity
"""
    
    label = ['other_intent','type_edu','case','career']
"""
dict_entity = list_entity[0]

## add key --> list value to matching confirm object
# count = 0
for key,value in map_order_entity.items():
    if not key.endswith('inform') and key != 'not_intent':
        map_order_entity[key] = map_order_entity[key] + [key]

# print(map_order_entity)

def find_all_entity(intent,mess_clean):
    normalized_input_sentence = mess_clean
    result_entity_dict={}
    list_order_entity_name=map_order_entity[intent]
    map_entity_name_to_threshold={}
    for entity_name in list_order_entity_name:
        # threshold wordnumber
        if entity_name in ['subject','tuition', 'subject_group','major_code','year']:
            map_entity_name_to_threshold[entity_name]=1
        elif entity_name in ['major_name','type_edu']:
            map_entity_name_to_threshold[entity_name]=2
        elif entity_name in ['case']:
            map_entity_name_to_threshold[entity_name]=3
        else:
            map_entity_name_to_threshold[entity_name]=4

    ordered_real_dict = OrderedDict()
    for entity_name in map_order_entity[intent]:
        # print(entity_name)
        ordered_real_dict[entity_name] = dict_entity[entity_name]
    for entity_name, list_entity in ordered_real_dict.items():
        # phân biệt cho từng order
        if entity_name == 'type_edu':
            matching_threshold = 0.2
        elif entity_name == 'subject':
            matching_threshold = 0.55
        elif entity_name == 'major_name':
            matching_threshold = 0.35
        elif entity_name == 'case':
            matching_threshold = 0.4

        else:
            matching_threshold = 0.1
        catch_entity_threshold_loop = 0
        while True:
            if catch_entity_threshold_loop > 3:
                break
            list_dict_longest_common_entity = find_entity_longest_common(normalized_input_sentence,list_entity,entity_name)
            if list_dict_longest_common_entity == []:
                break
            if list_dict_longest_common_entity[0]['longest_common_length'] < map_entity_name_to_threshold[entity_name] :
                break

            list_sentence_token = normalized_input_sentence.split(' ')
            greatest_entity_index=None
            greatest_common_length = None
            greatest_end_common_index = None
            max_match_entity = 0.0
            for dict_longest_common_entity in list_dict_longest_common_entity:
                longest_common_entity_index = dict_longest_common_entity['longest_common_entity_index']
                longest_common_length = dict_longest_common_entity['longest_common_length']
                end_common_index = dict_longest_common_entity['end_common_index']
                list_sentence_token_match = list_sentence_token[end_common_index - longest_common_length+1:end_common_index+1]

                list_temp_longest_entity_token = str(list_entity[longest_common_entity_index]).split(' ')
                score = len(list_sentence_token_match)/float(len(list_temp_longest_entity_token))
                # print(score)
                if score > max_match_entity:
                    max_match_entity = score
                    greatest_entity_index = longest_common_entity_index
                    greatest_common_length = longest_common_length
                    greatest_end_common_index = end_common_index
            if greatest_common_length >= map_entity_name_to_threshold[entity_name] and max_match_entity > matching_threshold:
                result = ' '.join(list_sentence_token[greatest_end_common_index - greatest_common_length +1 :greatest_end_common_index +1])

                if entity_name in result_entity_dict:
                    result_entity_dict[entity_name].append(result)
                else:
                    result_entity_dict[entity_name] = [result]
                list_sentence_token[greatest_end_common_index - greatest_common_length +1 :greatest_end_common_index +1] = ["✪"]*greatest_common_length
                normalized_input_sentence = ' '.join(list_sentence_token)
            catch_entity_threshold_loop = catch_entity_threshold_loop + 1
    # if intent == 'point':
    #     result_entity_dict['point'] = catch_point(input_sentence)
    point_entity,list_point_regex = catch_point(mess_clean)
    list_entity_found = list(result_entity_dict.values())
    confirm_obj = None
    # print('point_entity',point_entity)
    if list_entity_found:
        for p in list_point_regex:
            for sublist_entity in list_entity_found:

                for e in sublist_entity:

                    if p not in e and point_entity:
                        # if point_entity:
                        # print('Trueeeee')
                        result_entity_dict['point'] = point_entity

                        if intent in result_entity_dict:
                            value = result_entity_dict.pop(intent)
                            confirm_obj = {intent:value}
    else:
        if point_entity:
            result_entity_dict['point'] = point_entity

    if intent in result_entity_dict:
        value = result_entity_dict.pop(intent)
        confirm_obj = {intent:value}

    return result_entity_dict,confirm_obj

# mess1 = 'cho em hỏi khối nào thi môn hoá học'
# s = 'Thi khối B cần học những môn nào?'
# s = 'cho em xin Chỉ tiêu tuyển sinh năm 2020 của khối A1 ngành điện điện tử?'
# #
# intent_catched, prob,mess_clean = catch_intent(s)
# print('intent',intent_catched)
# entity_dict,confirm = find_all_entity(intent_catched,mess_clean)
# print('entity_dict',entity_dict)
# print("confirm",confirm)
