import requests
import re
from bs4 import BeautifulSoup
import threading

def create_domain(domain,token):
    
    sp.acquire()

    url="https://web.umeng.com/main.php?c=site&a=add&ajax=module=add"
    
    header={
            'authority':'web.umeng.com',
            'accept': '*/*',
            'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'cookie':token,
            'referer':'https://web.umeng.com/main.php?',
            'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'x-requested-with':'XMLHttpRequest'
        }
    
    data={
        'sitename':domain,
        'domainlist':domain,
        'sitedomain':domain,
        'type':'IT网络',
        'subtype':'IT网络其它',
        'provinces':'16',
        'cities':'0',
        'siteinfo':None,
        'xsftoken':'cnzz_63de26bdc976b'
    }

    result=requests.post(url,headers=header,data=data)

    print(result)
    sp.release()
    return result

def main(input_domain,input_token):
    global sp 
    sp=threading.Semaphore(5)
    domainlist=re.findall(r'[a-zA-Z.:0-9-]+',input_domain)
    for domain in domainlist : 
        t1=threading.Thread(target=create_domain,args=(domain,input_token))
        t1.start()
    
    return domainlist


if __name__ == "__main__":
    token="PHPSESSID=guinrkingpf3kao3eis2bt7qr1; Hm_lvt_289016bc8d714b0144dc729f1f2ddc0d=1675503269; _abfpc=493150058472b32755f75bda9e3bb604c37ec5a0_2.0; dplus_finger_print=293600551; AGL_USER_ID=e4b710a9-358e-40f7-b8bf-5713fc50c65f; cna=18c4360a5a3b3e6e11b010097ec83329; uc_session_id=cc2db9ca-5401-4c9d-9de7-764071899a32; from=umeng; edtoken=cnzz_63de26bdc976b; frontvar=siteListSortId%3D%26siteShowHis%3Dopen%26cmenu%3Dflow_realtime; CNZZDATA1281115298=1742139104-1675501656-https%253A%252F%252Fweb.umeng.com%252F%7C1677650105; umplus_uc_token=1tDD7KQi9-F_JSWOmeqDf8g_81afc88de8fe4d8b807240d160124ea4; umplus_uc_loginid=SC%E8%B2%B3%E5%8F%83%E5%8A%A0; Hm_lpvt_289016bc8d714b0144dc729f1f2ddc0d=1677653062; UM_distinctid=1869bea343d70d-0c1f147805fabc-1f525634-1fa400-1869bea343e4cb"
    domain="""bill301eee.cc
    biill301kkk.cc biill301ggg.cc
    
    biill301ppp.cc"""

    print(main(domain,token))
    