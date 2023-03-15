from OpenSSL import crypto 
from datetime import datetime,timezone,timedelta
import pytz
import requests 
import pydig
import os 





def get_yc_ssl(domain):
    url="http://yc-api.cdnvips.net/Cdn/getCert"
    data={
        'domain':domain
    }

    result=requests.post(url,data=data).json()

    return result

def compare_cert(cert_data):

    cert=crypto.load_certificate(crypto.FILETYPE_PEM,cert_data.encode())
    not_before=datetime.strptime(cert.get_notBefore().decode(),'%Y%m%d%H%M%SZ')
    tz=pytz.timezone('UTC')

    now=datetime.now(tz)
    now = now.replace(tzinfo=None)
    


    print(now)
    print(not_before)
    

    diff_day = (now-not_before).total_seconds()/86400

    return diff_day


# cert=get_yc_ssl('m.bosco.live')['cert']
# print(cert)


# print(compare_cert(cert))
domain="m.bosco.live"

resolver=pydig.Resolver(
    executable='/usr/bin/dig',
    nameservers=["8.8.8.8",],
    additional_args=['+time=3',]
)


data = pydig.query('m.bosco.live','CNAME')
data=pydig.query(data[0],'CNAME')
print(data)
