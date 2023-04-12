from dotenv import load_dotenv
import os 
import requests
import re
import cdnw_client2
import json
from pprint import pprint
from datetime import datetime,timezone,timedelta
load_dotenv()
CDNW_ACCESSKEY=os.getenv('CDNW_ACCESSKEY')
CDNW_SECRETKEY=os.getenv('CDNW_SECRETKEY')
now=datetime.now().strftime("%Y-%m-%d")

global AccessKey, SecretKey
AccessKey = CDNW_ACCESSKEY
SecretKey = CDNW_SECRETKEY

def upload_cdnw(cert_name,cert,key):
    host='api.cdnetworks.com'
    http_method = 'POST'
    uri='/api/certificate'
    post_request_body={
        'name':now+"_"+cert_name,
        'certificate':cert,
        'privateKey':key
    }
    
    data=cdnw_client2.send_request(AccessKey, SecretKey, host, uri, http_method, post_request_body).json()

    return data

def check_cdnw_certid(domain):
    host='api.cdnetworks.com'
    http_method = 'GET'
    uri='/api/ssl/certificate'
    post_request_body={}
    data=cdnw_client2.send_request(AccessKey, SecretKey, host, uri, http_method, post_request_body).json()['ssl-certificate']
    # print(data)
    # certid_list=[ x for x in data if domain in x['related-domains']]
    certid_list=[]
    for x in data : 
        if x['name'] == now+'_'+domain : 
            return x['certificate-id']

        else :
            domain_list=x['dns-names']
            # print(domain_list)
            root_domain=".".join(domain.split('.')[-2:])
            # print(root_domain)
            if domain in domain_list or "*."+root_domain in domain_list : 
                certid_list.append((x['certificate-id'],x['certificate-validity-to']))
    # print(certid_list)    
    if len(certid_list) > 1 :
        temp_time=datetime.strptime('2020-01-01 00:00:01','%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
        temp_id=""
        for certid in certid_list : 
            cert_time=datetime.strptime(certid[1], '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
            # print(cert_time)
            if cert_time > temp_time : 
                temp_time = cert_time 
                temp_id = certid[0]

        return temp_id

    try :return certid_list[0][0]

    except IndexError : 
        return None

def add_domain(domain,origin_protocol='http',refer=None):
    
    yc_dict=get_ycinfo(domain)
    if yc_dict :
        origins=[ re.search(r'http.*\/\/([^\/]+)',x).group(1) for x in yc_dict['ip'].split(',') if x ]
        origin_ports=yc_dict['sourcePort'].split(',')
        print("origin: {}".format(";".join(origins)))
        print("origin: {}".format(";".join(origin_ports)))
        origin = ";".join(origins)
        origin_port=  ";".join(origin_ports)
    
    else : 
        return json.dumps({'Action':'GetYccdnInfo','Response':'Domain does not exist on YCCDN or need to add whitelist on target server.'}) 

    host='api.cdnetworks.com'
    uri='/cdnw/api/domain'
    http_method = 'POST'
    post_request_body={
        "version": "1.0.0",
        "contract-id": "40016167",
        "item-id": "10",
        "accelerate-no-china":True,
        'domain-name':domain,
        'referenced-domain-name':refer,
        'origin-config':{
            'origin-ips':origin,
        },
        "ssl":{
             "use-ssl":False,
        }
    }
    
    if str(origin_port) == "443":
        origin_protocol = "https"
    elif str(origin_port) == "80":
        origin_protocol = "http"
    
    
    print(post_request_body)
    response=cdnw_client2.send_request(CDNW_ACCESSKEY,CDNW_SECRETKEY,host,uri,http_method,post_request_body).json()
    

    if response['message'] == 'success' or response['code'] == 'DomainAlreadyExists' : 
        print(json.dumps({'Action':'SetOriginProtocol','Responese':set_origin_protocol(domain,origin_port,origin_protocol)}))
        print(json.dumps({'Action':'SetOriginAddress','Responese':set_origin_address(domain,origin)}))
        
    
        if yc_dict['certificatesContent'] : 
            cert = yc_dict['certificatesContent']
            key = yc_dict['privateKey']
            status = upload_cdnw(domain,cert,key)['message']
            print(json.dumps({'Action':'UploadSSL','Responese':status}))

            if status == 'success' or "already" in status : 
                print(json.dumps({'Action':'ContactSSL','Responese':contact_ssl(domain)}))

        if yc_dict['isForceHttps'] :         
            print(json.dumps({'Action':'ForceHttps','Responese':add_forcehttps(domain)}))

    return json.dumps({'Action':'AddDomain','Responese':response})

def contact_ssl(domain):
    host='api.cdnetworks.com'
    uri='/cdnw/api/domain/{}'.format(domain)
    http_method = 'PUT'
    
    sslid = check_cdnw_certid(domain)
    # print("sslid: {}".format(sslid)) 
    post_request_body={
        "ssl":{
             "use-ssl":False,
             "ssl-certificate-id":sslid
             },
    }

    if sslid : post_request_body['ssl']['use-ssl'] = True

    return cdnw_client2.send_request(AccessKey, SecretKey, host, uri, http_method, post_request_body).json()

def set_origin_address(domain,origin):
    host='api.cdnetworks.com'
    uri='/cdnw/api/domain/{}'.format(domain)
    http_method = 'PUT'
    
    post_request_body={
        "origin-config": {
            "origin-ips": origin,
            }
    }

    return cdnw_client2.send_request(AccessKey, SecretKey, host, uri, http_method, post_request_body).json()

def get_ycinfo(domain):
    url="http://yc-api.cdnvips.net/Cdn/getYcDomainInfo"
    data={
        "domain":domain
    }
    try : 
        response=requests.post(url,data=data).json()
    except:
        return None
        # return json.dumps({'Action':'GetYccdnInfo','Response':'Please add whitelist on target server.'})

    return response

def set_origin_protocol(domain,port,protocol=None):
    host = 'api.cdnetworks.com'
    http_method = 'PUT'
    uri = "/api/config/back2originrewrite/{}".format(domain)

    post_request_body = {
 "backToOriginRewriteRule":{
 "protocol":protocol,
 "port":port
 }
}
    return cdnw_client2.send_request(CDNW_ACCESSKEY,CDNW_SECRETKEY,host,uri,http_method,post_request_body).json()

def add_forcehttps(domain):
    host = 'api.cdnetworks.com'
    http_method = 'PUT'
    uri = "/api/config/InnerRedirect/{}".format(domain)
    post_request_body = {
        'rewrite-rule-settings':[
            {
                'path-pattern':'.*',
                'ignore-letter-case':True,
                'publish-type':'Cache',
                'before-value':'^http://([^/]+/.*)',
                'after-value':'301:https://$1',
                'rewrite-type':'after'
            },
        ]
    }

    return cdnw_client2.send_request(AccessKey, SecretKey, host, uri, http_method, post_request_body).json()

def delete_domain(domainlist):
    result_log=[]
    
    for domain in domainlist : 
        host = 'api.cdnetworks.com'
        http_method = 'DELETE'
        uri="/api/domain/{}".format(domain)
        post_request_body = {}
        result=cdnw_client2.send_request(AccessKey, SecretKey, host, uri, http_method, post_request_body).json()
        
        result_log.append(json.dumps({'Domain':domain , 'Result': result}))
    
    print("\n".join(result_log))
    now_time=datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=8)))
    try:
        with open('delete_cdnw.log','r+') as f : 
            old_content=f.read()
            f.seek(0)
            f.write(f"\n{now_time}\n")
            f.write("\n".join(result_log))
            f.write("\n"+old_content)
    except FileNotFoundError :
        with open('delete_cdnw.log','w+') as f : 
            f.write(f"\n{now_time}\n")
            f.write("\n".join(result_log))

