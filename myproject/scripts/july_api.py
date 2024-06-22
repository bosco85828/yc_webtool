import requests
from dotenv import load_dotenv
import os 
import base64

load_dotenv()
JULY_KEY=os.getenv('JULY_KEY')
JULY_SECRET=os.getenv('JULY_SECRET')

# def get_token(func):
#     def wrapper(*args,**kargs):

#         url="http://34.81.219.244:8080/APIAccessTokenService/getAPIAccessToken"
#         data={
#             "type": "admin",
#             "accessKeyId": JULY_KEY,
#             "accessKey": JULY_SECRET
#         }
#         result=requests.post(url,json=data).json()
#         if result['code'] == 200:
#             token=result['data']['token']
#         else : 
#             print(result)
#             token=None
        
#         return func(token,*args,**kargs)
#     return wrapper 

def get_token():
    url="http://34.81.219.244:8080/APIAccessTokenService/getAPIAccessToken"
    data={
        "type": "admin",
        "accessKeyId": JULY_KEY,
        "accessKey": JULY_SECRET
    }
    result=requests.post(url,json=data).json()
    if result['code'] == 200:
        token=result['data']['token']
    else : 
        print(result)
        token=None
    
    return token

class Client():

    token=get_token()
    header={
            "X-Edge-Access-Token":token,
            "Content-Type":"application/json"
        }
    
    def get_traffic(self,day):
        url="http://34.81.219.244:8080/TrafficDailyStatService/findTrafficDailyStatWithDay"
        
        data={
            "day":str(day)
        }
        
        result=requests.post(url,headers=self.header,json=data).json()

        return result

    
    def get_users(self):
        url="http://34.81.219.244:8080/UserService/listEnabledUsers"
        url="http://34.81.219.244:8080/UserService/countAllEnabledUsers"
        data={
            'size':100,
            'offset':2
        }

        # result=requests.post(url,headers=self.header,json=data).json()
        result=requests.post(url,headers=self.header).json()
        # return result['data']['users']
        return result
    def get_ssl_id(self):
        url="http://34.81.219.244:8080/SSLCertService/listSSLCerts"
        # url="http://34.81.219.244:8080/SSLCertService/findEnabledSSLCertConfig"
        data={
            # 'isAvailable':True,
            # 'isExpired':False,
            'domains':['24712.xyz'],
            'size':100
        }

        result=requests.post(url,headers=self.header,json=data).json()['data']['sslCertsJSON']
        # result=requests.post(url,headers=self.header).json()
        decoded_bytes = base64.b64decode(result)
        decoded_string = decoded_bytes.decode('utf-8')
        return decoded_string



    def add_domain(self):
        url="http://34.81.219.244:8080/ServerService/createBasicHTTPServer"
        data={
            # 'name':"bosco.com", #網站名稱
            'userId':0,
            'domains':['bosco1.com','bosco2.com'],
            'originAddrs':["http://example.com"],
            'enableWebsocket':True,
            # 'serverNamesJSON':[
            #                     {
            #         "name": "",
            #         "type": "full",
            #         "subNames": ["example.com", "google.com", "facebook.com"]
            #     }
            # ],
            'nodeClusterId':1, 


        }
        result=requests.post(url,headers=self.header,json=data).json()
        return result

    def get_cluster_id(self):
        url="http://34.81.219.244:8080/NodeClusterService/findAllEnabledNodeClusters"
        # data={
        #     'size':100,
        # }
        result=requests.post(url,headers=self.header).json()
        if str(result['code']) == "200" : 
            return result['data']['nodeClusters']
        else : 
            return result
        
    

if __name__ == "__main__":
    client=Client()
    day=20231030
    # print(client.get_traffic(day))
    # print(client.add_domain())
    print(client.get_ssl_id())
    # print(len(client.get_cluster_id()))

