from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk
import json

# Import JSON Path
f = open('./data/dict_entity_mar22.json', encoding="utf8")

# Load JSON file
data = json.load(f)

# Define Dictionaries
result_dt = {}
data_dt = {}

# Convert JSON to Dictionary
for i in data:
    data_dt.update(i)

# Processing subject_group
sub_group1 = []
sub_group2 = []
sub_group3 = []
sub_group4 = []
sub_group5 = []
sub_group6 = []
sub_group7 = []

for key in data_dt:
    if key == "subject_group":
        for value in data_dt[key]:
            if value == "a00" or value == "a":
                sub_group1.append(value)
            if value == "a01" or value == "a1":
                sub_group2.append(value)
            if value == "d01" or value == "d1":
                sub_group3.append(value)
            if value == "d07" or value == "d7":
                sub_group4.append(value)
            if value == "b00" or value == "b":
                sub_group5.append(value)
            if value == "v00" or value == "v":
                sub_group6.append(value)
            if value == "v01" or value == "v1":
                sub_group7.append(value)
    else: pass
sub_group = [sub_group1, sub_group2, sub_group3, sub_group4, sub_group5, sub_group6, sub_group7]

data_dt.update({'subject_group': sub_group})

# Create Combobox
def Combobox(dispname, dictinput, y_place):
    key, value = list(dictinput.items())[0]

    option = list(dictinput.values())  
    newlist = []
    for i in option:
        for j in i:
            newlist.append(j)

    variable = StringVar()

    tk.Label(master, text=dispname, background="#CEE3F6").place(x = 120, y = y_place)                     
    menu = ttk.OptionMenu(master, variable, variable, *newlist)          
    
    menu.config(width=30) 
    menu.place(x = 180, y = y_place + 22)

    def check(*args):
        # Processing subject in subject_group
        if key == "subject_group":
            if 'a00' in variable.get():
                result_dt.update({key.lower(): sub_group1})
                result_dt.update({"subject": ["toán", "vật lý", "hóa học"]})
            elif 'a01' in variable.get():
                result_dt.update({key.lower(): sub_group2})
                result_dt.update({"subject": ["toán", "vật lý", "tiếng anh"]})
            elif 'd01' in variable.get():
                result_dt.update({key.lower(): sub_group3})
                result_dt.update({"subject": ["toán", "tiếng anh", "ngữ văn"]})
            elif 'd07' in variable.get():
                result_dt.update({key.lower(): sub_group4})
                result_dt.update({"subject": ["toán", "hóa học", "tiếng anh"]})
            elif 'b00' in variable.get():
                result_dt.update({key.lower(): sub_group5})
                result_dt.update({"subject": ["toán", "hóa học", "sinh học"]})
            elif 'v00' in variable.get():
                result_dt.update({key.lower(): sub_group6})
                result_dt.update({"subject": ["toán", "vật lý", "vẽ hình họa mỹ thuật"]})
            elif 'v01' in variable.get():
                result_dt.update({key.lower(): sub_group7})
                result_dt.update({"subject": ["toán", "ngữ văn", "vẽ hình họa mỹ thuật"]})

        else: result_dt.update({key.lower(): variable.get()})

    variable.trace('w', check)

# Main function
def main():
    global master
    master = tk.Tk()
    master.geometry("1200x800+400+50")
    master.title('Admin Tool')
    master.config(background="#CEE3F6")

    # Create Combobox
    combox1 = Combobox("Mã ngành", {"major_code": data_dt['major_code']}, 20)
    combox2 = Combobox("Chuyên ngành", {"major_name": data_dt['major_name']}, 80)
    combox3 = Combobox("Hình thức đào tạo", {"type_edu": data_dt['type_edu']}, 140)
    combox4 = Combobox("Năm", {"year": data_dt['year']+['2021','2022']}, 200)
    combox5 = Combobox("Định hướng nghề nghiệp", {"career": data_dt['career']}, 260)
    combox7 = Combobox("Học phí", {"tuition": data_dt['tuition']}, 320)
    combox8 = Combobox("Khối", {"subject_group": data_dt['subject_group']}, 380)
    combox9 = Combobox("Phương thức tuyển sinh", {"case": data_dt['case']}, 440)
    combox10 = Combobox("Đối tượng tuyển sinh", {"object": data_dt['object']}, 500)
    combox11 = Combobox("Đăng ký", {"register": data_dt['register']}, 560)
    
    point_st = tk.StringVar()
    criteria_st = tk.StringVar()
    
    # Submit Button
    def submit_button():
        output = tk.StringVar()
        point = point_st.get()
        criteria = criteria_st.get()
        result_dt.update({"point":point, "criteria":criteria})

        text = Text(master)
        text.pack(expand=YES, fill=BOTH)
        text.place(x = 500, y = 50)

        text.insert(END, str(result_dt))

    tk.Label(master, text='Output:', background="#CEE3F6").place(x = 500, y = 30)

    tk.Label(master, text='Điểm', background="#CEE3F6").place(x = 120, y = 650)
    point = tk.Entry(master, textvariable = point_st)                                       
    point.config(width=7)
    point.place(x = 160, y = 650)

    tk.Label(master, text='Chỉ tiêu', background="#CEE3F6").place(x = 220, y = 650)
    criteria = tk.Entry(master, textvariable = criteria_st)          
    criteria.config(width=7)
    criteria.place(x = 270, y = 650)

    button = Button(master, text="Submit", command=submit_button).place(x = 220, y = 700)                    

    mainloop()

    # print(result_dt)

    return result_dt 

# Execuse File
main()