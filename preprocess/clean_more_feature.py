from data.case_admission import list_case
from utils import clean_mess,export_pickle_file
# for item in list_case:
for key in list(list_case.keys()):
    case = list_case[key]
    for subkey in list(case.keys()):
        case[subkey] = [clean_mess(subitem) for subitem in case[subkey]]
print(list_case)
export_pickle_file(list_case,'/home/taindp/PycharmProjects/thesis/data/list_case_clean.pkl')
