import requests
from bs4 import BeautifulSoup
import re
def compare_cnzz(domain):
    url="https://{}/".format(domain)
    result=requests.get(url)
    soup=BeautifulSoup(result.text,'lxml')
    data=soup.find_all('script')

    
    ans=[ str(x) for x in data if x != None and "cnzz.com" in str(x) and "cnzz_s_tag" not in str(x) ]
    
    
    if ans : 
        cnzz_id=re.search(r'id=(\d+)',ans[0]).group(1)
        cnzz_domain=re.search(r'https://([0-9a-zA-Z.-]+)',ans[0]).group(1)
    
    else : 
        return {domain:"Can't find cnzz's code on {}.".format(domain)}
    
    return {domain:{cnzz_domain:cnzz_id}}

if __name__ == "__main__":
    print(compare_cnzz('193452.com'))







