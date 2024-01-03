from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkalidns.request.v20150109.AddDomainRecordRequest import AddDomainRecordRequest
from aliyunsdkalidns.request.v20150109.AddDomainRequest import AddDomainRequest
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest
from aliyunsdkalidns.request.v20150109.SetDomainRecordStatusRequest import SetDomainRecordStatusRequest
from aliyunsdkalidns.request.v20150109.DeleteDomainRecordRequest import DeleteDomainRecordRequest

import json
from datetime import datetime,timezone,timedelta
from pprint import pprint
from dotenv import load_dotenv
import os 

load_dotenv()
ALI_SC_ID=os.getenv('ALI_SC_ID')
ALI_SC_SECRET=os.getenv('ALI_SC_SECRET')
ALI_KIM_ID=os.getenv('ALI_KIM_ID')
ALI_KIM_SECRET=os.getenv('ALI_KIM_SECRET')

global customer
customer={
    'sc':{'id':ALI_SC_ID,'secret':ALI_SC_SECRET},
    'kim':{'id':ALI_KIM_ID,'secret':ALI_KIM_SECRET}
}

def add_domain(c_name,domain):
    client = AcsClient(
        customer[c_name]['id'],
        customer[c_name]['secret'],
        'cn-shenzhen'
    )
    result_list=[]

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

def add_record(c_name,domain,type,value):
    split_domain = domain.split('.')
    if len(split_domain) < 3 :
        root = domain 
        host = "@"
    else :
        root = ".".join(split_domain[-2::])
        host = ".".join(split_domain[0:-2])
    
    print('root:' + root)
    print('host:' + host)
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
    page=1
    response_list=[]
    while True : 
        request_=DescribeDomainRecordsRequest()
        request_.set_accept_format('json')
        request_.set_DomainName(root)
        request_.set_PageSize(500)
        request_.set_PageNumber(page)

        if host:
            request_.set_RRKeyWord(host)

        response=client.do_action_with_exception(request_)
        data=json.loads(str(response,encoding='utf-8'))['DomainRecords']['Record']
        
        if data : 
            response_list+=data
            page+=1
        else : 
            break
    
    results=[]
    for data in response_list : 
        results.append({
            'domain':str(data['RR']) + '.' + str(data['DomainName']),
            'type':data['Type'],
            'value':data['Value'],
            'ttl':data['TTL'],
            'status':data['Status'],
            'record_id':data['RecordId']
        })
    
    return results
    # return json.loads(str(response,encoding='utf-8'))
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

def swich_record(c_name,record_id,type_='disable'):
    client = AcsClient(
        customer[c_name]['id'],
        customer[c_name]['secret'],
        'cn-shenzhen'
    )

    request_=SetDomainRecordStatusRequest()
    request_.set_accept_format('json')
    request_.set_RecordId(record_id)
    request_.set_Status(type_)

    result=client.do_action_with_exception(request_)
    return json.loads(str(result,encoding='utf-8')) 

def delete_record(c_name,record_id):
    client = AcsClient(
        customer[c_name]['id'],
        customer[c_name]['secret'],
        'cn-shenzhen'
    )

    request_=DeleteDomainRecordRequest()
    request_.set_accept_format('json')
    request_.set_RecordId(record_id)

    result=client.do_action_with_exception(request_)
    return json.loads(str(result,encoding='utf-8')) 

def compare(datas,domain,old_value):
    for data in datas:
        if data['domain'].split('.')[0] == '@' : 
            data['domain']='.'.join(data['domain'].split('.')[-2::])
        if domain == data['domain'] and old_value == data['value'] :            
            return data['record_id']

def main(action,c_name,infos):
    if action == "add_domain":
        for domain in infos : 
            domain=domain[0]
            print(add_domain(c_name,domain))

    elif action == "add_record":
        for info in infos:
            domain , type_ , value = info
            add_record(c_name,domain,type_,value)

    elif action == "get_record":
        domain = infos[0][0]
        print(domain)
        return get_domain_record(c_name,domain)
            
    elif action == "switch":
        for info in infos : 
            domain , value , type_ = info 
            if len(domain.split('.')) > 2 : 
                root=".".join(domain.split('.')[-2::])
            else : 
                root=domain

            datas=get_domain_record(c_name,root)
            
            record_id=compare(datas,domain,value)            
            print(swich_record(c_name,record_id,type_))
            
    
    elif action == "modify":
        for info in infos : 

            domain , old_value , new_type , new_value = info 

            if len(domain.split('.')) > 2 : 
                root=".".join(domain.split('.')[-2::])
                host= ".".join(domain.split('.')[0:-2])
            else : 
                root=domain
                host='@'
        
            datas=get_domain_record(c_name,root)
            record_id=compare(datas,domain,old_value)        
            change_domain_record(c_name,record_id,host,new_type,new_value)
    
    elif action == "delete":
        for info in infos:
            domain,value=info
            if len(domain.split('.')) > 2 : 
                root=".".join(domain.split('.')[-2::])
                host= ".".join(domain.split('.')[0:-2])
            else : 
                root=domain
                host='@'

            datas=get_domain_record(c_name,root)
            record_id=compare(datas,domain,value)     
            delete_record(c_name,record_id)


if __name__ == "__main__":
    pprint(main('switch','kim',[('1960000.app.klchemicals.net',"cdn-node-hk-common-8.klchemicals.net",'enable')]))
    # pprint(main('change_record','sc',[('www.bosco.com',"bosco.live",'A',"2.2.2.2")]))
    # print(delete_record('sc','818282108218929152'))
    # pprint(len(main('get_record','kim',[('klchemicals.net',)])))
    # print(add_domain('sc',input_domain))
    # records=get_domain_record('sc','bosco.com','www')
    # print(records)
    # for record in records : 
    #     print(record)
    #     if record['RR'] == "www" : 
    #         record_id = record['RecordId']
    
    # print(disable_record('sc','818288189989113856'))
    
    # print(record_id)

    # print(change_domain_record('sc',record_id,'www','CNAME','bosco.live'))