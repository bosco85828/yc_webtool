from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkalidns.request.v20150109.AddDomainRecordRequest import AddDomainRecordRequest
from aliyunsdkalidns.request.v20150109.AddDomainRequest import AddDomainRequest
from datetime import datetime,timezone,timedelta
global customer
customer={
    'sc':{'id':'LTAI5tLLhoNFCreJ81jGFAnw','secret':'OweIwUzXup2251GHusrQLdBPPIKvqV'}
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

if __name__ == "__main__":
    input_domain=['bosco.com','bill2.com','bill3.com']
    print(add_domain('sc',input_domain))