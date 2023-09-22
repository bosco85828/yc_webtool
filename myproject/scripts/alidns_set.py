from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkalidns.request.v20150109.AddDomainRecordRequest import AddDomainRecordRequest
from aliyunsdkalidns.request.v20150109.AddDomainRequest import AddDomainRequest
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest
from aliyunsdkalidns.request.v20150109.SetDomainRecordStatusRequest import SetDomainRecordStatusRequest
import json
from datetime import datetime,timezone,timedelta
from dotenv import load_dotenv
import os 

load_dotenv()
ALI_SC_ID=os.getenv('ALI_SC_ID')
ALI_SC_SECRET=os.getenv('ALI_SC_SECRET')

global customer
customer={
    'sc':{'id':ALI_SC_ID,'secret':ALI_SC_SECRET}
}

def add_domain(c_name,dlist):
    client = AcsClient(
        customer[c_name]['id'],
        customer[c_name]['secret'],
        'cn-shenzhen'
    )
    result_list=[]
    for domain in dlist:
        request_=AddDomainRequest()
        request_.set_DomainName(domain)
        
        try:
            result=client.do_action_with_exception(request_)
            if result : 
                result_list.append(str({domain:"success"}))
        except Exception as e :
            # result_list.append(dir(e))
            result_list.append(str({domain:e.message}))
            
    try : 
        with open('alidns_adddomain.log',"r+") as f:
            now_time=datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=8)))
            old_content=f.read()
            f.seek(0)
            f.write(f"\n{now_time}\n")
            f.writelines("\n".join(result_list))
            f.write("\n"+old_content)
    
    except FileNotFoundError:
        with open('alidns_adddomain.log',"w+") as f:
            now_time=datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=8)))
            f.write(f"\n{now_time}\n")
            f.writelines("\n".join(result_list))

    return result_list

def add_record(c_name,root,host,type,value):

    client = AcsClient(
        customer[c_name]['id'],
        customer[c_name]['secret'],
        'cn-shenzhen'
    )

    request_=AddDomainRecordRequest()
    request_.set_accept_format('json')
    request_.set_Value(value)
    request_.set_Type(type)
    request_.set_RR(host)
    request_.set_DomainName(root)

    result=client.do_action_with_exception(request_)
    return str(result, encoding='utf-8')

def get_domain_record(c_name,root,host=None):
    client = AcsClient(
        customer[c_name]['id'],
        customer[c_name]['secret'],
        'cn-shenzhen'
    )

    request_=DescribeDomainRecordsRequest()
    request_.set_accept_format('json')
    request_.set_DomainName(root)
    request_.set_PageSize(500)
    if host:
        request_.set_RRKeyWord(host)

    result=client.do_action_with_exception(request_)
    return json.loads(str(result,encoding='utf-8'))
    # return json.loads(result)


def change_domain_record(c_name,record_id,host,type_,value):
    client = AcsClient(
        customer[c_name]['id'],
        customer[c_name]['secret'],
        'cn-shenzhen'
    )

    request_=UpdateDomainRecordRequest()
    request_.set_RecordId(record_id)
    request_.set_RR(host)
    request_.set_Type(type_)
    request_.set_Value(value)

    result=client.do_action_with_exception(request_)
    return json.loads(str(result,encoding='utf-8')) 

def disable_record(c_name,record_id):
    client = AcsClient(
        customer[c_name]['id'],
        customer[c_name]['secret'],
        'cn-shenzhen'
    )

    request_=SetDomainRecordStatusRequest()
    request_.set_accept_format('json')
    request_.set_RecordId(record_id)
    request_.set_Status("Disable")

    result=client.do_action_with_exception(request_)
    return json.loads(str(result,encoding='utf-8')) 

if __name__ == "__main__":
    input_domain=['bosco.com']
    # print(add_domain('sc',input_domain))
    records=get_domain_record('sc','bosco.com','www')['DomainRecords']['Record']
    print(records)
    for record in records : 
        print(record)
        if record['RR'] == "www" : 
            record_id = record['RecordId']
    
    # print(disable_record('sc','818288189989113856'))
    
    # print(record_id)

    # print(change_domain_record('sc',record_id,'www','CNAME','bosco.live'))