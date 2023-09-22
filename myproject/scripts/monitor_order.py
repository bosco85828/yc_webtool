#!/usr/bin python3
# -*- coding: utf-8 -*-
"""
@author: Bill
Command:
    python monitor_order.py
"""
import requests
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException,TimeoutException,WebDriverException
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.add_argument("--disable-notifications")  
options.add_argument("--headless")
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('blink-settings=imagesEnabled=false')
options.add_argument('--disable-dev-shm-usage')

# options.add_argument("--disable-notifications")  
# options.add_argument("--headless") 
s=Service(ChromeDriverManager().install())


def compare_cnzz(domain):
    url="https://{}/".format(domain)
    result=requests.get(url)
    soup=BeautifulSoup(result.text,'lxml')
    data=soup.find_all('script')

    ans=[ x.string for x in data if x.string != None and "cnzz_s_tag.src" in x.string ]

    data=ans[0].split('\n')
    for i in data : 
        if "cnzz_s_tag.src" in i :
            result=i.strip()

    cnzz_id=re.search(r'id=(\d+)',result).group(1)
    cnzz_domain=re.search(r'https://([0-9a-zA-Z.-]+)',result).group(1)

    return f"{cnzz_domain}:{cnzz_id}"


def login(domain,right_code,browser):

    if str(merchant_id) == "0":
        try : browser.get(f"https://{domain}/")
        except WebDriverException : 
            wrong_domain.append(f"{domain}>Please check domain SSL.")
            # print("Please check domain SSL.")
            return f"{domain}: Please check domain SSL."
        # try:temp=browser.find_element(By.XPATH,'//div[@class="close-button"][1]')
        # except NoSuchElementException:
        #     wrong_domain.append(f"{domain}>can't access")
        #     return f"{domain} can't access."
        # except : 
        #     wrong_domain.append(f"{domain}>something wrong")
        #     return f"{domain}, something wrong."
        
        locator=(By.XPATH,'//div[@class="close-button"][1]')
        search_close= WebDriverWait(browser,10).until(EC.element_to_be_clickable(locator),"訪問出現異常")
        # print(search_close)
        search_close.click()
        time.sleep(3)
        locator=(By.XPATH,'//div[@class="class-block-selector"]/div')
        temp=WebDriverWait(browser,10).until(EC.presence_of_all_elements_located(locator))
        # print([ x.get_attribute('class') for x in temp ])
        banner=browser.find_elements(By.XPATH,'//div[@class="class-block-selector"]/div')
        compare_result=compare_banner(banner)
        
        if compare_result != "Success" : 
            wrong_domain.append(f"{domain}>{compare_result}, Now:{now_banner}.")
            return f"{domain}, {compare_result}, Now:{now_banner}."

    # temp=browser.find_element(By.XPATH,'//div[@class="login-wrapper"]/img[2]')
    # locator=(By.XPATH,'//div[@class="login-wrapper"]/img[1]')
    # temp= WebDriverWait(browser,10).until(EC.element_to_be_clickable(locator),"訪問出現異常")
    # print(123)
    # # print(temp)
    # temp.click()
    browser.get(f"https://{domain}/regist")
    # temp=browser.find_element(By.XPATH,'//div[@class="swiper-slide swiper-slide-active"]//form/div[4]//input')
    locator=(By.XPATH,'//div[@class="swiper-slide swiper-slide-active"]//form/div[4]//input')
    temp=WebDriverWait(browser,10).until(EC.presence_of_element_located(locator),"找不到邀請碼")
    code=temp.get_attribute('value')
    if code != right_code:
        wrong_domain.append(f"{domain}>The code is wrong, Wrong code: {code}, Correct: {right_code}.")
        return f"{domain}, The code is wrong, Wrong code: {code}, Correct: {right_code}."
    
    return "Completed"


def compare_banner(banner):
    banner_list=["electronic","live","qpgame","cpgame","hunter","sports","esports","hotgame"]
    global banner_result
    banner_result=[ (int(order[x])-1,banner_list[x]) for x in range(len(order))]
    banner_result.sort(key=lambda x : x[0])
    # print(order)
    print(banner_result)
    # banner_list=list(enumerate(["electronic","live","qpgame","cpgame","hunter","sports","esports"]))
    
    for index,value in banner_result:
        
        temp_banner=banner[index].get_attribute('class').split(" ")[-1]
        now_banner.append(temp_banner)     
        
        if temp_banner != value : 
            return "The order of the buttons is wrong."

    else : return "Success"


def main(input_,qlist,input_order,statistics,merchant):
    global merchant_id
    merchant_id=merchant

    global correct_domain
    correct_domain=[]
    
    global browser
    browser = webdriver.Chrome(service=s, options=options)
    browser.set_page_load_timeout(120)

    global wrong_domain
    wrong_domain=[]
    global now_banner
    global order 
    order = input_order
    
    dlist=[tuple(re.findall(r'[a-zA-Z.0-9-:]+',x)) for x in input_.split('\n') if x ]
    
    # dlist=[tuple(x.strip().split(' ')) for x in input_.split('\n') if x ]
    # print(dlist)
    if str(statistics) == "0" :
        try:
            for dm,right_code in dlist:
                
                now_banner=[]
                try : 
                    if login(dm,right_code,browser) != "Completed" : 
                        continue

                except TimeoutException : 
                    print(f"{dm} check timeout.")
                    wrong_domain.append(f"{dm}>check timeout.")
                    continue
                except :
                    wrong_domain.append(f"{dm}>Something wrong,please try again.") 
                    print(f"{dm} Something wrong")
                    continue
                
                correct_domain.append(dm)
                print(f"{dm}, Completed.")

        except ValueError : 
            wrong_domain.append("格式錯誤>請確認格式是否符合範例。")
            # raise ValueError("Please check the domain.txt format.")
    else:
        try:
            for dm,right_code,statistics_code in dlist:
                
                now_banner=[]
                #比對選單順序以及驗證碼
                try : 
                    if login(dm,right_code,browser) != "Completed" : 
                        continue

                except TimeoutException : 
                    print(f"{dm} check timeout.")
                    wrong_domain.append(f"{dm}>check timeout.")
                    continue
                except :
                    wrong_domain.append(f"{dm}>Something wrong,please try again.") 
                    print(f"{dm} Something wrong")
                    continue
                
                #比對統計碼
                try : 
                    now_cnzz=compare_cnzz(dm)
                except : 
                    wrong_domain.append(f"{dm}>Can't find cnzz code.")
                    print(f"{dm}>Can't find cnzz code.")
                    continue

                if statistics_code != now_cnzz:
                    wrong_domain.append(f"{dm}>Cnzz_code is wrong, the current statistics code on the website is {now_cnzz}.")
                    print(f"{dm}>Cnzz_code is wrong, the current statistics code on the website is {now_cnzz}.")
                    continue
                
                correct_domain.append(dm)
                print(f"{dm}, Completed.")



        except ValueError : 
            wrong_domain.append("格式錯誤>請確認格式是否符合範例。")
            # raise ValueError("Please check the domain.txt format.")

    print("========================================")
    print(f"Wrong domain : {len(wrong_domain)}")
    print(f"Correct domain : {len(correct_domain)}")
    print(wrong_domain)
    print("\n")
    browser.quit()
    
    try: 
        qlist.put(banner_result)
    except: pass 
    
    qlist.put(len(correct_domain))
    qlist.put(wrong_domain)
    return wrong_domain

if __name__ == "__main__" : 
    domain="""www.bosco.live 639920
196ga.com 097988
90201.pw 142982"""
    print(main(domain))