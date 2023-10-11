import requests 
from dotenv import load_dotenv
import os 
from pprint import pprint
load_dotenv()
CF_TOKEN=os.getenv('CF_TOKEN')
 
class Client():
    header={
        "Authorization":f"Bearer {CF_TOKEN}",
        "Content-Type":"application/json",
    }
    def create_zone(self):
        url="https://api.cloudflare.com/client/v4/zones"
        # url="https://api.cloudflare.com/client/v4/accounts"
        data={
                "account": {
                    "id": "023e105f4ecef8ad9ca31a8372d0c353"
                },
                "name": "example.com",
                "type": "full"
            }
        
        result=requests.get(url,headers=self.header).json()

    
    def get_zones(self):
        page=1
        url=f"https://api.cloudflare.com/client/v4/zones?per_page=50&page={page}"
        data=requests.get(url,headers=self.header).json()
        total_pages=data['result_info']['total_pages']
        result=data['result']
        
        while page <= total_pages : 
            page+=1 
            url=f"https://api.cloudflare.com/client/v4/zones?per_page=50&page={page}"
            data=requests.get(url,headers=self.header).json()
            if data['result']:
                result+=data['result']
        
        return result
    
    def get_records(self,zone_id):
        page=1
        url=f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records?per_page=50000&page={page}"
        data=requests.get(url,headers=self.header).json()
        total_pages=data['result_info']['total_pages']
        result=data['result']
        while total_pages != 1 and page <= total_pages : 
            page+=1
            url=f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records?per_page=50000&page={page}"
            data=requests.get(url,headers=self.header).json()
            result+=data['result']

        return result
    
    def get_record_id(self,zone_id,domain,value):
        
        for record in self.get_records(zone_id) : 
            print(record)
            if record['name'] == domain and record['content'] == value: 
                record_id=record['id']
                break

        return record_id
    
    def get_zone_id(self,zones,domain):
        root='.'.join(domain.split('.')[-2::])
        for zone in zones : 
            if zone['name'] == root : 
                zone_id=zone['id']
                break
        return zone_id

    def add_record(self,zones,domain,dns_type,value):
        
        zone_id=self.get_zone_id(zones,domain)

        url=f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
        data={
            "content": value,
            "name": domain,
            "proxied": False,
            "type": dns_type,
            "ttl": 60
        }

        result=requests.post(url,headers=self.header,json=data).json()
        return result

    def modify_record(self,zones,domain,value,new_type,new_value):
        zone_id=self.get_zone_id(zones,domain)
        record_id=self.get_record_id(zone_id,domain,value)

        url=f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}"
        data={
            
            "content": new_value,
            "name": domain,
            "proxied": False,
            "type": new_type,
            "ttl": 60

        }
        result=requests.put(url,headers=self.header,json=data).json()
        return result 


    def del_record(self,zones,domain,value):
        zone_id=self.get_zone_id(zones,domain)
        record_id=self.get_record_id(zone_id,domain,value)

        url=f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}"
        result=requests.delete(url,headers=self.header)

        return result
    
def main(action,infos):
    cf_client=Client()
    zones=cf_client.get_zones()
    if action == "add" : 
        for info in infos : 
            try : 
                domain , dns_type , value = info 
            except ValueError : continue
            print(cf_client.add_record(zones,domain,str(dns_type).upper(),value))

    elif action == "modify" : 
        for info in infos :
            try : 
                domain,old_value,new_type,new_value=info
            except ValueError : continue
            cf_client.modify_record(zones,domain,old_value,str(new_type).upper(),new_value)


    else : 
        for info in infos:
            try :
                domain,value = info 
            except ValueError : continue
            cf_client.del_record(zones,domain,value)
    


if __name__=="__main__":
    cf_client=Client()
    zones=cf_client.get_zones()
    # datas=[
    #     ('test.1961002.app','CNA1697004942E','google.com'),
    #     ('test.1961002.app','CNAME','google.com'),
    #     ('test.1961002.app','A','1.1.1.1')
    #     ]
    # main('add',datas)
    # print(cf_client.create_zone())
    
    pprint(cf_client.get_records(cf_client.get_zone_id(zones,'1961002.app')))

    # print(cf_client.del_record(zones,"*.1961002.app","1.1.1.1"))
    # print(cf_client.modify_record(zones,'test.1961002.app','1.1.1.1','A','2.2.2.2'))
    # print(cf_client.get_record_id(zones,'www.1961002.app'))
    # print(cf_client.add_record(zones,"*.1961002.app",'A','2.2.2.2'))