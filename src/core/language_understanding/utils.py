import regex as re
from .vietnamese_standardize import VietnameseStandardize
import json


def load_pattern(pattern_file_path: str) -> dict:
    """
    Loading the pattern of intents
    args:
        - pattern_file_path: Path to the json file containing the patterns
    return:
        - the dictionary of content
    """
    return json.load(open(pattern_file_path, "r", encoding="utf8"))


def loaddicchar():
    dic = {}
    char1252 = "à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ".split(
        "|"
    )
    charutf8 = "à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ".split(
        "|"
    )
    for i in range(len(char1252)):
        dic[char1252[i]] = charutf8[i]
    return dic


def convert_unicode(txt):
    dicchar = loaddicchar()
    return re.sub(
        r"à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ",
        lambda x: dicchar[x.group()],
        txt,
    )


def normalize_format_number(mess: str):
    decmark_reg = re.compile("(?<=\d),(?=\d)")
    mess_norm = decmark_reg.sub(".", mess)
    return mess_norm


def clean_text(mess: str):
    mess_unic = convert_unicode(mess)
    mess_std = VietnameseStandardize().standardize_sentence(mess_unic).lower()
    mess_norm = normalize_format_number(mess_std)
    mess_rmspectoken = re.findall(
        r"(?i)\b[a-záàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệóòỏõọôốồổỗộơớờởỡợíìỉĩịúùủũụưứừửữựýỳỷỹỵđ0-9\/\-\.]+\b",
        mess_norm,
    )
    mess_norm = " ".join(mess_rmspectoken)
    return mess_norm


def find_entity_equation(sentence, list_entity):
    normalized_sentence = convert_unicode(sentence)
    list_token_sentence = normalized_sentence.split(" ")
    list_result_entity = []
    list_normalized_entity = [convert_unicode(entity) for entity in list_entity]
    for entity in list_normalized_entity:
        list_token_entity = entity.split(" ")
        for i in range(len(list_token_sentence) - len(list_token_entity) + 1):
            if list_token_entity == list_token_sentence[i : i + len(list_token_entity)]:
                list_result_entity.append(entity)
    return list_result_entity


def longest_common_sublist(a, b):
    table = {}
    l = 0
    i_max = None
    j_max = None
    for i, ca in enumerate(a, 1):
        # enumerate(iter,start)
        for j, cb in enumerate(b, 1):
            if ca == cb:
                table[i, j] = table.get((i - 1, j - 1), 0) + 1
                if table[i, j] > l:
                    l = table[i, j]
                    i_max = i
                    j_max = j
    if i_max != None:
        return l, i_max - 1
    return l, i_max


def lcs_length(a, b):
    table = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i, ca in enumerate(a, 1):
        for j, cb in enumerate(b, 1):
            table[i][j] = (
                table[i - 1][j - 1] + 1
                if ca == cb
                else max(table[i][j - 1], table[i - 1][j])
            )
    return table[-1][-1]


def find_entity_longest_common(sentence, list_entity):
    normalized_sentence = convert_unicode(sentence)
    list_token_sentence = normalized_sentence.split(" ")
    dict_max_len = {}
    list_normalized_entity = [str(entity) for entity in list_entity]
    result = []
    longest_common_length = None
    end_common_index = None
    for index, entity in enumerate(list_normalized_entity):
        list_token_entity = entity.split(" ")
        longest_common_length, end_common_index = longest_common_sublist(
            list_token_sentence, list_token_entity
        )
        if longest_common_length != 0:
            dict_max_len[(index)] = {
                "longest_common_length": longest_common_length,
                "end_common_index": end_common_index,
            }
        # list_token_sentence = list_token_sentence[: end_common_index - longest_common_length] + list_token_sentence[end_common_index:]
    max_longest_common_length = 0
    for k, v in dict_max_len.items():
        if v["longest_common_length"] > max_longest_common_length:
            max_longest_common_length = v["longest_common_length"]

    for k, v in dict_max_len.items():
        if v["longest_common_length"] == max_longest_common_length:
            result.append(
                {
                    "longest_common_entity_index": int(k),
                    "longest_common_length": v["longest_common_length"],
                    "end_common_index": v["end_common_index"],
                }
            )
    return result


def check_shorted_entity(path_db_entity):
    with open(path_db_entity, "r") as dict_file:
        dict = json.load(dict_file)
    len_dict = {}
    for item in dict.keys():
        shorted = 100
        for ele in dict[item]:
            ele_ap = []
            ele_split = str(ele).split()
            for i in ele_split:
                if i != " ":
                    ele_ap.append(i)
            ele_len = len(ele_ap)
            if ele_len < shorted:
                shorted = ele_len
        len_dict[item] = shorted
    return len_dict
