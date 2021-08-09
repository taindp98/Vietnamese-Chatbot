dict_business_intent = {}

# dict_business_intent["duration"] = ["mấy năm","chừng nào","tới chừng nào","tới mấy năm","bao lâu","may nam","chung nao","học có lâu không","có lâu không","bốn năm","4 năm","5 năm","năm năm","bao nhiêu năm","bao lau","bao nhieu nam","bao nhiêu học kỳ","bao nhiêu học kì","mấy học kì","mấy học kỳ","may hoc ky","may hoc ki","có lâu","lâu"]

# dict_business_intent["location"] = ["học ở đâu","học ở chỗ nào","học ở cs nào","học ở cơ sở nào","hoc o cho nao","hoc o cs nao","học ở cơ sở 1","học ở cở sở 2","học ở cs1","học ở cs2","học ở nước ngoài","nước nào","nuoc ngoai","nuoc nao","học ở mỹ","học ở nhật"]

# dict_business_intent["public_transport"] = ["buýt","xe buýt","bus","xe buyt","buyt","tuyến xe","xe số","xe bus","xe số mấy","xe so may","bus so may","xe buýt nào","xe buyt nao","xe nao","xe nào","tuyến nào","tuyen nao","tuyến số mấy","số mấy","tuyen so may","so may","trạm xe buýt","trạm xe số mấy","tram bus","trạm bus","trạm nào","trạm dừng","trạm","tram"]

# dict_business_intent["accommodation"] = ["chỗ ở","ở chỗ nào","có chỗ ở","ktx","ký túc xá","kí túc xá","ky tuc xa","ki tuc xa","nên ở đâu","ở đâu","chỗ ăn chỗ ở","cho an cho o","nhà trọ","nha tro","nhà ở","nha o","cho o","cho an","ở trọ","o tro","nhà trọ","phòng trọ","phong tro","chung cu","chung cư","thuê phòng","thuê nhà","nha tro"]

# dict_business_intent["address"] = ["địa chỉ","cơ sở 2 ở đâu","cơ sở 1 ở đâu","cs2","cs1","cs2 ở đâu","cs1 ở đâu","địa chỉ cs2","địa chỉ cs1","địa chỉ của trường","dia chi","dia chi cs2","dia chi cs1","ben tre","bến tre"]

# dict_business_intent["out_come"] = ["yêu cầu đầu ra","chuẩn đầu ra","đầu ra","dau ra","yeu cau dau ra","chuan dau ra","chuẩn ra trường","chuẩn tốt nghiệp","yêu cầu tốt nghiệp","chuan tot nghiep","chuan ra truong","chuẩn tiếng anh","chuan tieng anh","chuẩn ngoại ngữ","chuan ngoai ngu","yêu cầu tiếng anh","yêu cầu ngoại ngữ","yeu cau ngoai ngu"]

dict_business_intent["subject_group"] = ['khối','tổ hợp khối','khói','khoi']

dict_business_intent["tuition"] = ["học phí","hoc phí","học phi","hoc phi","mắc","có mắc","rẻ","có rẻ","đắt","có đắt","đắc","có đắc","học phí là bao nhiêu","học phí bao nhiêu","tiền học","tiền","tien hoc","giá","giá tín chỉ","giá tiền","gia tien","giá tiền của"]

dict_business_intent["point"] = ['điểm','điểm chuẩn',"nhiêu điểm","bao nhiêu điểm","mấy điểm","điểm bao nhiêu","điểm thi bao nhiêu","điểm đạt không","điểm tốt không","điểm thấp không","thi nhiêu điểm","điểm nhiêu","mấy điểm","được nhiêu","công bố điểm thi","điểm nhiêu","mấy điểm","điểm bao nhiêu","nhieu diem","được nhiêu điểm","mấy điểm","điểm bao nhiêu","bao nhiêu điểm","có nhiêu điểm","mấy điểm","đậu hông","may diem","điểm bao nhiêu","bao nhieu diem","kết quả thi","điểm xét tuyển bao nhiêu","bao nhieu diem","điểm bao nhiêu","nhiêu điểm","mấy điểm","bao nhiu diem","diem bao nhiu","may diem","nhiêu điểm","được nhiêu","điểm thi bao nhiêu","điểm mấy","thi nhiêu điểm","bao nhiêu điểm","mấy điểm","điểm thế nào","điểm sao rồi","điểm ổn không","điểm nhiêu","điểm thế nào","bao nhiêu điểm","bao nhieu điểm","mấy điểm đậu","bao nhiều điểm","bao nhiêu điểm","mấy điểm","điểm bao nhiêu","bao nhiêu điểm"]

