import requests
import re
from bs4 import BeautifulSoup
import threading
import cdnw_client
import time
from datetime import datetime,timezone,timedelta
global AccessKey,SecretKey,host
AccessKey = 'qG3fh4K9ZFbapLm8ASHsdeyeAF9JmlFv6mbK'
SecretKey = 'J6NZfEAVLKEZ4nDWyaSzpFFVYtYERVWSDQYayDNcW0l5uCwAJKEHVBYgLCas0cq6'
host = 'api.cdnetworks.com'

def get_yc_ssl(domain):
    url="http://yc-api.cdnvips.net/Cdn/getCert"
    data={
        'domain':domain
    }

    result=requests.post(url,data=data).json()

    return result

def upload_cdnw(cert_name,cert,key):
    http_method = 'POST'
    uri='/api/certificate'
    post_request_body={
        'name':cert_name,
        'certificate':cert,
        'privateKey':key
    }
    
    data=cdnw_client.send_request(AccessKey, SecretKey, host, uri, http_method, post_request_body)

    return data

def check_cdnw_certid(cert_name):
    http_method = 'GET'
    uri='/api/ssl/certificate'
    post_request_body={}
    data=cdnw_client.send_request(AccessKey, SecretKey, host, uri, http_method, post_request_body)
    soup=BeautifulSoup(data.text,'xml')
    certs=soup.find_all('ssl-certificate')
    cert=[ x for x in certs if x.find('name').get_text()==cert_name ]
    
    return cert[0].find('certificate-id').get_text()
    
    
    


def set_cdnwdomain_cert(domain,certid):
    http_method = "PUT"
    uri='/api/domain/{}'.format(domain)
    post_request_body={
        "ssl":{
             "use-ssl":True,
            #  "use-for-sni":"",
             "ssl-certificate-id":certid
             }
    }
    data=cdnw_client.send_request(AccessKey, SecretKey, host, uri, http_method, post_request_body)
    soup=BeautifulSoup(data.text,'xml')
    result=soup.find('message').get_text()

    return result

def main(input_domain):
    domainlist=re.findall(r'[a-zA-Z0-9.-]+',input_domain)
    # print(domainlist)
    result_log=[]
    for domain in domainlist : 
        data=get_yc_ssl(domain)
        cert=data['cert']
        key=data['key']

        if cert and key : 
            upload_result=upload_cdnw(domain,cert,key)
            if upload_result.status_code == 200 :
                while True:
                    try:
                        certid=check_cdnw_certid(domain)

                    except IndexError:
                        time.sleep(2)
                        continue

                    result_log.append(str({domain:set_cdnwdomain_cert(domain,certid)}))
                    break

            elif "already" in upload_result.text : 
                certid=check_cdnw_certid(domain)
                result_log.append(str({domain:set_cdnwdomain_cert(domain,certid)}))

            else :
                soup=BeautifulSoup(upload_result.text,'xml')
                result_msg=soup.find('message').get_text()
                result_log.append(str({domain:result_msg})) 
        else : 
            result_log.append(str({domain:"YCCDN SSL does not exist."})) 

    
    
    print("\n".join(result_log))
    now_time=datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=8)))
    try:
        with open('cdnw_uploadssl.log','r+') as f : 
            old_content=f.read()
            f.seek(0)
            f.write(f"\n{now_time}\n")
            f.write("\n".join(result_log))
            f.write("\n"+old_content)
    except FileNotFoundError :
        with open('cdnw_uploadssl.log','w+') as f : 
            f.write(f"\n{now_time}\n")
            f.write("\n".join(result_log))
            


if __name__ == "__main__":
    domain="test.bosco.live"
    data=get_yc_ssl(domain)
    cert=data['cert']
    key=data['key']
    print(upload_cdnw(domain,cert,key).text)
    # print(data)
    # print(bool(cert))
    # print(cert)
    # print(len(cert))
    # print(cert)
    # print(key)
    # print("is cert == key? {}".format(cert==key))

