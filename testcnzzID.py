import requests
import re
from bs4 import BeautifulSoup

def get_now_cnzz():
    url="https://123365.co/"
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