dict_business_intent["major_code"] = ["mã",'ma']

dict_business_intent["subject"] = ["môn thi","mon thi","môn nào","mon nao","tổ hợp","tổ hợp môn","môn"]

dict_business_intent['object'] = ['đối tượng','doi tuong','thí sinh','thi sinh', 'đôi tuong','doi tượng']

dict_business_intent['major_name'] = ['ngành nào','tên ngành','nganh nao']

dict_business_intent['register'] = ['làm thế nào','đăng ký','đăng kí','dang ki','dang ky','nộp','ứng tuyển','dự tuyển','ung tuyen','du tuyen']

dict_business_intent['criteria'] = ['chỉ tiêu','chi tieu']

dict_business_intent['year'] = ['năm nào']

dict_random_intent = {}

# dict_random_intent["anything"] = ["sao cũng được","gì cũng được","anything","s cũng được",'j cũng được',"không biết","k biết","ko biết","không nhớ","ko nhớ","k nhớ","không rõ","k rõ","ko rõ","cũng được","cũng ok","cũng không sao","cũng dc","cũng k sao","cũng ko sao"]
# dict_random_intent["hello"] = ["chào"," xin chào","chao","xin chao","hello","chao buoi sang","chào buổi sáng","hi "]
# dict_random_intent["done"] = ["tạm biệt","bye bye","pp","tam biet","bye"]
# dict_random_intent["thanks"] = ["đúng","phải rồi","ok","ừ","ừm","oke","yes","hay quá","cảm ơn","cam on","tks","thanks","thank","thank u","thank you","cám ơn","ty","đúng rồi","tốt lắm","cảm ơn nha","vang","vâng","đúng vậy","chính xác"]

###
#INTENT MESSAGE SIGNALS
list_question_signal = [" hả ","chứ","có biết","phải không","đâu","là sao","nào","khi nào","nơi nào","không ạ","k ạ","là sao","nữa vậy","chưa á","ko ạ","sao ạ","chưa ạ","sao vậy","không vậy","k vậy","ko vậy","chưa vậy","thế"," nhỉ "," ai"," ai ","ở đâu","ở mô","đi đâu","bao giờ","bao lâu","khi nào","lúc nào","hồi nào","vì sao","tại sao","thì sao","làm sao","như nào","thế nào","cái chi","gì","bao nhiêu","mấy","?"," hả ","được không","được k","được ko","vậy ạ","nào vậy","nào thế","nữa không","đúng không","đúng k","đúng ko","nữa k","nữa ko","nào ấy","nào ạ"]
list_question_signal_last = ["vậy","chưa","không","sao","à","hả","nhỉ","thế"]
list_object = ["bạn","cậu","ad","anh","chị","admin","em","mày","bot"]
list_subject = ["mình","tôi","tớ","tao","tui","anh","em"]
list_verb_want = ["hỏi","biết","xin"]
list_verb_have = ["có","được"]

#intent not want information
list_hello_notification = ["hello","chào","helo",'hi']
list_done_notification = ["bye","tạm biệt","bai","gặp lại",'pp']
list_thanks_notification = ["cảm ơn","tks","thanks",'thank']
list_anything_notification = ["sao cũng được","gì cũng được","anything","s cũng được",\
    'j cũng được',"không biết","k biết","ko biết","không nhớ","ko nhớ","k nhớ","không rõ",\
        "k rõ","ko rõ","cũng được","cũng ok","cũng không sao","cũng dc","cũng k sao","cũng ko sao"]

#intent agree or disagree

list_agree_notification = ['yes','ok','đúng rồi','đúng','chắc vậy','chính xác','phải rồi','vâng']
list_disagree_notification = ['không phải','no','sai rồi','sai']


THRESHOLD_DISTANCE_SIGNAL_QUESTION = 0.5
THRESHOLD_PRED_INTENT = {
    # 'other':0.9,
    'type_edu': 0.82,
    'case': 0.82,
    'career': 0.8
}

THRESHOLD_EDIT_DIST = 0.85
