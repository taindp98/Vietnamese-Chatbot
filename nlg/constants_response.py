MATCH_FOUND = {
    'found': [
        "Thông tin *found_slot* bạn cần: *found_slot_instance*"
    ],
    'not_found': [
        "Mình không tìm thấy ngành nào chứa thông tin *found_slot* mà bạn cần, bạn xem lại các thông tin đã cung cấp dưới đây và điều chỉnh lại giúp mình nhé!"
    ],
    'found_major' :[
        "Dưới đây là thông tin bạn cần tìm."
    ]
}
REQUEST = {}
"""
user_known = ['major_name', 'type_edu','subject','subject_group','point', 'year']
# sửa lại dialogue train
'major_code',
'major_name',
'type_edu',
'point',
'subject_group',
'university_code',
'university_name',
'year',



'career',
'company',
'subject',
'tuition_one_credit',
'duration_std',
'credits',
'foreign_lang_min'
"""
###############################################################################################################
REQUEST['major_name'] = [
    'Bạn định hỏi về *major_name* nào? (Vd: khoa học máy tính, điện điện tử, cơ khí, ...)',
    '*major_name* là gì vậy bạn? (Vd: khoa học máy tính, điện điện tử, cơ khí, ...)',
    'Bạn cần thông tin về *major_name* nào? (Vd: khoa học máy tính, điện điện tử, cơ khí, ...)'
]
REQUEST['type_edu'] = [
    '*type_edu* bạn cần tìm là gì vậy ạ? (Vd: đại trà,chất lượng cao, tiên tiến)',
    'Bạn muốn tìm thông tin về *type_edu* nào? (Vd: đại trà,chất lượng cao, tiên tiến)'
]
REQUEST['point'] = [
    'Bạn muốn tra cứu mức *point* thế nào ạ?',
    'Bạn muốn tìm ngành với *point* tầm bao nhiêu ạ?',
    'Cho mình xin thêm thông tin về *point* mong muốn của bạn được không?'
]
REQUEST['subject_group'] = [
    'Bạn muốn tra cứu *subject_group* nào bạn?',
    'Cụ thể là *subject_group* nào vậy bạn?',
    'Mời bạn cung cấp thông tin *subject_group* '
]

REQUEST['subject'] = [
    'Bạn muốn tìm *subject* nào vậy bạn?',
    # 'Cụ thể là *subject* nào vậy bạn?',
    # 'Mời bạn cung cấp thông tin *subject* '
]

REQUEST['year'] = [
    'Bạn cho mình xin *year* cụ thể bạn muốn tìm nha!',
    '*year* bao nhiêu vậy bạn?'
]

REQUEST['case'] = [
    'Bạn cho mình xin *case* cụ thể bạn muốn tìm nha! (Vd: thi tốt nghiệp, đánh giá năng lực, ưu tiên xét tuyển)',
    '*case* bạn cần tìm là gì vậy ạ? (Vd: thi tốt nghiệp, đánh giá năng lực, ưu tiên xét tuyển)'
]

REQUEST['criteria'] = [
    'Bạn cho mình xin *criteria* cụ thể bạn muốn tìm nha!',
    '*criteria* bạn cần tìm là gì vậy ạ?'
]

REQUEST['object'] = [
    'Bạn thuộc *object* nào vậy ạ? (Vd: thi tốt nghiệp, trường chuyên, học sinh giỏi quốc gia,...)'
]

REQUEST['register'] = [
    'Bạn muốn *register* theo hình thức nào vậy ạ?',
    'Bạn muốn lựa chọn hình thức *register* như thế nào vậy ạ? (Vd: đăng ký thi tốt nghiệp, đăng ký ưu tiên xét tuyển,...)'
]
REQUEST['major_code'] = [
    'Bạn cho mình xin *major_code* cụ thể bạn muốn tìm nha!',
    '*major_code* bạn cần tìm là bao nhiêu vậy ạ?'
]

REQUEST['tuition'] = [
    'Bạn cho mình xin mức *tuition* cụ thể bạn muốn tìm nha!'
]

REQUEST['career'] = [
    '*career* bạn cần tìm là gì vậy ạ?'
]

REQUEST_REPEAT = [
    'Thông tin *request_key* bạn nhập vào chưa rõ ràng, bạn cung cấp lại giúp mình thông tin này nhé! ',
    'Rất tiếc, thông tin *request_key* bạn nhập vào mình vẫn chưa rõ, bạn vui lòng cung cấp lại thông tin này giúp mình nhé!',
    'Bạn cung cấp lại thông tin *request_key* giúp mình với nhé!'
]
################################################################################

