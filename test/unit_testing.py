from preprocess.normalize_typing import chuan_hoa_dau_cau_tieng_viet
from entity.confirm_object import catch_point,normalize_format_number
import os

_PATH_CURRENT = '/home/taindp/PycharmProjects/thesis'
_PATH_TYPING_FILE = os.path.join(_PATH_CURRENT,'test_case','unit_test','typing.txt')

_PATH_POINT_FILE = os.path.join(_PATH_CURRENT,'test_case','unit_test','point.txt')

# case_open = open(_PATH_TYPING_FILE,'r')
case_open = open(_PATH_POINT_FILE,'r')

list_case = case_open.readlines()
# print(list_word)
def unit_test(list_case):
    count_pass = 0
    for idx, items in enumerate(list_case):
        # items = items.replace('\n','').replace(', ',',').split(',')
        items = items.replace('\n','').split('#')
        raw_word,fine_word = items[0],items[1].split('-')

        # fine_word = [float(item) for item in fine_word]

        print('='*50)
        print('Test case: {}'.format(idx))
        print('Input: {}'.format(raw_word))
        print('Expect output: {}'.format(fine_word))

        confirm_obj,list_point_regex = catch_point(normalize_format_number(raw_word))
        confirm_obj = [str(item) for item in confirm_obj]
        if fine_word == confirm_obj:
        # if fine_word == chuan_hoa_dau_cau_tieng_viet(raw_word):
            count_pass += 1

            # print('Actual output: {}'.format(chuan_hoa_dau_cau_tieng_viet(raw_word)))
            print('Pass: {}'.format('Success'))

        elif fine_word == ['EMPTY'] and not confirm_obj:
            count_pass += 1
            print('Pass: {}'.format('Success'))
        else:
            # print('Actual output: {}'.format(chuan_hoa_dau_cau_tieng_viet(raw_word)))
            print('Actual output: {}'.format(confirm_obj))
            print('Pass: {}'.format('Fail'))
        # else:
            # print(items)
    print('Pass Rate: {0}/{1}'.format(count_pass,len(list_case)))
    
unit_test(list_case)


