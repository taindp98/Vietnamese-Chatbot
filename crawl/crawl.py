from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import os
import re
import sys
from datetime import datetime
import csv
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
def init_browser(url):
    # options = Options()
    global browser
    browser=webdriver.Firefox(executable_path="./geckodriver")
    browser.get(url)
    sleep(2)
    print('Initial browser...')
def login(email,password):
    # sleep(2)
    # browser.refresh()
    browser.find_element_by_xpath("//input[@name='email']").send_keys(email)
    browser.find_element_by_xpath("//input[@name='pass']").send_keys(password)
    sleep(1)
    # if browser.find_element_by_xpath("//input[@aria-label='Đăng nhập']"):
    #     browser.find_element_by_xpath("//input[@aria-label='Đăng nhập']").click()
    # elif browser.find_element_by_xpath("//div[@aria-label='Accessible login button']"):
    #     browser.find_element_by_xpath("//div[@aria-label='Accessible login button']").click()
    if browser.find_element_by_xpath("//button[@name='login']"):
        browser.find_element_by_xpath("//button[@name='login']").click()
    else:
        sys.exit()
    print('Login...')
# get element
def find_page(name_page):
    sleep(0.5)
    findbox = browser.find_element_by_xpath("//input[@role='combobox']")
    sleep(2)
    findbox.send_keys(name_page)

    sleep(1)

    sel_page1 = browser.find_elements_by_xpath("//li[@role='option']")
    sel_page1[0].click()
    sleep(2)
    sel_page2 = browser.find_elements_by_xpath("//a[@role='presentation']")
    sel_page2[0].click()
    sleep(0.5)
    browser.refresh()
def get_post_id(post_element):
    re_token1=r'\(.*?\)'
    re_token2=r'\".*?\"'
    post2str = str(post_element)
    postele = str(re.findall(re_token1,post2str)[0]).replace(r'(',r'').replace(r')',r'')
    id = str(re.findall(re_token2,str(postele.split(',')[-1]))[0]).replace(r'"',r'')
    return id

def press_extra():
    posts = browser.find_elements_by_xpath("//div[@role='article']")
    # print(len(posts))
    sleep(1)
    for post in posts:
        try:
            extras = post.find_elements_by_xpath("//div[@role='button']")
            if extras:
                for extra in extras:
                    # cnt = extra.get_attribute('innerHTML')
                    cnt = extra.get_attribute('innerHTML')
                    if str(cnt).startswith('Xem thêm'):
                        browser.execute_script("arguments[0].click();", extra)
        except:
            continue
    print('Page extra..')
def scroll_page():
    # scroll ---> extra page
    sleep(2)
    last_height = browser.execute_script("return document.body.scrollHeight")
    # browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    new_height = browser.execute_script('window.scrollTo(0, window.scrollY + 1096);')
    # if new_height == last_height:
    #     sys.exit()
    print('Scrolling...')
    sleep(2)
    press_extra()
    print('Scrolled...')
    return True

# def save_img(id,urls,path):
#     folder = os.path.join(path,id)
#     if os.path.isdir(folder):
#         for index,url in enumerate(urls):
#             resource = urllib.request.urlopen(url)
#             if os.path.isfile(os.path.join(folder,f'{id}'+'_'+f'{index}'+'.jpg')):
#                 continue
#             else:
#                 with open(os.path.join(folder,f'{id}'+'_'+f'{index}'+'.jpg'), 'wb') as handler:
#                     handler.write(resource.read())
#     else:
#         os.mkdir(folder)
#         for index,url in enumerate(urls):
#             resource = urllib.request.urlopen(url)
#             if os.path.isfile(os.path.join(folder,f'{id}'+'_'+f'{index}'+'.jpg')):
#                 continue
#             else:
#                 with open(os.path.join(folder,f'{id}'+'_'+f'{index}'+'.jpg'), 'wb') as handler:
#                     handler.write(resource.read())
def get_post(time_scroll,url):
    browser.get(url)
    # today = date.today()
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S").replace(r'/',r'_').replace(r':',r'_').replace(r' ',r'_')
    if not os.path.isdir(f'data_crawl/{dt_string}'):
        os.mkdir(f'data_crawl/{dt_string}')
    path_out = f'data_crawl/{dt_string}/data_crawler.json'
    list_out = []

    memory = []
    cur_time = 0
    while True:
        print('Current post: {}'.format(len(memory)))
        if cur_time == time_scroll:
            break
        else:
            cur_time += 1
            print('Current time:{}'.format(cur_time))
            scrolled = scroll_page()
            # try:
            if scrolled:
                # print(scrolled)
                posts = browser.find_elements_by_xpath("//div[@role='article']")
                for post in posts:
                    dict_post = {}
                    if post.get_attribute('aria-posinset'):
                        ids = str(post.get_attribute('aria-describedby')).split(' ')
                        # mỗi ids[] gồm post,content,ảnh,cmt
                        # print(ids[0])
                        if ids[1] not in memory:
                            memory.append(ids[1])
                            contents = browser.find_elements_by_xpath(f"//div[@id='{ids[1]}' and @data-ad-preview='message']//div[@style='text-align: start;']")
                            list_content = []
                            dict_post['id'] = ids[1]
                            for txt in contents:
                                # print(ids[1])
                                # print(txt.text)
                                if txt.text != '':
                                    list_content.append(txt.text)
                            if len(list_content) > 0:
                                dict_post['content'] = list_content
                                with open(path_out, 'a') as jsonfile:
                                    dict2str = str(dict_post).replace(r"'",r'"')
                                    jsonfile.write(dict2str)
                                    jsonfile.write('\n')



if __name__== '__main__':
    email = ''
    password = ''
    time_scroll = 15

    url = 'https://www.facebook.com/'
    init_browser(url)
    login(email,password)
    # url = 'https://www.facebook.com/groups/huongnghieptuvantuyensinh/'
    #url="https://www.facebook.com/groups/huongnghieptuvantuyensinh/"
    # url="https://www.facebook.com/groups/HuongNghiepThongMinh/"
    # url="https://www.facebook.com/groups/533625860900876/"
    url = 'https://www.facebook.com/groups/BKTPHCM'
    get_post(time_scroll,url)
    browser.close()
