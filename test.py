import socket
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
import json

options = Options()
options.add_argument("--disable-notifications")    
options.add_argument("--headless")
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('blink-settings=imagesEnabled=false')
options.add_argument('--disable-dev-shm-usage')

s=Service(ChromeDriverManager().install())
global browser
browser = webdriver.Chrome(service=s, options=options)
browser.get("http://yc-api.cdnvips.net/Cdn/getYcDomain")
global wait
wait=WebDriverWait(browser,10)

locator=(By.XPATH,'//body')
body=wait.until(EC.presence_of_element_located(locator))
data=body.text

data=data.strip('[]')
print(type(json.loads(data)))


