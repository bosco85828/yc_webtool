import requests
import re
from bs4 import BeautifulSoup
import threading

def get_yc_ssl(domain):
    url="http://yc-api.cdnvips.net/Cdn/getCert"
    data={
        'domain':domain
    }

    result=requests.post(url,data=data).json()

    return result

if __name__ == "__main__":
    domain="member23.site"
    data=get_yc_ssl(domain)
    cert=data['cert']
    key=data['key']

    print("is cert == key? {}".format(cert==key))

