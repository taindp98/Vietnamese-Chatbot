from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk
import json

# Import JSON Path
f = open('./data/entity_admin.json', encoding="utf8")

# Load JSON file
data = json.load(f)

# Define Dictionaries
result_dt = {}
data_dt = {}

# Convert JSON to Dictionary
for component in data:
    data_dt.update(component)

# Create Combobox
def Combobox(dispname, dictinput, y_place):
    key, value = list(dictinput.items())[0]

    option = list(dictinput.values()) 
    newlist = [" "]

    for i in option:
        for j in i:    
            newlist.append(str(j).replace("['","").replace("']","").replace("', '",", "))

    variable = StringVar()

    tk.Label(master, text=dispname, background="#CEE3F6").place(x = 120, y = y_place)                     
    menu = ttk.OptionMenu(master, variable, *newlist)        
    
    menu.config(width=30) 
    menu.place(x = 180, y = y_place + 22)
    
    def check(*args):
        # Processing subject in subject_group, type in type_value
        if key == "subject_group":
            if "a00" in variable.get():
                result_dt.update({key.lower(): [variable.get().replace(", ","', '")]})
                result_dt.update({"subject": ["toán", "vật lý", "hóa học"]})
            elif "a01" in variable.get():
                result_dt.update({key.lower(): [variable.get().replace(", ","', '")]})
                result_dt.update({"subject": ["toán", "vật lý", "tiếng anh"]})
            elif "d01" in variable.get():
                result_dt.update({key.lower(): [variable.get().replace(", ","', '")]})
                result_dt.update({"subject": ["toán", "tiếng anh", "ngữ văn"]})
            elif "d07" in variable.get():
                result_dt.update({key.lower(): [variable.get().replace(", ","', '")]})
                result_dt.update({"subject": ["toán", "hóa học", "tiếng anh"]})
            elif "b00" in variable.get():
                result_dt.update({key.lower(): [variable.get().replace(", ","', '")]})
                result_dt.update({"subject": ["toán", "hóa học", "sinh học"]})
            elif "v00" in variable.get():
                result_dt.update({key.lower(): [variable.get().replace(", ","', '")]})
                result_dt.update({"subject": ["toán", "vật lý", "vẽ hình họa mỹ thuật"]})
            elif "v01" in variable.get():
                result_dt.update({key.lower(): [variable.get().replace(", ","', '")]})
                result_dt.update({"subject": ["toán", "ngữ văn", "vẽ hình họa mỹ thuật"]})

        else: result_dt.update({key.lower(): [variable.get().replace(", ","', '")]})

    variable.trace('w', check)

# Main function
def main():
    global master
    master = tk.Tk()
    master.geometry("1280x720+400+50")
    master.title('Admin Tool')
    master.config(background="#CEE3F6")

    # Create Combobox
    combox1 = Combobox("Mã ngành", {"major_code": data_dt['major_code']}, 20)
    combox2 = Combobox("Chuyên ngành", {"major_name": data_dt['major_name']}, 80)
    combox3 = Combobox("Hình thức đào tạo", {"type_edu": data_dt['type_edu']}, 140)
    combox4 = Combobox("Năm", {"year": data_dt['year']}, 200)
    combox5 = Combobox("Định hướng nghề nghiệp", {"career": data_dt['career']}, 260)
    combox7 = Combobox("Học phí", {"tuition": data_dt['tuition']}, 320)
    combox8 = Combobox("Khối", {"subject_group": data_dt['subject_group']}, 380)
    combox9 = Combobox("Phương thức tuyển sinh", {"case": data_dt['case']}, 440)
    combox10 = Combobox("Đối tượng tuyển sinh", {"object": data_dt['object']}, 500)
    combox11 = Combobox("Đăng ký", {"register": data_dt['register']}, 560)
    
    point_st = tk.StringVar()
    criteria_st = tk.StringVar()

    text = Text(master)
    text.pack(expand=YES, fill=BOTH)
    text.place(x = 600, y = 55)

    # Submit Button
    def submit_button():
        output = tk.StringVar()
        point = point_st.get()
        criteria = criteria_st.get()
        result_dt.update({"point":point, "criteria":criteria})

        text = Text(master)
        text.pack(expand=YES, fill=BOTH)
        text.place(x = 600, y = 55)
        
        text.insert(END, str(result_dt).replace('["' , "['").replace('"]' , "']"))

    tk.Label(master, text='Output:', background="#CEE3F6").place(x = 600, y = 30)

    tk.Label(master, text='Điểm', background="#CEE3F6").place(x = 120, y = 650)
    point = ttk.Entry(master, textvariable = point_st)                                       
    point.config(width=7)
    point.place(x = 157, y = 651)

    tk.Label(master, text='Chỉ tiêu', background="#CEE3F6").place(x = 250, y = 650)
    criteria = ttk.Entry(master, textvariable = criteria_st)          
    criteria.config(width=7)
    criteria.place(x = 300, y = 651)

    button = ttk.Button(master, text="Submit", command=submit_button).place(x = 220, y = 685)            

    mainloop()

    return result_dt 

# Execuse File
main()