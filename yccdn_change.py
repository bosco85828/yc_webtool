#!/usr/bin python3
# -*- coding: utf-8 -*-
"""
@author: Bosco
Command:
    python3 py_programming02.py
"""


from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
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
# options.add_argument("--headless") 


def login(admin):

    s=Service(ChromeDriverManager().install())
    global browser
    browser = webdriver.Chrome(service=s, options=options)
    browser.get("https://admin.cdnvips.net/Login")
    global wait
    wait=WebDriverWait(browser,10)
    # time.sleep(3)
    # acount=browser.find_element(By.ID,"UserName")
    # password=browser.find_element(By.ID,"Password")
    # submit=browser.find_element(By.ID,"btnSumbit")
    locator=(By.ID,"UserName")
    acount=wait.until(EC.presence_of_element_located(locator))
    locator=(By.ID,"Password")
    password=wait.until(EC.presence_of_element_located(locator))
    
    acount.send_keys('bill')
    password.send_keys('1qaz@WSXbill')

    locator=(By.ID,"btnSumbit")
    submit=wait.until(EC.element_to_be_clickable(locator))
    submit.click()
    # time.sleep(3)


    # user_list=browser.find_element(By.XPATH,'//ul[@class="sidebar-menu tree"]//li[@class="treeview menu-open"]//a[@href="/Merchant"]')
    locator=(By.XPATH,'//ul[@class="sidebar-menu tree"]//li[@class="treeview menu-open"]//a[@href="/Merchant"]')
    user_list=wait.until(EC.element_to_be_clickable(locator))
    # print(user_list.text)
    user_list.click()


    # temp=browser.find_element(By.XPATH,'//input[@id="Name"][1]')
    locator=(By.XPATH,'//input[@id="Name"][1]')
    temp=wait.until(EC.presence_of_element_located(locator))
    temp.send_keys(admin)

    # temp=browser.find_element(By.XPATH,'//button[@class="btn btn-default"][1]')
    locator=(By.XPATH,'//button[@class="btn btn-default"][1]')
    temp=wait.until(EC.element_to_be_clickable(locator))
    temp.click()

    time.sleep(1)

    # admin_search=browser.find_element(By.XPATH,'//a[@class="btn btn-info btn-xs "][1]')
    locator=(By.XPATH,'//a[@class="btn btn-info btn-xs "][1]')
    admin_search=wait.until(EC.element_to_be_clickable(locator))
    admin_search.click()
    
    browser.switch_to.window(browser.window_handles[1])

    # temp=browser.find_element(By.XPATH,'//li[@class="treeview"][2]//li[1]//a[1]')
    locator=(By.XPATH,'//li[@class="treeview"][2]//li[1]//a[1]')
    temp=wait.until(EC.element_to_be_clickable(locator))
    temp.click()

    

