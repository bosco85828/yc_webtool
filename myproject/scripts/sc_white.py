import requests
from datetime import datetime,timezone,timedelta
import re
from dotenv import load_dotenv
import os 

load_dotenv()
SC_WHITE_NAME=os.getenv('SC_WHITE_NAME')
SC_WHITE_PASSWORD=os.getenv('SC_WHITE_PASSWORD')


def get_token():
    url="https://api.speedfan66.com/api/admin/SysAdminLogin/Login"
    header={
        'authority':'api.speedfan66.com',
        'accept':'application/json, text/plain, */*',
        'content-type':'application/json',
        'origin': 'http://admin.howfunwedo.com',
        'referer': 'http://admin.howfunwedo.com/',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'        
    }
    data={
        'signName':SC_WHITE_NAME,
        'signPassword':SC_WHITE_PASSWORD
    }
    
    result=requests.post(url,headers=header,json=data).json()
    
    return result['data']['token']


# merchantID 1="196TY" 2="KK體育" 3="T體育"
def add_white(token,dlist,merchantId=1,type_=0,platformNameId=2,all_domain=None):
    domain_list = list(set(dlist) - all_domain)
    domain_str=",".join(domain_list)
    
    # print(domain_str)
    url="https://api.speedfan66.com/api/admin/SysMerchantDomainInfo/Create"
    
    header={
        'authority':'api.speedfan66.com',
        'accept':'application/json, text/plain, */*',
        'authorization': f'Bearer {token}',
        'content-type':'application/json',
        'origin': 'http://admin.howfunwedo.com',
        'referer': 'http://admin.howfunwedo.com/',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'        
    }
    
    data={
        'merchantId':merchantId,
        'type':type_,
        'isOnly':False,
        'isPC':False,
        'domain':domain_str,
        'isHttps':False,
        'isDisable':False,
        'platformNameId':platformNameId
    }

    if ":" in domain_list[0] and domain_list[0].split(':')[1] != "80":        
        data['isHttps'] = True     
    
    result = requests.post(url,headers=header,json=data).json()
    print("=========")
    print(result)
    print("=========")
    return result

# merchantID 1="196TY" 2="KK體育" 3="T體育"
def add_code(token,dcodelist,merchantId=1):

    final_dcode=[ {'domain':x[0],'correspondData':x[1]} for x in dcodelist]

    url="https://api.speedfan66.com/api/admin/SysMerchantDomainCorrespondInfo/Create"
    header={
        'authority':'api.speedfan66.com',
        'accept':'application/json, text/plain, */*',
        'authorization': f'Bearer {token}',
        'content-type':'application/json',
        'origin': 'http://admin.howfunwedo.com',
        'referer': 'http://admin.howfunwedo.com/',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'        
    }
    data={
        'domainData': final_dcode,
        'gameSortData':[],
        'merchantId':merchantId,
        'type':1
    }

    result=requests.post(url,headers=header,json=data).json()

    return result

def add_order(token,dlist,order,merchantId=1):
    gamedata=[
        {"typeCode":"ELECTRONIC","typeName":"电子游戏"},
        {"typeCode":"LIVE","typeName":"真人视讯"},
        {"typeCode":"QPGAME","typeName":"棋牌游戏"},
        {"typeCode":"CPGAME","typeName":"彩票游戏"},
        {"typeCode":"HUNTER","typeName":"捕鱼游戏"},
        {"typeCode":"SPORTS","typeName":"体育竞技"},
        {"typeCode":"ESPORTS","typeName":"电子竞技"},
        {"typeCode":"HOTGAME","typeName":"热门游戏","sequence":"0"}
    ]
    final_domain=[ {'domain':x} for x in dlist ]
    for i in range(len(order)) :
         gamedata[i]['sequence']=order[i]
    gamedata.sort(key=lambda x : x['sequence'])
    # print(gamedata)
    # print(gamedata)
    # print(final_domain)

    url="https://api.speedfan66.com/api/admin/SysMerchantDomainCorrespondInfo/Create"
    header={
        'authority':'api.speedfan66.com',
        'accept':'application/json, text/plain, */*',
        'authorization': f'Bearer {token}',
        'content-type':'application/json',
        'origin': 'http://admin.howfunwedo.com',
        'referer': 'http://admin.howfunwedo.com/',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'        
    }

    data={
        'domainData':final_domain,
        'gameSortData':gamedata,
        'merchantId':merchantId,
        'type':2
    }

    result=requests.post(url,headers=header,json=data).json()
    return result

