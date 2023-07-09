import os
from .utils import load_pattern, find_entity_longest_common
from collections import OrderedDict
import string
import regex as re
from .intent_recognize import IntentRecognition


class EntityRecognition:
    """
    Find the available entities from the input sentence
    """

    def __init__(self, root: str) -> None:
        self.dict_entity = load_pattern(os.path.join(root, "entity.json"))
        self.map_order_entity = load_pattern(
            os.path.join(root, "map_order_entity.json")
        )
        for key, _ in self.map_order_entity.items():
            if not key.endswith("inform") and key != "not_intent":
                self.map_order_entity[key] += [key]

        self.define_compare = load_pattern(os.path.join(root, "comparison.json"))
        self.configs = load_pattern(os.path.join(root, "configs.json"))
        # threshold wordnumber
        self.entity_threshold = {}
        # matching threshold
        self.matching_threshold = {}
        for ent in list(self.dict_entity.keys()):
            self.entity_threshold[ent] = 4
            self.matching_threshold[ent] = 0.1
            for idx, value in enumerate(
                list(self.configs["num_words_entity_threshold"].values())
            ):
                if ent in value:
                    self.entity_threshold[ent] = idx + 1
                    break
            for key, value in list(self.configs["matching_entity_threshold"].items()):
                if ent == key:
                    self.matching_threshold[ent] = value

    def catch_point(self, mess: str):
        compare_flag = "lte"
        for key in list(self.define_compare.keys()):
            for value in self.define_compare[key]:
                if mess.find(value) != -1:
                    compare_flag = key
                else:
                    continue

        define_regex_point = r"\d*\.\d+|\d+"
        words = mess.split(" ")
        list_alphabet = [string.ascii_lowercase] + [string.ascii_uppercase]

        viet_string = (
            "áàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệóòỏõọôốồổỗộơớờởỡợíìỉĩịúùủũụưứừửữựýỳỷỹỵđ"
        )
        for v in viet_string:
            list_alphabet.append(v)
        list_point_regex = []
        for w in words:
            if not w.startswith(tuple(list_alphabet)):
                list_point_regex += re.findall(define_regex_point, w)

        list_point_float = [float(item) for item in list_point_regex]
        list_point_sort = sorted(list_point_float)

        list_point_res = []
        if len(list_point_sort) == 1:
            if compare_flag == "lte":
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

    def _find_one_entity_type(
        self, entity_type: str, query: str, gallery: list, bag_of_entity: dict
    ):
        limit_loop = 0
        while True:
            if limit_loop > 3:
                break
            list_longest_entity = find_entity_longest_common(
                sentence=query, list_entity=gallery
            )
            if len(list_longest_entity) == 0:
                break

            else:
                if (
                    list_longest_entity[0]["longest_common_length"]
                    < self.entity_threshold[entity_type]
                ):
                    break

            list_token = query.split(" ")
            longest_length = None
            longest_last_idx = None
            max_match_entity = 0.0
            for item in list_longest_entity:
                longest_common_entity_index = item["longest_common_entity_index"]
                longest_common_length = item["longest_common_length"]
                end_common_index = item["end_common_index"]
                list_matched_token = list_token[
                    end_common_index - longest_common_length + 1 : end_common_index + 1
                ]

                longest_entity_token = len(
                    str(gallery[longest_common_entity_index]).split(" ")
                )
                score = len(list_matched_token) / longest_entity_token
                if score > max_match_entity:
                    max_match_entity = score
                    longest_length = longest_common_length
                    longest_last_idx = end_common_index
            if (
                longest_length >= self.entity_threshold[entity_type]
                and max_match_entity > self.matching_threshold[entity_type]
            ):
                start_idx = longest_last_idx - longest_length + 1
                end_idx = longest_last_idx + 1
                found_entity = " ".join(list_token[start_idx:end_idx])

                if entity_type not in bag_of_entity:
                    bag_of_entity[entity_type] = []
                bag_of_entity[entity_type].append(found_entity)

                list_token[start_idx:end_idx] = ["✪"] * longest_length
                query = " ".join(list_token)
            limit_loop += 1

        return bag_of_entity

    def find(self, intent: str, mess: str):
        bag_of_entity = {}
        ordered_real_dict = OrderedDict()
        for ent in self.map_order_entity[intent]:
            ordered_real_dict[ent] = self.dict_entity[ent]

        # 1. Skimming all entities pattern in the gallery
        for entity_type, gallery in ordered_real_dict.items():
            bag_of_entity = self._find_one_entity_type(
                entity_type=entity_type,
                query=mess,
                gallery=gallery,
                bag_of_entity=bag_of_entity,
            )
        # 2. Focus on the "point" entity
        point_entity, _ = self.catch_point(mess)
        confirm_obj = None
        if point_entity:
            bag_of_entity["point"] = point_entity
        # 3. Remove the entity if it and intent are the same
        if intent in bag_of_entity:
            value = bag_of_entity.pop(intent)
            confirm_obj = {intent: value}

        return bag_of_entity, confirm_obj


if __name__ == "__main__":
    # mess1 = 'cho em hỏi khối nào thi môn hoá học'
    # s = 'Thi khối B cần học những môn nào?'
    s = "cho em xin Chỉ tiêu tuyển sinh năm 2020 của khối A1 ngành điện điện tử?"
    # #
    entity_recognizer = EntityRecognition()
    intent_recognizer = IntentRecognition()
    intent_catched, prob, mess = intent_recognizer.predict(s)
    print("intent", intent_catched)
    entity_dict, confirm = entity_recognizer.find(intent_catched, mess)
    print("entity_dict", entity_dict)
    # print("confirm",confirm)
