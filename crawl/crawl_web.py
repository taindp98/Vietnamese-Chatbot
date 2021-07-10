from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import csv

#1. Khai bao browser

browser=webdriver.Firefox(executable_path="./geckodriver")
#2. Mo website
url="https://diemthi.tuyensinh247.com/diem-chuan.html"
browser.get(url)

#3. Lay bai viet
sleep(5)

post = browser.find_elements_by_xpath("//a")

f1=(open('/home/taindp/Database/code_and_name_uni.txt','w',encoding='utf-8'))
for ele in post:
    text=ele.get_attribute("textContent")
    text=str(text)
    f1.write(text)
    f1.write('\n')
    print(text)
    #else:
    #        writer=csv.writer(file2)
    #        writer.writerow(text)
    #        print(text)
sleep(3)
browser.close()
# with open('/home/taindp/PycharmProjects/crawl/crawl_viettat_data.csv','w',encoding='utf-8') as file:
#     writer=csv.writer(file)
    


