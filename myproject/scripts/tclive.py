import json
import types
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.live.v20180801 import live_client, models
from dotenv import load_dotenv
import os 
from pprint import pprint
import json
import math
load_dotenv()
TC_ID=os.getenv('TC_ID')
TC_KEY=os.getenv('TC_KEY')

#獲得單一分頁域名列表
def get_domains_row(client,page):
    # 实例化一个请求对象,每个接口都会对应一个request对象
    req = models.DescribeLiveDomainsRequest()
    params = {
        "PageSize": 100,
        "PageNum": page
    }
    req.from_json_string(json.dumps(params))

    # 返回的resp是一个DescribeLiveDomainsResponse的实例，与请求对象对应
    resp = client.DescribeLiveDomains(req)
    # 输出json格式的字符串回包     
    data=json.loads(resp.to_json_string())
    
    return data

#檢查總頁數並且獲得域名列表加總
def get_domains(client):
    
    page=1
    result=get_domains_row(client,page)

            
    if result['AllCount'] > 100 :         
        all_page=math.ceil(result['AllCount']/100 )
        datas=result['DomainList']
        page+=1
        
        while page <= all_page : 
            datas += get_domains_row(client,page)['DomainList']
            page += 1 

        else : return datas 

            
    else : return result['DomainList']
    
def enable_domain(client,domain):
     # 实例化一个请求对象,每个接口都会对应一个request对象
    req = models.EnableLiveDomainRequest()
    params = {
        "DomainName": domain
    }
    req.from_json_string(json.dumps(params))
    # 返回的resp是一个EnableLiveDomainResponse的实例，与请求对象对应
    resp = client.EnableLiveDomain(req)
    # 输出json格式的字符串回包
    return json.loads(resp.to_json_string())

def disable_domain(client,domain):
     # 实例化一个请求对象,每个接口都会对应一个request对象
    req = models.ForbidLiveDomainRequest()
    params = {
        "DomainName": domain
    }
    req.from_json_string(json.dumps(params))
    # 返回的resp是一个EnableLiveDomainResponse的实例，与请求对象对应
    resp = client.ForbidLiveDomain(req)
    # 输出json格式的字符串回包
    return json.loads(resp.to_json_string())

def main(_type,domain=None): 
    
    try:
        # 实例化一个认证对象，入参需要传入腾讯云账户 SecretId 和 SecretKey，此处还需注意密钥对的保密
        # 代码泄露可能会导致 SecretId 和 SecretKey 泄露，并威胁账号下所有资源的安全性。密钥可前往官网控制台 https://console.tencentcloud.com/capi 进行获取
        cred = credential.Credential(TC_ID, TC_KEY)
        # 实例化一个http选项，可选的，没有特殊需求可以跳过
        httpProfile = HttpProfile()
        httpProfile.endpoint = "live.tencentcloudapi.com"

        # 实例化一个client选项，可选的，没有特殊需求可以跳过
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        
        # 实例化要请求产品的client对象,clientProfile是可选的
        client = live_client.LiveClient(cred, "", clientProfile)
        
        if _type=="get":
            result=get_domains(client)
            domains=[]
            for temp in result : 
                domains.append(
                    {
                        'domain':temp['Name'],
                        'type':temp['Type'],
                        'status':temp['Status'],                        
                        'cname':temp['TargetDomain']
                    }
                )

            return domains
             
        elif _type=="enable":
            result=enable_domain(client,domain)
            return result
        
        elif _type=="disable":
            result=disable_domain(client,domain)
            return result

    except TencentCloudSDKException as err:
        print(err)

if __name__=="__main__":
    print(main("disable","pull.lbqssss.top"))