def add_domain(cusID,domainlist,request_port,origin_addr,origin_port,type,redirect=None):
    
        login(cusID)
        for domain in domainlist:
            with open("ycadd.log","a+") as f :

                try:
                    locator=(By.XPATH,'//i[@class="fa fa-plus-circle"]')
                    temp=wait.until(EC.element_to_be_clickable(locator))
                    temp.click()
                    locator=(By.XPATH,'//input[@id="Domain"]')
                    d_name=wait.until(EC.presence_of_element_located(locator))
                    d_name.send_keys(domain)
                    locator=(By.XPATH,'//input[@id="IP"]')
                    origin=wait.until(EC.presence_of_element_located(locator))
                    origin.send_keys(origin_addr)
                    locator=(By.XPATH,'//input[@id="AccelerationDomainPort"]')
                    r_port=wait.until(EC.presence_of_element_located(locator))
                    r_port.send_keys(request_port)
                    # print(origin_port)
                    if origin_port == "matchviewer" : 
                        # print('1')
                        locator=(By.XPATH,'//input[@id="IsAgreementFollow"][@value="1"]')
                        port=wait.until(EC.element_to_be_clickable(locator))
                        port.click()
                    else :
                        # print('2')
                        locator=(By.XPATH,'//input[@id="SourcePort"]')
                        port=wait.until(EC.presence_of_element_located(locator))
                        port.send_keys(origin_port)
                    # locator=(By.XPATH,'//input[@id="AccelerationArea"][@value=2]')
                    # area=wait.until(EC.element_to_be_clickable(locator))
                    # area.click()
                    locator=(By.XPATH,f'//input[@id="AccelerationType"][@value={type}]')
                    Accelerate_type=wait.until(EC.element_to_be_clickable(locator))
                    Accelerate_type.click()

                    if redirect : 
                        locator=(By.XPATH,'//span[@class="bootstrap-switch-label"]')
                        redirect_enable=wait.until(EC.element_to_be_clickable(locator))
                        redirect_enable.click()

                        # print(redirect)

                        locator=(By.XPATH,f'//input[@name="RedirectType"][@value={redirect}]')
                        redirect_type=wait.until(EC.element_to_be_clickable(locator))
                        redirect_type.click()
                    try:
                        locator=(By.XPATH,'//i[@class="fa fa-check-circle"]')
                        end_button=wait.until(EC.element_to_be_clickable(locator))
                        end_button.click()

                        locator=(By.XPATH,'//button[@id="J-alert-Ok"]')                
                        check=wait.until(EC.element_to_be_clickable(locator))
                        check.click()
                    except:
                        browser.quit()
                        f.write("{}\n".format({f"{domain}":"The domain has already been created or entered in the wrong format, please check in YCCDN admin."}))
                        login(cusID)
                        
                        continue
                            

                    print({f"{domain}":"Create completed"})
                    f.write("{}\n".format({f"{domain}":"Create completed"}))
                
                except : 
                    print({f"{domain}":"Something wrong, please try again."})
                    f.write("{}\n".format({f"{domain}":"Something wrong, please try again."}))
                    browser.quit()
                    login(cusID)
                    # f.write("{}\n".format({f"{domain}":"Something wrong, please try again."}))

        else: browser.quit()





def change_origin(domain,browser):
    temp=browser.find_element(By.XPATH,'//input[@id="Domain"]')

    temp.clear()
    temp.send_keys(domain)
    temp=browser.find_element(By.XPATH,'//button[@class="btn btn-default"]')
    temp.click()
    time.sleep(1)
    tr_size=browser.find_elements(By.XPATH,'//table[@id="CdnInfoTable"]/tbody/tr')
    index=1

    if tr_size: 
        
        while index <= len(tr_size) : 
            temp=browser.find_element(By.XPATH,f'//table[@id="CdnInfoTable"]/tbody/tr[{index}]/td[2]')
            print(temp.text)
            if domain == temp.text : 
                break
            else : 
                index += 2
        
        else : return f"{domain} can't find domain."
                        

        temp=browser.find_element(By.XPATH,f'//table[@id="CdnInfoTable"]/tbody/tr[{index}]//i[@class="fa fa-edit"]')
        temp.click()
        time.sleep(1)

        temp=browser.find_element(By.XPATH,'//input[@name="IP"]')
        temp.clear()

        time.sleep(1)
        temp.send_keys('http://h5-2.member23.site')

        temp=browser.find_element(By.XPATH,'//input[@name="SourcePort"]')
        temp.clear()
        time.sleep(1)
        temp.send_keys('80')
        time.sleep(1)
        # temp=browser.find_element(By.XPATH,'//i[@class="fa fa-check-circle"]')
        # temp.click()
        # time.sleep(1)
        # temp=browser.find_element(By.XPATH,'//button[@class="btn btn-primary pull-right"]')
        # temp.click()
        # time.sleep(1)
        return f"{domain} Complete"
    
    else : return f"{domain} can't find domain."



if __name__ == "__main__":
    
    # with open('domain3.txt') as f : 
    #     dlist=[ x.strip() for x in f.readlines()]
    # print(dlist)
    # print(len(dlist))
    dlist=['ittlefish99.com']

    print(add_domain(['bosco1.com'],"443","http://1.1.1.1",80,3,302))
    time.sleep(5)
    # for dm in dlist : 
        # print(change_origin(dm,browser))

