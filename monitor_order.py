#!/usr/bin python3
# -*- coding: utf-8 -*-
"""
@author: Bill
Command:
    python monitor_order.py
"""

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




def login(domain,right_code,browser):
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
    
    return f"{domain}, Completed."


def compare_banner(banner):
    banner_list=["electronic","live","qpgame","cpgame","hunter","sports","esports","hotgame"]
    banner_result=[ (int(order[x])-1,banner_list[x]) for x in range(len(order))]
    banner_result.sort(key=lambda x : x[0])
    # print(order)
    # print(banner_result)
    # banner_list=list(enumerate(["electronic","live","qpgame","cpgame","hunter","sports","esports"]))
    
    for index,value in banner_result:
        
        temp_banner=banner[index].get_attribute('class').split(" ")[-1]
        now_banner.append(temp_banner)     
        
        if temp_banner != value : 
            return "The order of the buttons is wrong."

    else : return "Success"


def main(input_,qlist,input_order):
    global browser
    browser = webdriver.Chrome(service=s, options=options)
    browser.set_page_load_timeout(120)

    global wrong_domain
    wrong_domain=[]
    global now_banner
    global order 
    order = input_order
    
    dlist=[tuple(re.findall(r'[a-zA-Z.0-9-]+',x)) for x in input_.split('\n') if x ]
    
    # dlist=[tuple(x.strip().split(' ')) for x in input_.split('\n') if x ]
    print(dlist)
    try:
        for dm,right_code in dlist:
            now_banner=[]
            try : 
                print(login(dm,right_code,browser))
            except TimeoutException : 
                print(f"{dm} check timeout.")
                wrong_domain.append(f"{dm}>check timeout.")
                continue
            except :
                wrong_domain.append(f"{dm}>Something wrong,please try again.") 
                print(f"{dm} Something wrong")
                continue
    except ValueError : 
        raise ValueError("Please check the domain.txt format.")

    print("========================================")
    print(f"Wrong domain : {len(wrong_domain)}")
    print(wrong_domain)
    print("\n")
    browser.quit()
    qlist.put(wrong_domain)
    return wrong_domain

if __name__ == "__main__" : 
    domain="""www.bosco.live 639920
196ga.com 097988
90201.pw 142982"""
    print(main(domain))