def main(domainlist,refer):

    result_log=[]
    for domain in domainlist :
        
        result_log.append(json.dumps({'Domain':domain,'Result':json.loads(add_domain(domain,refer=refer))}))
    
    print("\n".join(result_log))
    now_time=datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=8)))
    try:
        with open('sync_cdnw.log','r+') as f : 
            old_content=f.read()
            f.seek(0)
            f.write(f"\n{now_time}\n")
            f.write("\n".join(result_log))
            f.write("\n"+old_content)
    except FileNotFoundError :
        with open('sync_cdnw.log','w+') as f : 
            f.write(f"\n{now_time}\n")
            f.write("\n".join(result_log))
        
    
   


if __name__ == "__main__":
    
    # host = 'api.cdnetworks.com'
    # http_method = 'GET'
    # # if api support get method , please add parameters after uri, exp: test?a=1&b=2&c=3
    # uri = "/api/config/InnerRedirect/www.bosco.live"
    # # if api is a post method, please put parameters as dict
    # post_request_body = {}

    # print(cdnw_client2.send_request(AccessKey, SecretKey, host, uri, http_method, post_request_body).json())

    # https://api.cdnetworks.com/cdnw/api/domain/*
    # print(delete_domain('m.bosco.live'))
    print(contact_ssl('www.bosco.live'))
    # print(set_origin_address('m.bosco.live','1.1.1.1'))
    # print(contact_ssl('m.bosco.live'))
    # print(check_cdnw_certid('m.bosco.live'))
    # data=get_ycinfo('www.bosco.live')
    # if data['isForceHttps'] : 
    #     print(123)

    # pprint(data['certificatesContent'])
    # pprint(data['privateKey'])

    
    # print(add_forcehttps('www.bosco.live'))
