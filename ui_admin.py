from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
import json
import pymongo
import os
from dotenv import load_dotenv

load_dotenv()

conn_str = os.getenv('MONGOLAB_URI')

myclient = pymongo.MongoClient(conn_str)

mydb = myclient["hcmut"]
# mycol = mydb["investigate"]
mycol = mydb['general']

class Main():
    def __init__(self, JSONpath, ImgPath, Consist):
        self.jsonpath = JSONpath
        self.jsonconsist = Consist
        self.result_dt = {}
        self.data_dt = {}
        self.data_cons_dt = {}
        self.point = None
        self.criteria = None
        self.img = ImgPath
        
        self.LoadData()
        self.main()
        
    def LoadData(self):
        f = open(self.jsonpath, encoding="utf8")
        g = open(self.jsonconsist, encoding="utf8")

        data = json.load(f)
        for component in data:
            self.data_dt.update(component)
        
        self.data_cons_dt = json.load(g)


    # Create Combobox
    def Combobox(self, dispname, dictinput, y_place):
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
            # Processing 4 type
            if key == "type_edu":               
                for i in self.data_cons_dt["tuition_type_edu"].keys():
                    if i in variable.get():
                        self.result_dt.update({"tuition": self.data_cons_dt["tuition_type_edu"][i]})
            
            if key == "major_code":
                for i in self.data_cons_dt["career_major_code"].keys():
                    if i in variable.get():
                        self.result_dt.update({"career": self.data_cons_dt["career_major_code"][i]})
            
            if key == "case":
                for i in self.data_cons_dt["object_case"].keys():
                    if i in variable.get():
                        self.result_dt.update({"object": self.data_cons_dt["object_case"][i]})
                        self.result_dt.update({"register": self.data_cons_dt["register_case"][i]})

            # Processing subject in subject_group, type in type_value
            if key == "subject_group":
                if "" in variable.get():
                    self.result_dt.update({key.lower(): []})
                    self.result_dt.update({"subject":[]})
                if "a00" in variable.get():
                    self.result_dt.update({key.lower(): [variable.get().replace(", ","', '")]})
                    self.result_dt.update({"subject": ["toán", "vật lý", "hóa học"]})
                elif "a01" in variable.get():
                    self.result_dt.update({key.lower(): [variable.get().replace(", ","', '")]})
                    self.result_dt.update({"subject": ["toán", "vật lý", "tiếng anh"]})
                elif "d01" in variable.get():
                    self.result_dt.update({key.lower(): [variable.get().replace(", ","', '")]})
                    self.result_dt.update({"subject": ["toán", "tiếng anh", "ngữ văn"]})
                elif "d07" in variable.get():
                    self.result_dt.update({key.lower(): [variable.get().replace(", ","', '")]})
                    self.result_dt.update({"subject": ["toán", "hóa học", "tiếng anh"]})
                elif "b00" in variable.get():
                    self.result_dt.update({key.lower(): [variable.get().replace(", ","', '")]})
                    self.result_dt.update({"subject": ["toán", "hóa học", "sinh học"]})
                elif "v00" in variable.get():
                    self.result_dt.update({key.lower(): [variable.get().replace(", ","', '")]})
                    self.result_dt.update({"subject": ["toán", "vật lý", "vẽ hình họa mỹ thuật"]})
                elif "v01" in variable.get():
                    self.result_dt.update({key.lower(): [variable.get().replace(", ","', '")]})
                    self.result_dt.update({"subject": ["toán", "ngữ văn", "vẽ hình họa mỹ thuật"]})

            else: self.result_dt.update({key.lower(): [variable.get().replace(", ","', '")]})

        variable.trace('w', check)

    # Main function
    def main(self):
        global master
        master = tk.Tk()
        master.geometry("1280x720+400+50")
        master.title('Admin Tool')
        master.config(background="#CEE3F6")

        # Insert Image:
        bard = Image.open(self.img)
        bard = bard.resize((130, 130), Image.ANTIALIAS)
        bardejov = ImageTk.PhotoImage(bard)
        label1 = Label(master, image=bardejov)
        label1.image = bardejov
        label1.config(background="#CEE3F6")
        label1.place(x = 580, y = 20)

        # Title TOOL ADMIN
        title1 = tk.Label(master, text='TOOL ADMIN', background="#CEE3F6")
        title1.config(font=("Courier", 30))
        title1.place(x = 900, y = 10)

        # Title DỰ ÁN XÂY DỰNG CHATBOT
        title1 = tk.Label(master, text='DỰ ÁN XÂY DỰNG CHATBOT', background="#CEE3F6")
        title1.config(font=("Courier", 30))
        title1.place(x = 770, y = 60)

        # Title TƯ VẤN TUYỂN SINH ĐẠI HỌC
        title1 = tk.Label(master, text='TƯ VẤN TUYỂN SINH ĐẠI HỌC', background="#CEE3F6")
        title1.config(font=("Courier", 30))
        title1.place(x = 730, y = 110)

        # Create Combobox
        combox1 = Main.Combobox(self, "Mã ngành", {"major_code": sorted(self.data_dt['major_code'])}, 100)
        combox2 = Main.Combobox(self, "Chuyên ngành", {"major_name": sorted(self.data_dt['major_name'])}, 160)
        combox3 = Main.Combobox(self, "Hình thức đào tạo", {"type_edu": sorted(self.data_dt['type_edu'])}, 220)
        combox4 = Main.Combobox(self, "Năm", {"year": sorted(self.data_dt['year']+['2021','2022'])}, 280)      
        combox5 = Main.Combobox(self, "Khối", {"subject_group": sorted(self.data_dt['subject_group'])}, 340)
        combox6 = Main.Combobox(self, "Phương thức tuyển sinh", {"case": sorted(self.data_dt['case'])}, 400)
        
        
        point_st = tk.StringVar()
        criteria_st = tk.StringVar()

        text = Text(master)
        text.pack(expand=YES, fill=BOTH)
        text.place(x = 650, y = 250)

        # Submit Button
        def gen_output():
            output = tk.StringVar()
            self.point = point_st.get()
            if self.point:
                self.point = float(self.point)
            self.criteria = criteria_st.get()
            if self.criteria:
                self.criteria = int(self.criteria)
            self.result_dt.update({"point": [self.point], "criteria": [self.criteria]})

            text = Text(master)
            text.pack(expand=YES, fill=BOTH)
            text.place(x = 650, y = 250)
            
            text.insert(END, str(self.result_dt).replace('["' , "['").replace('"]' , "']"))
            result = str(self.result_dt).replace('["' , "['").replace('"]' , "']")
            print(result)
            return result
        
        def submit():
            mycol.insert_one(json.loads(str(self.result_dt).replace('["' , "['").replace('"]' , "']").replace("\'",'\"')))
            # mycol.insert_one(self.result_dt)

        output = tk.Label(master, text='Output:', background="#CEE3F6")
        output.place(x = 620, y = 220)
        output.config(font=("Arial",14))

        tk.Label(master, text='Điểm', background="#CEE3F6").place(x = 120, y = 470)
        point = ttk.Entry(master, textvariable = point_st)                                       
        point.config(width=7)
        point.place(x = 180, y = 471)

        tk.Label(master, text='Chỉ tiêu', background="#CEE3F6").place(x = 280, y = 470)
        criteria = ttk.Entry(master, textvariable = criteria_st)          
        criteria.config(width=7)
        criteria.place(x = 340, y = 471)

        button = ttk.Button(master, text="Output Generate", command=gen_output).place(x = 180, y = 585)      
        button = ttk.Button(master, text="Submit Document", command=submit).place(x = 340, y = 585)        

        mainloop()

# Execuse File
execuse = Main('./data/entity_admin.json', './data/LogoBK.png', './data/dict_consist.json')