INFORM = {}

INFORM['major_code'] = [
    '*major_code_instance* có phải là *major_code* bạn muốn tìm không?'
]
INFORM['major_name'] = [
    '*major_name_instance* có phải là *major_name* bạn đang tìm kiếm không ?'
]
INFORM['type_edu'] = [
    'có phải bạn muốn hỏi về chương trình *type_edu_instance* không?',
    '*type_edu_instance* có phải là *type_edu* bạn muốn tìm không?'
]
INFORM['point'] = [
    '*point_instance* có phải mức *point* cho ngành bạn đang tìm kiếm không ?'
]
INFORM['subject_group'] = [
    'có phải bạn muốn hỏi về *subject_group_instance* không?',
    '*subject_group_instance* có phải là *subject_group* bạn muốn tìm không?'
]

INFORM['year'] = [
    'năm *year_instance* có phải là năm bạn tìm kiếm ?'
]

INFORM['career'] = [
    '*career_instance* có phải là *career* của ngành bạn cần tìm ?'
]
INFORM['subject'] = [
    '*subject_instance* thuộc tổ hợp *subject* cho ngành bạn cần tìm phải không ?'
]
INFORM['tuition'] = [
    '*tuition_instance* là *tuition* cho chương trình đào tạo bạn cần tìm phải không ?'
]

INFORM['major'] = [
    'Đây là ngành mình tìm được với yêu cầu hiện tại của bạn: *major_instance*'
]

INFORM['case'] = [
    '*case* bạn cần tìm là *case_instance* phải không ạ ?'
]

INFORM['criteria'] = [
    '*criteria* hiện tại cho chương trình đào tạo bạn cần tìm có phải là *criteria_instance* không ?'
]

INFORM['object'] = [
    'Bạn có phải thuộc *object* là *object_instance* không ?'
]

INFORM['register'] = [
    '*register_instance* có phải là *register* mà bạn lựa chọn không ạ ?'
]

# user_known = ['major_name', 'type_edu','subject','subject_group', 'year']
AGENT_REQUEST_OBJECT = {
    "major_name": "tên ngành",
    "type_edu": "chương trình đào tạo",
    "point": "điểm chuẩn",
    "subject_group": "tổ hợp khối",
    "subject": "môn thi",
    "year":"năm",
    "career": "cơ hội nghề nghiệp",
    "case": "phương thức tuyển sinh",
    "criteria": "chỉ tiêu tuyển sinh",
    "object" : "đối tượng xét tuyển",
    "register": "cách thức đăng ký",
    "major_code": "mã ngành",
    "tuition":"học phí"
}

AGENT_INFORM_OBJECT = {
    "major_name": "tên ngành",
    "type_edu": "chương trình đào tạo",
    "point": "điểm chuẩn",
    "subject_group": "tổ hợp khối",
    "subject": "môn thi",
    "year":"năm",
    "career": "cơ hội nghề nghiệp",
    "case": "phương thức tuyển sinh",
    "criteria": "chỉ tiêu tuyển sinh",
    "object" : "đối tượng tuyển sinh",
    "register": "cách thức đăng ký",
    "major_code": "mã ngành",
    "tuition":"học phí"
}
list_map_key = ["major_name", "point", "subject_group","year"]

GREETING = [
    'Xin chào! Mình là BK Assistant. Mình có thể giúp gì được bạn?',
    'Hi! BK Assistant có thể giúp gì được bạn đây?'
]
DONE = [
    'Cảm ơn bạn, hy vọng bạn hài lòng với trải nghiệm vừa rồi! Bye ',
    'Rất vui được tư vấn cho bạn! Chào bạn nhé!',
    'Hy vọng bạn hài lòng với những gì mình tư vấn. Chào bạn!'
]
DONT_UNDERSTAND = [
    'Xin lỗi, mình không hiểu. Bạn nói cách khác dễ hiểu hơn được không?',
    'Mình không hiểu ý bạn lắm'
]

NOT_FOUND = [
    'Mình không tìm thấy ngành nào thỏa mãn các thông tin bạn đã cung cấp, vui lòng điều chỉnh lại giúp mình nhé!'
]
EMPTY_SLOT = [
    'Bạn muốn tìm thông tin với *request_slot* nào cũng được đúng không ạ ?'
]
