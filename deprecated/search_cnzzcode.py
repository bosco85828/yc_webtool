import requests
import re
from bs4 import BeautifulSoup

def get_siteid(domain):
    # domain_list=[]
    for i in range(1,7):
        url=f"https://web.umeng.com/main.php?c=site&a=show&ajax=module=list|module=isOpenTongji&search=&currentPage={i}&pageType=90&sort=5"

        header={
            'authority':'web.umeng.com',
            'accept': '*/*',
            'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'cookie':token,
            'referer':'https://web.umeng.com/main.php?c=site&a=show',
            'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'x-requested-with':'XMLHttpRequest'
        }
        
        result=requests.get(url,headers=header).json()
        
        
        
        # domain = [ x['domain'] for x in result['data']['list']['items']]    
        # domain_list += domain

        for x in result['data']['list']['items']:
            if x['domain'] == domain:
                return x['siteid']

    
    

def get_cnzz_domain(ID):
    url=f"https://web.umeng.com/main.php?c=site&a=getcode&siteid={ID}"
    
    header={
        'authority':'web.umeng.com',
        'accept': '*/*',
        'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie':token,
        'referer':'https://web.umeng.com/main.php?c=site&a=show',
        'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'x-requested-with':'XMLHttpRequest'
    }
    result=requests.get(url,headers=header)

    soup=BeautifulSoup(result.text,'lxml')
    # print(soup)
    data=soup.find_all('textarea',{'name':'textarea'})
    # for i in data:
    #     print(i.string)
    try : cnzz_domain=re.search(r'https://(\w+\.\w+\.\w+)',str(data[0].string)).group(1)
    except AttributeError :
        cnzz_domain = None
        

    return cnzz_domain

def main(input_token,input_domain):

    global token
    token=input_token
    domain_list=re.findall(r'[a-zA-Z.0-9-]+',input_domain)
    result_list=[]
    for domain in domain_list : 
        siteID=get_siteid(domain)
        cnzzdomain=get_cnzz_domain(siteID)
        # result_list.append(str({'domain':domain,'cnzz_info':f'{cnzzdomain}:{siteID}'}))
        result_list.append(f"{domain} {cnzzdomain}:{siteID}")
    
    print("\n".join(result_list))
    return result_list

if __name__ == "__main__":
    
    global token
    token='PHPSESSID=guinrkingpf3kao3eis2bt7qr1; Hm_lvt_289016bc8d714b0144dc729f1f2ddc0d=1675503269; _abfpc=493150058472b32755f75bda9e3bb604c37ec5a0_2.0; dplus_finger_print=293600551; AGL_USER_ID=e4b710a9-358e-40f7-b8bf-5713fc50c65f; cna=18c4360a5a3b3e6e11b010097ec83329; uc_session_id=cc2db9ca-5401-4c9d-9de7-764071899a32; from=umeng; edtoken=cnzz_63de26bdc976b; frontvar=siteListSortId%3D%26siteShowHis%3Dopen%26cmenu%3Dflow_realtime; CNZZDATA1281115298=1742139104-1675501656-https%253A%252F%252Fweb.umeng.com%252F%7C1677566120; umplus_uc_token=1OuYjNx56zna0NspbOVXxAQ_630cd4124f3646d7b9f07d7ed22fb5bd; umplus_uc_loginid=qaz67890; Hm_lpvt_289016bc8d714b0144dc729f1f2ddc0d=1677568141; UM_distinctid=18696da65a0167-04b816c5ca6349-1f525634-13c680-18696da65a1a4a'
    domain="""38289.mba
    38228.mba 38216.mba
    17667.me

    369236.org

    """
    # siteID=get_siteid(domain)
    # cnzzdomain=get_cnzz_domain(siteID)
    # print({'domain':domain,'cnzz_info':f'{cnzzdomain}:{siteID}'})
    main(token,domain)
    