#     cert="""-----BEGIN CERTIFICATE-----
# MIIEUjCCAzqgAwIBAgISBFMNwkFH/z6UCnpWZ7JF5zqqMA0GCSqGSIb3DQEBCwUA
# MDIxCzAJBgNVBAYTAlVTMRYwFAYDVQQKEw1MZXQncyBFbmNyeXB0MQswCQYDVQQD
# EwJSMzAeFw0yMzAzMDIwNDEzMzdaFw0yMzA1MzEwNDEzMzZaMBcxFTATBgNVBAMM
# DCouYm9zY28ubGl2ZTBZMBMGByqGSM49AgEGCCqGSM49AwEHA0IABLslG5ZC52WH
# /8vuTiYvmxx4znKZd7TZNcH/yHAJUWLrnlCuskDfNOJcY99AHOMP3DWifhOxvFTg
# XU4/hzDoRu6jggJGMIICQjAOBgNVHQ8BAf8EBAMCB4AwHQYDVR0lBBYwFAYIKwYB
# BQUHAwEGCCsGAQUFBwMCMAwGA1UdEwEB/wQCMAAwHQYDVR0OBBYEFJNnmttvzZSa
# oNoPw+Wwdrds7T0qMB8GA1UdIwQYMBaAFBQusxe3WFbLrlAJQOYfr52LFMLGMFUG
# CCsGAQUFBwEBBEkwRzAhBggrBgEFBQcwAYYVaHR0cDovL3IzLm8ubGVuY3Iub3Jn
# MCIGCCsGAQUFBzAChhZodHRwOi8vcjMuaS5sZW5jci5vcmcvMBcGA1UdEQQQMA6C
# DCouYm9zY28ubGl2ZTBMBgNVHSAERTBDMAgGBmeBDAECATA3BgsrBgEEAYLfEwEB
# ATAoMCYGCCsGAQUFBwIBFhpodHRwOi8vY3BzLmxldHNlbmNyeXB0Lm9yZzCCAQMG
# CisGAQQB1nkCBAIEgfQEgfEA7wB1AHoyjFTYty22IOo44FIe6YQWcDIThU070ivB
# OlejUutSAAABhqC9e80AAAQDAEYwRAIgPfDO3dbEk9I3xjWHi3fbUlevHhHxIkcH
# nTGutHUCLLgCIGTzK6ZGFntbY0iyfoT6UFU5JlD3T5RhUw9R5u63H+xoAHYAtz77
# JN+cTbp18jnFulj0bF38Qs96nzXEnh0JgSXttJkAAAGGoL173QAABAMARzBFAiEA
# +mHszAfKUahUOvnuoYfQggb3++3O2vJXAc4ooNMCKyACIAfCY9/bSxYC8Kq4SG8b
# AQ6LG9b3CdP22MUNuZ1PI6OrMA0GCSqGSIb3DQEBCwUAA4IBAQA8Uz45Q6q0NOPA
# PF5pQ19LuGh6n+KIC5nXXBb4nwcXNxEA4osZe4e2MP5FTdMamO0shApz8ywKtxNl
# GTDo03bEuddFwyVzeY2+SuMewWkQ0CLa5aAzH/SW1MfsAOOQH3BUWRjY12caS8Ft
# heBxgoA5ERkP6gSx72YSW9TxLpkNWj56zMayFytwmBd3gYppJQujLn/xV9lOKO7t
# 9MreSdzpdMycEvsxytitrDM3S7XP6OL+8iZ2uZEP4PfVS9C4NBJhMQcWaEMrPrR+
# LncTFsPQ+H5137mB48Ai43/vHTUY5wnoo4aqtypyZaMHQe+24/70heJgToexgDHV
# HATKe68E
# -----END CERTIFICATE-----
# -----BEGIN CERTIFICATE-----
# MIIFFjCCAv6gAwIBAgIRAJErCErPDBinU/bWLiWnX1owDQYJKoZIhvcNAQELBQAw
# TzELMAkGA1UEBhMCVVMxKTAnBgNVBAoTIEludGVybmV0IFNlY3VyaXR5IFJlc2Vh
# cmNoIEdyb3VwMRUwEwYDVQQDEwxJU1JHIFJvb3QgWDEwHhcNMjAwOTA0MDAwMDAw
# WhcNMjUwOTE1MTYwMDAwWjAyMQswCQYDVQQGEwJVUzEWMBQGA1UEChMNTGV0J3Mg
# RW5jcnlwdDELMAkGA1UEAxMCUjMwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEK
# AoIBAQC7AhUozPaglNMPEuyNVZLD+ILxmaZ6QoinXSaqtSu5xUyxr45r+XXIo9cP
# R5QUVTVXjJ6oojkZ9YI8QqlObvU7wy7bjcCwXPNZOOftz2nwWgsbvsCUJCWH+jdx
# sxPnHKzhm+/b5DtFUkWWqcFTzjTIUu61ru2P3mBw4qVUq7ZtDpelQDRrK9O8Zutm
# NHz6a4uPVymZ+DAXXbpyb/uBxa3Shlg9F8fnCbvxK/eG3MHacV3URuPMrSXBiLxg
# Z3Vms/EY96Jc5lP/Ooi2R6X/ExjqmAl3P51T+c8B5fWmcBcUr2Ok/5mzk53cU6cG
# /kiFHaFpriV1uxPMUgP17VGhi9sVAgMBAAGjggEIMIIBBDAOBgNVHQ8BAf8EBAMC
# AYYwHQYDVR0lBBYwFAYIKwYBBQUHAwIGCCsGAQUFBwMBMBIGA1UdEwEB/wQIMAYB
# Af8CAQAwHQYDVR0OBBYEFBQusxe3WFbLrlAJQOYfr52LFMLGMB8GA1UdIwQYMBaA
# FHm0WeZ7tuXkAXOACIjIGlj26ZtuMDIGCCsGAQUFBwEBBCYwJDAiBggrBgEFBQcw
# AoYWaHR0cDovL3gxLmkubGVuY3Iub3JnLzAnBgNVHR8EIDAeMBygGqAYhhZodHRw
# Oi8veDEuYy5sZW5jci5vcmcvMCIGA1UdIAQbMBkwCAYGZ4EMAQIBMA0GCysGAQQB
# gt8TAQEBMA0GCSqGSIb3DQEBCwUAA4ICAQCFyk5HPqP3hUSFvNVneLKYY611TR6W
# PTNlclQtgaDqw+34IL9fzLdwALduO/ZelN7kIJ+m74uyA+eitRY8kc607TkC53wl
# ikfmZW4/RvTZ8M6UK+5UzhK8jCdLuMGYL6KvzXGRSgi3yLgjewQtCPkIVz6D2QQz
# CkcheAmCJ8MqyJu5zlzyZMjAvnnAT45tRAxekrsu94sQ4egdRCnbWSDtY7kh+BIm
# lJNXoB1lBMEKIq4QDUOXoRgffuDghje1WrG9ML+Hbisq/yFOGwXD9RiX8F6sw6W4
# avAuvDszue5L3sz85K+EC4Y/wFVDNvZo4TYXao6Z0f+lQKc0t8DQYzk1OXVu8rp2
# yJMC6alLbBfODALZvYH7n7do1AZls4I9d1P4jnkDrQoxB3UqQ9hVl3LEKQ73xF1O
# yK5GhDDX8oVfGKF5u+decIsH4YaTw7mP3GFxJSqv3+0lUFJoi5Lc5da149p90Ids
# hCExroL1+7mryIkXPeFM5TgO9r0rvZaBFOvV2z0gp35Z0+L4WPlbuEjN/lxPFin+
# HlUjr8gRsI3qfJOQFy/9rKIJR0Y/8Omwt/8oTWgy1mdeHmmjk7j1nYsvC9JSQ6Zv
# MldlTTKB3zhThV1+XWYp6rjd5JW1zbVWEkLNxE7GJThEUG3szgBVGP7pSWTUTsqX
# nLRbwHOoq7hHwg==
# -----END CERTIFICATE-----
# -----BEGIN CERTIFICATE-----
# MIIFYDCCBEigAwIBAgIQQAF3ITfU6UK47naqPGQKtzANBgkqhkiG9w0BAQsFADA/
# MSQwIgYDVQQKExtEaWdpdGFsIFNpZ25hdHVyZSBUcnVzdCBDby4xFzAVBgNVBAMT
# DkRTVCBSb290IENBIFgzMB4XDTIxMDEyMDE5MTQwM1oXDTI0MDkzMDE4MTQwM1ow
# TzELMAkGA1UEBhMCVVMxKTAnBgNVBAoTIEludGVybmV0IFNlY3VyaXR5IFJlc2Vh
# cmNoIEdyb3VwMRUwEwYDVQQDEwxJU1JHIFJvb3QgWDEwggIiMA0GCSqGSIb3DQEB
# AQUAA4ICDwAwggIKAoICAQCt6CRz9BQ385ueK1coHIe+3LffOJCMbjzmV6B493XC
# ov71am72AE8o295ohmxEk7axY/0UEmu/H9LqMZshftEzPLpI9d1537O4/xLxIZpL
# wYqGcWlKZmZsj348cL+tKSIG8+TA5oCu4kuPt5l+lAOf00eXfJlII1PoOK5PCm+D
# LtFJV4yAdLbaL9A4jXsDcCEbdfIwPPqPrt3aY6vrFk/CjhFLfs8L6P+1dy70sntK
# 4EwSJQxwjQMpoOFTJOwT2e4ZvxCzSow/iaNhUd6shweU9GNx7C7ib1uYgeGJXDR5
# bHbvO5BieebbpJovJsXQEOEO3tkQjhb7t/eo98flAgeYjzYIlefiN5YNNnWe+w5y
# sR2bvAP5SQXYgd0FtCrWQemsAXaVCg/Y39W9Eh81LygXbNKYwagJZHduRze6zqxZ
# Xmidf3LWicUGQSk+WT7dJvUkyRGnWqNMQB9GoZm1pzpRboY7nn1ypxIFeFntPlF4
# FQsDj43QLwWyPntKHEtzBRL8xurgUBN8Q5N0s8p0544fAQjQMNRbcTa0B7rBMDBc
# SLeCO5imfWCKoqMpgsy6vYMEG6KDA0Gh1gXxG8K28Kh8hjtGqEgqiNx2mna/H2ql
# PRmP6zjzZN7IKw0KKP/32+IVQtQi0Cdd4Xn+GOdwiK1O5tmLOsbdJ1Fu/7xk9TND
# TwIDAQABo4IBRjCCAUIwDwYDVR0TAQH/BAUwAwEB/zAOBgNVHQ8BAf8EBAMCAQYw
# SwYIKwYBBQUHAQEEPzA9MDsGCCsGAQUFBzAChi9odHRwOi8vYXBwcy5pZGVudHJ1
# c3QuY29tL3Jvb3RzL2RzdHJvb3RjYXgzLnA3YzAfBgNVHSMEGDAWgBTEp7Gkeyxx
# +tvhS5B1/8QVYIWJEDBUBgNVHSAETTBLMAgGBmeBDAECATA/BgsrBgEEAYLfEwEB
# ATAwMC4GCCsGAQUFBwIBFiJodHRwOi8vY3BzLnJvb3QteDEubGV0c2VuY3J5cHQu
# b3JnMDwGA1UdHwQ1MDMwMaAvoC2GK2h0dHA6Ly9jcmwuaWRlbnRydXN0LmNvbS9E
# U1RST09UQ0FYM0NSTC5jcmwwHQYDVR0OBBYEFHm0WeZ7tuXkAXOACIjIGlj26Ztu
# MA0GCSqGSIb3DQEBCwUAA4IBAQAKcwBslm7/DlLQrt2M51oGrS+o44+/yQoDFVDC
# 5WxCu2+b9LRPwkSICHXM6webFGJueN7sJ7o5XPWioW5WlHAQU7G75K/QosMrAdSW
# 9MUgNTP52GE24HGNtLi1qoJFlcDyqSMo59ahy2cI2qBDLKobkx/J3vWraV0T9VuG
# WCLKTVXkcGdtwlfFRjlBz4pYg1htmf5X6DYO8A4jqv2Il9DjXA6USbW1FzXSLr9O
# he8Y4IWS6wY7bCkjCWDcRQJMEhg76fsO3txE+FiYruq9RUWhiF1myv4Q6W+CyBFC
# Dfvp7OOGAN6dEOM4+qR9sdjoSYKEBpsr6GtPAQw4dy753ec5
# -----END CERTIFICATE-----"""
#     key="""-----BEGIN PRIVATE KEY-----
# MIGHAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBG0wawIBAQQgqMw7LtVT+oz50fHF
# hjbQ8v2EBq4cvjtyOWDsnp/ouZChRANCAAS7JRuWQudlh//L7k4mL5sceM5ymXe0
# 2TXB/8hwCVFi655QrrJA3zTiXGPfQBzjD9w1on4TsbxU4F1OP4cw6Ebu
# -----END PRIVATE KEY-----"""
#     key="123"
    # cert_name='test.bosco.live'
    # if "already" in upload_cdnw(cert_name,cert,key).text : 
    #     print(123)
    # cert_id=check_cdnw_certid(cert_name)
    # print(cert_id)
    # print(set_cdnwdomain_cert(domain,cert_id))
    
    
    
    
   
