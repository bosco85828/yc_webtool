#!/usr/bin python3
# -*- coding: utf-8 -*-
"""
@author: Bosco
Command:
    python3 py_programming02.py
"""
import sys
from datetime import datetime,timezone,timedelta
import requests
from selenium.common.exceptions import NoSuchElementException,TimeoutException
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
import pytz
from OpenSSL import crypto
from dotenv import load_dotenv
import os 
import json
from enum import Enum, unique


load_dotenv()
YC_PASSWORD=os.getenv('YC_PASSWORD')


options = Options()
options.add_argument("--disable-notifications")    
options.add_argument("--headless")
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('blink-settings=imagesEnabled=false')
options.add_argument('--disable-dev-shm-usage')
# options.add_argument("--headless") 
now=datetime.now().strftime("%Y-%m-%d")
path=os.getcwd()

class AccelType(Enum):
    api=1
    web=2
    websocket=3
    large_file=4
    small_file=5
    other=6
    


def login(admin):

    s=Service()
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
    password.send_keys(YC_PASSWORD)

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


def get_domains(cusid,file_name):
    global log_list
    log_list=[]
    login(cusid)

    tr_list=browser.find_elements(By.XPATH,'//table[@id="CdnInfoTable"]/tbody[1]/tr')
    
    index=1
    page=1
    
    domain_list=[]
    current_url = browser.current_url
    while True :
        
        locator=(By.XPATH,f'//table[@id="CdnInfoTable"]/tbody[1]/tr[{index}]/td[10]/a[1]/span')
        try : domain_info=wait.until(EC.element_to_be_clickable(locator)).click()
        except TimeoutException as err: 
            print('next_page')
            page+=1
            browser.get(current_url + f"?PageIndex={page}")
            tr_list=browser.find_elements(By.XPATH,'//table[@id="CdnInfoTable"]/tbody[1]/tr')

            if len(tr_list) == 0 :
                break

            index=1
            continue

        locator=(By.XPATH,'//input[@id="Domain"]')
        domain_name=wait.until(EC.presence_of_element_located(locator)).get_attribute('value')
        print(domain_name)
        locator=(By.XPATH,'//input[@id="CNAME"]')
        domain_cname=wait.until(EC.presence_of_element_located(locator)).get_attribute('value')
        locator=(By.XPATH,'//div[@class="form-group"][4]//input')
        domain_origin=wait.until(EC.presence_of_element_located(locator)).get_attribute('value')
        locator=(By.XPATH,'//div[@class="form-group"][6]//input[@id="SourcePort"]')
        domain_origin_port=wait.until(EC.presence_of_element_located(locator)).get_attribute('value')
        locator=(By.XPATH,'//input[@name="AccelerationDomainPort"]')  
        port=wait.until(EC.presence_of_element_located(locator)).get_attribute('value')
        locator=(By.XPATH,'//input[@name="IsRedirect"]')
        redirect=wait.until(EC.presence_of_element_located(locator)).get_attribute('value')
        locator=(By.XPATH,'//input[@name="IsBackToSourcerHost"]')
        custom_host=wait.until(EC.presence_of_element_located(locator)).get_attribute('value')
        locator=(By.XPATH,'//input[@name="IsHttps"]')
        https=wait.until(EC.presence_of_element_located(locator)).get_attribute('value')
        locator=(By.XPATH,'//input[@checked="checked" and @name="AccelerationType"]')
        type_=wait.until(EC.presence_of_element_located(locator)).get_attribute('value')
        

        if int(https):
            locator=(By.XPATH,'//input[@name="HttpsPort"]')
            https_port=wait.until(EC.presence_of_element_located(locator)).get_attribute('value')
        else:https_port=None

        if int(custom_host) : 
            locator=(By.XPATH,'//input[@name="CustomDomain"]')
            custom_domain=wait.until(EC.presence_of_element_located(locator)).get_attribute('value')
        else : custom_domain = None
            
        domain_dict={
                'domain':domain_name,
                'request_port':port,
                'cname':domain_cname,
                'origin':domain_origin,
                'origin_port':domain_origin_port,
                'https':bool(int(https)),
                'https_port':https_port,
                'redirect':bool(int(redirect)),
                'custom_host':bool(int(custom_host)),
                'custom_host_name':custom_domain,
                'AccelerationType':AccelType(int(type_)).name
            }    
        

        print(domain_dict)
        
        browser.get(current_url + f"?PageIndex={page}")
        index+=2
        domain_list.append(domain_dict)

    print(domain_list[0:2])
    print(len(domain_list))
    browser.quit()
    with open(f"{path}/yccdn/domain_info/{file_name}.json","w+") as f : 
        f.write(json.dumps(domain_list))
    
    return domain_list
    



if __name__ == "__main__":
    cusid='yc'

    get_domains(cusid,'yctest')

        
