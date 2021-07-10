import re
import string

DEFINE_COMPARE = {}
DEFINE_COMPARE['lte'] = ["thấp","thap","thấp hơn","thap hon","giảm","tuột","nhỏ","nhỏ hơn","dưới","dưới mức","ít","ít hơn","tới","toi","đến","den","cỡ","khoảng","tầm","khoang","tam","đạt","được","dat","duoc","dc","đc"]
DEFINE_COMPARE['gte'] = ["cao","cao hơn","tren","cao hon","tăng","trên","trên mức","nhiều","nhiều hơn","từ","tu"]


def normalize_format_number(mess):
    decmark_reg = re.compile('(?<=\d),(?=\d)')

    mess_norm = decmark_reg.sub('.',mess)

    return mess_norm


def catch_point(mess):

    compare_flag = 'lte'
    for key in list(DEFINE_COMPARE.keys()):
        for value in DEFINE_COMPARE[key]:
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
    # print('list_point_regex',list_point_regex)

    # list_point_regex = re.findall(define_regex_point,mess)
    # print(list_point_regex)
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
        # print(len(list_point_sort))
        if len(list_point_sort) == 2:
            list_point_res = list_point_sort.copy()
        else:
            list_point_res.append(list_point_sort[-2])
            list_point_res.append(list_point_sort[-1])

    return list_point_res,list_point_regex

# mess = 'cho em hỏi ngành kỹ thuật hóa học phải thi khối d07 đúng không ạ'
# mess = 'Cho em hỏi ngành công nghệ kỹ thuật hóa học, xét bằng học bạ đc 84,6 thì có cơ hội không ạ, em cảm ơn ạ'
# mess = 'cho em xin Chỉ tiêu tuyển sinh năm 2019 của khối A1 ngành điện điện tử?'
# confirm_obj,list_point_regex = catch_point(normalize_format_number(mess))
# print(confirm_obj)
# print(clean_mess(mess))
