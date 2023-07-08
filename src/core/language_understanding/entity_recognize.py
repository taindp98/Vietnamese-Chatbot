import os
from .utils import load_pattern, find_entity_longest_common
from collections import OrderedDict
import string
import regex as re
from .intent_recognize import IntentRecognition

class EntityRecognition:
    def __init__(self, root: str) -> None:

        self.dict_entity = load_pattern(os.path.join(root, "entity.json"))
        self.map_order_entity = load_pattern(os.path.join(root, "map_order_entity.json"))
        for key, value in self.map_order_entity.items():
            if not key.endswith('inform') and key != 'not_intent':
                self.map_order_entity[key] = self.map_order_entity[key] + [key]

        self.define_compare = load_pattern(os.path.join(root, "comparison.json"))
    
    def catch_point(self, mess: str):
        compare_flag = 'lte'
        for key in list(self.define_compare.keys()):
            for value in self.define_compare[key]:
                if (mess.find(value) != -1):
                    compare_flag = key
                else:
                    continue

        define_regex_point = r"\d*\.\d+|\d+"

        ## split to word
        words = mess.split(' ')
        list_alphabet = list(string.ascii_lowercase) + list(string.ascii_uppercase)

        viet_string = 'áàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệóòỏõọôốồổỗộơớờởỡợíìỉĩịúùủũụưứừửữựýỳỷỹỵđ'
        for v in viet_string:
            list_alphabet.append(v)
        list_point_regex = []
        for w in words:
            if not w.startswith(tuple(list_alphabet)):
                list_point_regex += re.findall(define_regex_point,w)
        
        list_point_float = [float(item) for item in list_point_regex]
        list_point_sort = sorted(list_point_float)

        list_point_res = []
        if len(list_point_sort) == 1:
            if compare_flag == 'lte':
                if list_point_sort[0] < 100 and list_point_sort[0] >= 30:
                    list_point_res.append(float(30))
                    list_point_res.append(list_point_sort[0])

                elif list_point_sort[0] < 1000 and list_point_sort[0] >= 100:
                    list_point_res.append(float(100))
                    list_point_res.append(list_point_sort[0])
                elif list_point_sort[0] < 30:
                    list_point_res.append(float(0))
                    list_point_res.append(list_point_sort[0])
            else:
                if list_point_sort[0] < 100 and list_point_sort[0] >= 30:
                    list_point_res.append(list_point_sort[0])
                    list_point_res.append(float(100))

                elif list_point_sort[0] < 1000 and list_point_sort[0] >= 100:
                    list_point_res.append(list_point_sort[0])
                    list_point_res.append(float(1000))
                elif list_point_sort[0] < 30:
                    list_point_res.append(list_point_sort[0])
                    list_point_res.append(float(30))

        elif len(list_point_sort) > 1 and max(list_point_sort) < 1000:
            if len(list_point_sort) == 2:
                list_point_res = list_point_sort.copy()
            else:
                list_point_res.append(list_point_sort[-2])
                list_point_res.append(list_point_sort[-1])

        return list_point_res, list_point_regex

    def find(self, intent: str, mess: str):
        result_entity_dict={}
        entity_to_thres={}
        for ent in self.map_order_entity[intent]:
            # threshold wordnumber
            if ent in ['subject','tuition', 'subject_group','major_code','year']:
                entity_to_thres[ent]=1
            elif ent in ['major_name','type_edu']:
                entity_to_thres[ent]=2
            elif ent in ['case']:
                entity_to_thres[ent]=3
            else:
                entity_to_thres[ent]=4

        ordered_real_dict = OrderedDict()
        for ent in self.map_order_entity[intent]:
            ordered_real_dict[ent] = self.dict_entity[ent]
        for ent, list_entity in ordered_real_dict.items():
            if ent == 'type_edu':
                matching_threshold = 0.2
            elif ent == 'subject':
                matching_threshold = 0.55
            elif ent == 'major_name':
                matching_threshold = 0.35
            elif ent == 'case':
                matching_threshold = 0.4

            else:
                matching_threshold = 0.1
            catch_entity_threshold_loop = 0
            while True:
                if catch_entity_threshold_loop > 3:
                    break
                list_longest_entity = find_entity_longest_common(mess, list_entity)
                if list_longest_entity == []:
                    break
                if list_longest_entity[0]['longest_common_length'] < entity_to_thres[ent] :
                    break

                list_sentence_token = mess.split(' ')
                greatest_common_length = None
                greatest_end_common_index = None
                max_match_entity = 0.0
                for dict_longest_common_entity in list_longest_entity:
                    longest_common_entity_index = dict_longest_common_entity['longest_common_entity_index']
                    longest_common_length = dict_longest_common_entity['longest_common_length']
                    end_common_index = dict_longest_common_entity['end_common_index']
                    list_sentence_token_match = list_sentence_token[
                        end_common_index - longest_common_length+1:end_common_index+1
                    ]

                    list_temp_longest_entity_token = str(list_entity[longest_common_entity_index]).split(' ')
                    score = len(list_sentence_token_match)/float(len(list_temp_longest_entity_token))
                    if score > max_match_entity:
                        max_match_entity = score
                        greatest_common_length = longest_common_length
                        greatest_end_common_index = end_common_index
                if greatest_common_length >= entity_to_thres[ent] and max_match_entity > matching_threshold:
                    start_idx = greatest_end_common_index - greatest_common_length +1
                    end_idx = greatest_end_common_index +1
                    result = ' '.join(
                        list_sentence_token[start_idx:end_idx]
                    )

                    if ent in result_entity_dict:
                        result_entity_dict[ent].append(result)
                    else:
                        result_entity_dict[ent] = [result]
                    list_sentence_token[start_idx:end_idx] = ["✪"] * greatest_common_length
                    mess = ' '.join(list_sentence_token)
                catch_entity_threshold_loop += 1
        
        point_entity, list_point_regex = self.catch_point(mess)
        list_entity_found = list(result_entity_dict.values())
        confirm_obj = None
        if list_entity_found:
            for p in list_point_regex:
                for sublist_entity in list_entity_found:
                    for e in sublist_entity:

                        if p not in e and point_entity:
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

        return result_entity_dict, confirm_obj
    
if __name__ == "__main__":

    # mess1 = 'cho em hỏi khối nào thi môn hoá học'
    # s = 'Thi khối B cần học những môn nào?'
    s = 'cho em xin Chỉ tiêu tuyển sinh năm 2020 của khối A1 ngành điện điện tử?'
    # #
    entity_recognizer = EntityRecognition()
    intent_recognizer = IntentRecognition()
    intent_catched, prob, mess = intent_recognizer.predict(s)
    print('intent',intent_catched)
    entity_dict,confirm = entity_recognizer.find(intent_catched, mess)
    print('entity_dict',entity_dict)
    # print("confirm",confirm)
