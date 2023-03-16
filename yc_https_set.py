#!/usr/bin python3
# -*- coding: utf-8 -*-
"""
@author: Bosco
Command:
    python3 py_programming02.py
"""

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

options = Options()
options.add_argument("--disable-notifications")    
options.add_argument("--headless")
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('blink-settings=imagesEnabled=false')
options.add_argument('--disable-dev-shm-usage')
# options.add_argument("--headless") 
now=datetime.now().strftime("%Y-%m-%d")

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

def compare_cert(cert_data):

    cert=crypto.load_certificate(crypto.FILETYPE_PEM,cert_data.encode())
    not_before=datetime.strptime(cert.get_notBefore().decode(),'%Y%m%d%H%M%SZ')
    tz=pytz.timezone('UTC')

    now_time = datetime.now(tz)
    now_time = now_time.replace(tzinfo=None)
    print(now_time)
    print(not_before)
    
    diff_day = (now_time-not_before).total_seconds()/86400

    return diff_day

def change_set(cusid,dlist,port,force=False):
    global log_list
    log_list=[]
    login(cusid)
    print(dlist)
    for domain in dlist:
        data=get_ycssl(domain)
        cert=data['cert']
        key=data['key']

        if not cert:
            log_list.append(str({domain:"Application for a new certificate failed. Please check if you are pointing correctly."}))
            continue
        
        if  compare_cert(cert) > 7: 
            count=0
            while count < 2  : 
                data=get_ycssl(domain)
                cert=data['cert']
                key=data['key']
                
                if compare_cert(cert) < 1 :
                    break

                else : 
                    count += 1 
                    continue 
            
            else : 
                log_list.append(str({domain:"Application for a new certificate failed. Please check if you are pointing correctly."}))
                continue
        


        locator=(By.XPATH,'//input[@name="Domain"]')
        temp=wait.until(EC.presence_of_element_located(locator))
        temp.clear()
        temp.send_keys(domain)

        locator=(By.XPATH,'//button[@class="btn btn-default"][1]')
        search=wait.until(EC.element_to_be_clickable(locator))
        search.click()

        tr_list=browser.find_elements(By.XPATH,'//table[@id="CdnInfoTable"]/tbody[1]/tr')
        index=1
        
        while index <= len(tr_list):
            locator=(By.XPATH,f'//table[@id="CdnInfoTable"]/tbody[1]/tr[{index}]/td[2]')
            yc_domain_name=wait.until(EC.presence_of_element_located(locator)).text

            if yc_domain_name != domain : 
                index +=2 
                continue

            else : 
                break
        
        else : 
            log_list.append(str({domain:"Can't find domain."}))
            continue


        locator=(By.XPATH,f'//table[@id="CdnInfoTable"]/tbody[1]/tr[{index}]//a[@class="btn btn-info"][1]')
        infopage=wait.until(EC.element_to_be_clickable(locator))
        infopage.click()

        locator=(By.XPATH,'//li[@id="Https"]')
        https_page=wait.until(EC.element_to_be_clickable(locator))
        https_page.click()
        
        #抓取目前開關 value
        locator=(By.XPATH,'//div[@id="tabHttps"]//div[@class="switch"][1]//input[@name="IsHttps"]')
        ishttps=wait.until(EC.presence_of_element_located(locator))
        https_value=ishttps.get_attribute('value')
        
        if not int(https_value):
            # print(123)
            locator=(By.XPATH,'//div[@id="tabHttps"]//div[@class="switch"][1]//span[2]')
            open_https=wait.until(EC.element_to_be_clickable(locator))
            # print(open_https.text)
            open_https.click()

            locator=(By.XPATH,'//input[@id="HttpsPort"]')
            https_port=wait.until(EC.presence_of_element_located(locator))
            try : 
                https_port.clear()
            except: pass

            https_port.send_keys(port)
        

        if int(force) : 

            locator=(By.XPATH,'//div[@id="tabHttps"]//input[@name="IsForceHttps"]')
            isforce=wait.until(EC.presence_of_element_located(locator))
            isforce_value=isforce.get_attribute('value')

            
            if not int(isforce_value) : 

                locator=(By.XPATH,'//div[@id="tabHttps"]//div[@class="form-group"][2]//span[2]')
                force_https=wait.until(EC.presence_of_element_located(locator))
                force_https.click()


        locator=(By.XPATH,'//input[@name="CertificatesType" and @value="1"]')
        cert_type=wait.until(EC.element_to_be_clickable(locator))
        cert_type.click()
        
        locator=(By.XPATH,'//input[@name="CertificatesName"]')
        cert_name=wait.until(EC.presence_of_element_located(locator))
        cert_name.clear()
        cert_name.send_keys(now+"_"+domain)

        locator=(By.XPATH,'//textarea[@name="CertificatesContent"]')
        cert_content=wait.until(EC.presence_of_element_located(locator))
        cert_content.clear()
        cert_content.send_keys(cert)

        locator=(By.XPATH,'//textarea[@name="PrivateKey"]')
        privatekey=wait.until(EC.presence_of_element_located(locator))
        privatekey.clear()
        privatekey.send_keys(key)

        locator=(By.XPATH,'//*[@id="formHttps"]//button[@class="btn btn-warning"]')
        submit=wait.until(EC.element_to_be_clickable(locator))
        submit.click()

        locator=(By.XPATH,'//button[@id="J-alert-Ok"]')
        check=wait.until(EC.element_to_be_clickable(locator))
        check.click()

        log_list.append(str({domain:"success"}))

    browser.quit()
    now_time=datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=8)))
    try : 
        with open("ychttps.log",'r+') as f : 
            old_content=f.read()
            f.seek(0)
            f.write(f"\n{now_time}\n")
            f.write("\n".join(log_list))
            f.write("\n"+old_content)
    except FileNotFoundError : 
        with open("ychttps.log",'w+') as f : 
            f.write(f"\n{now_time}\n")
            f.write("\n".join(log_list))



def get_ycssl(domain):
    url="http://yc-api.cdnvips.net/Cdn/getCert"
    data={
        'domain':domain
    }

    result=requests.post(url,data=data).json()
    return result

if __name__ == "__main__":
    cusid='yc'
    dlist=['m.bosco.live']
    port=443
    change_set(cusid,dlist,port)
    print(log_list)
    
    # print(cert)
    # print('==============')
    # print(key)