def add_statistics(domain,merchant,merchantId=1,cnzz_code="",google_code="",baidu_code=""):
    
    if str(merchantId) == "1":  
        url="http://api.modmojo.com/addScRec.php"
    elif str(merchantId) == "3":
        url="http://api2.modmojo.com/addScRec.php"

    data={
        'domain':domain,
        'merchant':merchant,
        'code': '{"cnzz":"'+cnzz_code+'","google":"'+google_code+'","baidu":"'+baidu_code+'"}'
    }

    # print(data)
    result=requests.post(url,data=data).text

    # print(result)
    return result

def check_white(token):
    url="https://api.speedfan66.com/api/admin/SysMerchantDomainInfo/PageList"
    header={
        'authority':'api.speedfan66.com',
        'accept':'application/json, text/plain, */*',
        'authorization': f'Bearer {token}',
        'content-type':'application/json',
        'origin': 'http://admin.howfunwedo.com',
        'referer': 'http://admin.howfunwedo.com/',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'        
    }

    data={
        'merchantId':1,
        'type':0,
        'pageIndex':1,
        'pageSize':1,
        'platformNameId':2
    }

    result=requests.post(url,headers=header,json=data).json()

    total_size=result['data']['total']

    data['pageSize'] = total_size

    result=requests.post(url,headers=header,json=data).json()

    domain_list=[ x['domain'] for x in result['data']['dataList'] if x ]
    return set(domain_list)

def main(input_dcodelist,input_order,statistics,merchant,domain_merchant):
    try : 
        testfile = open("scwhite.log","r+")
        testfile.close()
    except FileNotFoundError :
        testfile = open("scwhite.log","w+")
        testfile.close()

    with open("scwhite.log","r+") as f :
        
        token=get_token()
        dcodelist=[re.findall(r'[a-zA-Z.:0-9,-]+',x) for x in input_dcodelist.split('\n') if x ]
        domainlist=[ x[0] for x in dcodelist]
        # domain_str=",".join(domainlist)
        try:statistics_list=[(x[0],x[2]) for x in dcodelist if x]
        except: statistics_list = None 

        enable_https_dlist=[ domain for domain in domainlist if (":" in domain and domain.split(':')[1] != "80")]
        disable_https_dlist= list(set(domainlist) - set(enable_https_dlist))

        result=[]
        if enable_https_dlist : 
            result.append(str({"add_white":add_white(token,enable_https_dlist,merchantId=domain_merchant,all_domain=check_white(token))}))
        if disable_https_dlist : 
            result.append(str({"add_white":add_white(token,disable_https_dlist,merchantId=domain_merchant,all_domain=check_white(token))}))

        if str(domain_merchant) != "3" :
            result.append(str({"add_order":add_order(token,domainlist,input_order,domain_merchant)}))

        result.append(str({"add_invitation_code":add_code(token,dcodelist,domain_merchant)}))
        
        if statistics_list:
            if str(statistics) == "0" :
                for domain,cn_code in statistics_list : 
                    result.append(str({domain:add_statistics(domain,merchant,merchantId=domain_merchant,cnzz_code=cn_code)}))

            elif str(statistics) == "2" :
                for domain,gg_code in statistics_list : 
                    result.append(str({domain:add_statistics(domain,merchant,merchantId=domain_merchant,google_code=gg_code)}))
            
            elif str(statistics) == "1" :
                for domain,bd_code in statistics_list : 
                    result.append(str({domain:add_statistics(domain,merchant,merchantId=domain_merchant,baidu_code=bd_code)}))
        else : 
            result.append("{Error:statistics_list Failed to add statistics_code, because format error.}")

        print("\n".join(result))
        now_time=datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=8)))
        old_content=f.read()
        f.seek(0)
        f.write(f"\n{now_time}\n")
        f.write(f"\n{domainlist}\n")
        f.writelines("\n".join(result))
        f.write("\n"+old_content)
        


        return result



if __name__ == "__main__":
    # print(SC_WHITE_NAME)
    # print(SC_WHITE_PASSWORD)
    for i in range(1,7):
        domain="196999{}.com".format(i)
        print(domain)
    
    # print(add_statistics())
    # token=get_token()

    # input_="""bill225.com 11111 s9.cnzz.com:1281219776
    # bill225.live 22222 s4.cnzz.com:1281219778
    # bill225.cc 33333  v1.cnzz.com:1281216154"""

    # input_order="87563412"

    # main(input_,input_order,statistics=0,merchant="YCTEST")