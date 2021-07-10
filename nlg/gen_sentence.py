import re
import random
import warnings

from utils import check_match_sublist_and_substring
warnings.filterwarnings('ignore')

from nlg.constants_response import *

# def get_greeting_statement():
#     return random.choice(GREETING)
def response_craft(agent_action, state_tracker, confirm_obj,isGreeting=False):
    sentence_pattern = None
    list_sentence = []

    if isGreeting:
        print('Treee')
        sentence = random.choice(GREETING)
        # return random.choice(GREETING)
        list_sentence.append(sentence)
        return list_sentence

    agent_intent = agent_action['intent']



    if agent_intent == "inform":
        ############ TO DO : lấy list_match_obj ra inform cho user (dạng câu) (ok)
        # list_match_obj = agent_action['list_match_obj']
        inform_slot = list(agent_action['inform_slots'].keys())[0]
        if agent_action['inform_slots'][inform_slot] == 'no match available':
            sentence = random.choice(NOT_FOUND)
            list_sentence.append(sentence)
            # return random.choice(NOT_FOUND)
            return list_sentence

        #check lai
        sentence_pattern = random.choice(INFORM[inform_slot])

        sentence = sentence_pattern.replace("*{}*".format(inform_slot), AGENT_INFORM_OBJECT[inform_slot])

        if len(agent_action['inform_slots'][inform_slot]) > 1:
            inform_value = ",\n".join(agent_action['inform_slots'][inform_slot])
            sentence = sentence.replace("*{}_instance*".format(inform_slot), "\n\"{}\"".format(inform_value))

        elif len(agent_action['inform_slots'][inform_slot]) == 1:

            inform_value = agent_action['inform_slots'][inform_slot][0]
            sentence = sentence.replace("*{}_instance*".format(inform_slot), "\"{}\"".format(inform_value))
        else:
            sentence_pattern = random.choice(EMPTY_SLOT)
            sentence = sentence_pattern.replace("*request_slot*", AGENT_REQUEST_OBJECT[inform_slot])

        ## add list_sentence
        list_sentence.append(sentence)

    elif agent_intent == "request":
        request_slot = list(agent_action['request_slots'].keys())[0]
        sentence_pattern = random.choice(REQUEST[request_slot])
        sentence = sentence_pattern.replace("*{}*".format(request_slot), AGENT_REQUEST_OBJECT[request_slot])

        ## add list_sentence
        list_sentence.append(sentence)

    elif agent_intent == "done":
        sentence = random.choice(DONE)
        ## add list_sentence
        list_sentence.append(sentence)
        # return random.choice(DONE)
        return list_sentence

    elif agent_intent == "match_found":
        # print('>'*50)
        # print('match_found')
        inform_slot = state_tracker.current_request_slots[0]
        # inform_slot = user_action['request_slots']
        # print('inf_slot',inform_slot)

        if agent_action['inform_slots']['major'] == "no match available":
            sentence_pattern = random.choice(MATCH_FOUND['not_found'])
            sentence = sentence_pattern.replace("*found_slot*", AGENT_INFORM_OBJECT[inform_slot])
            ## add list_sentence
            list_sentence.append(sentence)

        else:
            key = agent_action['inform_slots']['major']
            first_result_data = agent_action['inform_slots'][key][0]

            list_record_match = list(agent_action['inform_slots'].values())[0]

            list_unique_slot_in_record_match = []
            for record in list_record_match:
                result = record[inform_slot]
                if result not in list_unique_slot_in_record_match:
                    list_unique_slot_in_record_match.append(result)

            # print('record match inform slot',list_unique_slot_in_record_match)

            # first_result_data = agent_action['inform_slots']

            # #nếu là câu hỏi intent confirm thì cần nlg lại mà match hay không
            # print("-------------------------------inform slot :{}".format(inform_slot))
            # print("---------------------------------confirm obj: {}".format(confirm_obj))
            response_match = ''
            # print('confirm_obj',confirm_obj)
            if confirm_obj != None:
                # if inform_slot not in list_map_key:
                # print('999999999')
                # print(confirm_obj[inform_slot],list_unique_slot_in_record_match)

                for item in list_unique_slot_in_record_match:
                    # print('item match',item)
                    check_match = check_match_sublist_and_substring(confirm_obj[inform_slot],item)
                    if check_match:
                        break
                value_match = ''
                if len(confirm_obj[inform_slot]) > 1:
                    # print(AGENT_INFORM_OBJECT[inform_slot])
                    if inform_slot != 'point':
                        value_match = ',\n'.join([str(item) for item in confirm_obj[inform_slot]])

                    else:
                        # print('#'*100)
                        confirm_obj_non_limit = []
                        for item in confirm_obj[inform_slot]:
                            if item != float(0) and item != float(100) and item != float(1000):
                                # print('item float',item,type(item))
                                confirm_obj_non_limit.append(item)
                        
                        value_match = ' ,\n'.join([str(item) for item in confirm_obj_non_limit])
                else:          
                    # print('#'*100)
                    value_match = str(confirm_obj[inform_slot][0])
                if check_match:
                    if inform_slot != 'point':
                        response_match = "\n\nĐúng rồi! Thông tin {0} bạn cần là {1}".format(AGENT_INFORM_OBJECT[inform_slot],value_match)
                    else:
                        response_match = "Chúc mừng bạn! Điểm của bạn cao hơn điểm chuẩn được công bố"
                else:
                    if inform_slot != 'point':
                        response_match = "\n\nSai rồi! Thông tin {0} không phải là {1}".format(AGENT_INFORM_OBJECT[inform_slot],value_match)
                    else:
                        response_match = "Điểm của bạn thấp hơn điểm chuẩn được công bố!"
                ## add list_sentence
                list_sentence.append(response_match)
            if inform_slot != "major":
                # sentence_pattern = random.choice(MATCH_FOUND['found'])
                # sentence = sentence_pattern.replace("*found_slot*", AGENT_INFORM_OBJECT[inform_slot])
                # print('sentence',sentence)
                # print('first_result_data',first_result_data)

                ## check many result

                if len(list_unique_slot_in_record_match) == 1:
                    sentence_pattern = random.choice(MATCH_FOUND['found'])
                    sentence = sentence_pattern.replace("*found_slot*", AGENT_INFORM_OBJECT[inform_slot])

                    first_record = list_unique_slot_in_record_match[0]

                    # if len(first_result_data[inform_slot]) > 1:
                    if len(first_record) > 1:
                        # inform_value = ",\n".join(first_result_data[inform_slot])
                        inform_value = ",\n".join(first_record)
                        sentence = sentence.replace("*found_slot_instance*", "\n\"{}\"".format(inform_value))
                    # elif len(first_result_data[inform_slot]) == 1:
                    elif len(first_record) == 1:
                        # inform_value = first_result_data[inform_slot][0]
                        inform_value = first_record[0]
                        sentence = sentence.replace("*found_slot_instance*", "\"{}\"".format(inform_value))
                    else: #slot mà user request của kết quả trả về là list rỗng
                        # inform_value = "không có thông tin này"
                        sentence = EMPTY_SLOT[0].replace("*request_slot*",AGENT_INFORM_OBJECT[inform_slot])

                    ## add list_sentence
                    list_sentence.append(sentence)

                else:
                                        # print('here')
                    # list_sentence = []
                    for item in list_unique_slot_in_record_match:
                        # print(item)
                        sentence_pattern = random.choice(MATCH_FOUND['found'])
                        sentence = sentence_pattern.replace("*found_slot*", AGENT_INFORM_OBJECT[inform_slot])
                        if len(item) > 1:
                            # inform_value = ",\n".join(first_result_data[inform_slot])
                            inform_value = ",\n".join(item)
                            sentence = sentence.replace("*found_slot_instance*", "\n\"{}\"".format(inform_value))
                        # elif len(first_result_data[inform_slot]) == 1:
                        #     print(inform_value)
                        elif len(item) == 1:
                            # inform_value = first_result_data[inform_slot][0]
                            inform_value = item[0]
                            sentence = sentence.replace("*found_slot_instance*", "\"{}\"".format(inform_value))
                        else: #slot mà user request của kết quả trả về là list rỗng
                            # inform_value = "không có thông tin này"
                            sentence = EMPTY_SLOT[0].replace("*request_slot*",AGENT_INFORM_OBJECT[inform_slot])

                        list_sentence.append(sentence)
                    # print(agent_intent)
                    # print(list_sentence)
            else:
                # print('here')
                sentence = random.choice(MATCH_FOUND['found_major'])
                ## add list_sentence
                list_sentence.append(sentence)

            # response_obj = ''

            # sentence += "\n" + response_obj + response_match
            # print("-----------------------------match sentence")
            # print(sentence)


    # if list_sentence:
    sentence_res = [item.replace(r'"',r'') for item in list_sentence]
    # else:
    #     sentence_res = sentence.replace(r'"',r'')
    # print("sentence_res",sentence_res)

    # print('='*50)
    # print("Agent's intent: {}".format(agent_intent))
    # print("Agent's inform slots: {}".format(inform_slot))
    # print("Agent's inform values: {}".format(inform_value))
    # print("Natural sentence: {}".format(sentence_res))
    # print('='*50)
    return sentence_res
