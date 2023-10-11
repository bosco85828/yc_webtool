import requests
from dotenv import load_dotenv
import os 

load_dotenv()
JULY_KEY=os.getenv('JULY_KEY')
JULY_SECRET=os.getenv('JULY_SECRET')

def get_token(func):
    def wrapper(*args,**kargs):

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
        
        return func(token,*args,**kargs)
    return wrapper 


    
class Client():
    @staticmethod
    @get_token
    def get_traffic(token,day):
        url="http://34.81.219.244:8080/TrafficDailyStatService/findTrafficDailyStatWithDay"
        header={
            "X-Edge-Access-Token":token,
            "Content-Type":"application/json"
        }
        data={
            "day":str(day)
        }
        
        result=requests.post(url,headers=header,json=data).json()

        return result




if __name__ == "__main__":
    client=Client()
    day=20231001
    print(client.get_traffic(day))

