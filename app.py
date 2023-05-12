import monitor_order
import re
import time
from flask import Flask, render_template, request
import threading
from queue import Queue
import yccdn_add_domain
import sc_white
import search_cnzzcode
import create_cnzz
import uploadSSL
import alidns_set
import yc_https_set
from datetime import datetime
import sync_config
import new_cnzz

app = Flask(__name__)
qlist=Queue()
lock = threading.Lock()

# @app.route("/<name>",methods=['GET'])
# def hello(name):
#     return f"Hello,{name}"
class MyThread(threading.Thread):
    def __init__(self,func,args=()):
        super(MyThread,self).__init__()
        self.func=func
        self.args=args
    def run(self):
        time.sleep(2)
        self.result = self.func(*self.args)
    def get_result(self):
        threading.Thread.join(self)
        try : 
            return self.result
        except Exception : 
            return None
        


@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/form")
def form():
    return render_template('form.html')



@app.route("/DeleteCdnw")
def delete_cdnw():
    return render_template('delete_cdnw.html')

@app.route("/DeleteCdnwCompleted",methods=['POST'])
def delete_cdnw_completed():
    input_domain=request.values['domain']
    domainlist=re.findall(r'[a-zA-Z.:0-9-]+',input_domain)

    t1=threading.Thread(target=sync_config.delete_domain,args=(domainlist,))
    t1.start()

    return render_template('delete_cdnw_completed.html',**locals())

@app.route("/DeleteCdnwLog")
def check_delete_cdnw_log():
    try :
        with open('delete_cdnw.log') as f :
            task=f.readlines()
        print(task)
    except FileNotFoundError : 
        task=['We currently do not have any log.']

    return render_template('check_delete_cdnw_log.html',**locals())

@app.route("/SyncCdnw")
def sync_cdnw_config():
    return render_template('sync_cdnw_config.html')

@app.route("/SyncCdnwCompleted",methods=['POST'])
def sync_cdnw_config_completed():
    input_domain=request.values['domain']
    try : input_refer=request.values['refer']
    except : 
        input_refer = None

    domainlist=re.findall(r'[a-zA-Z.:0-9-]+',input_domain)

    t1=threading.Thread(target=sync_config.main,args=(domainlist,input_refer))
    t1.start()

    return render_template('sync_cdnw_config_completed.html',**locals())

@app.route("/CheckSyncCdnwLog")
def check_sync_cdnw_log():
    try :
        with open('sync_cdnw.log') as f :
            task=f.readlines()
        print(task)
    except FileNotFoundError : 
        task=['We currently do not have any log.']

    return render_template('check_sync_cdnw_log.html',**locals())


@app.route("/ycopenhttps")
def yc_openhttps():
    return render_template('yc_openhttps.html')
    # return "功能暫未開放" , 404

@app.route("/ycopenhttpscompleted",methods=['POST'])
def yc_openhttps_completed():
    input_domain=request.values['domain_list']
    input_cusid=request.values['customer_ID']
    input_port=request.values['request_port']
    input_force=request.values['type']

    domainlist=re.findall(r'[a-zA-Z.:0-9-]+',input_domain)

    t1=threading.Thread(target=yc_https_set.change_set,args=(input_cusid,domainlist,input_port,input_force))
    t1.start()

    return render_template('yc_openhttps_completed.html',**locals())

@app.route("/checkychttps")
def check_yc_https():
    try :
        with open('ychttps.log') as f :
            task=f.readlines()
        print(task)
    except FileNotFoundError : 
        task=['We currently do not have any log.']

    return render_template('check_yc_httpslog.html',**locals())


@app.route("/ycadd")
def ycadd():
    return render_template('yc_add.html')
    # return "功能暫未開放" , 404

@app.route("/scwhite")
def scwhite():
    return render_template('scwhite.html')

@app.route("/cdnwuploadssl")
def cdnwuploadssl():
    return render_template('cdnw_uploadSSL.html')

@app.route("/searchcnzz")
def searchcnzz():
    return render_template('searchcnzz.html')

@app.route("/checkcnzz")
def checkcnzz():
    return render_template('checkcnzz.html')

@app.route("/checkCnzzCompleted",methods=['POST'])
def checkcnzz_completed():
    input_domain=request.values['test']
    dlist=re.findall(r'[0-9a-zA-Z:.-]+',input_domain)
    result=[]
    for domain in dlist : 
        result.append(str(new_cnzz.compare_cnzz(domain)))

    return render_template('checkcnzz_completed.html',**locals())


@app.route("/createcnzz")
def createcnzz():
    return render_template('createcnzz.html')

@app.route("/alidnsadddomain")
def alidns_add_domain():
    return render_template('alidns_add_domain.html')

@app.route("/alidnsadddomaincompleted",methods=['POST'])
def alidns_add_domain_completed():
    input_customer_name=request.values['c_name']
    input_domain=request.values['domain']
    dlist=re.findall(r'[0-9a-zA-Z:.-]+',input_domain)
    t1=threading.Thread(target=alidns_set.add_domain,args=(input_customer_name,dlist))
    t1.start()
    # result_list=alidns_set.add_domain(input_customer_name,dlist)
    
    return render_template('alidns_add_domain_completed.html',**locals())

@app.route("/checkcdnwssllog")
def check_cdnw_ssllog():
    try:
        with open('cdnw_uploadssl.log') as f :
            task=f.readlines()
        # print(task)
    except FileNotFoundError : 
        task=['We currently do not have any log.']

    return render_template('check_cdnw_ssllog.html',**locals())

@app.route("/cdnwuploadsslcompleted",methods=['POST'])
def cdnw_uploadssl_completed():
    input_domain=request.values['domain']
    
    t1=threading.Thread(target=uploadSSL.main,args=(input_domain,))
    t1.start()
    
    return render_template('cdnw_uploadSSL_completed.html')


@app.route("/createcnzzcompleted",methods=['POST'])
def creatd_cnzzcompleted():

    input_token=request.values['token']
    input_cookie=request.values['cookie']
    input_domain=request.values['domain']

    domainlist=create_cnzz.main(input_domain,input_cookie,input_token)

    print(domainlist)

    return render_template('creatd_cnzzcompleted.html',**locals())

@app.route("/searchcnzzcompleted",methods=['POST'])
def searchcnzz_completed():
    input_token=request.values['token']
    input_domain=request.values['domain']
    
    result=search_cnzzcode.main(input_token,input_domain)
    print(result)
    return render_template('searchcnzz_completed.html',**locals())


@app.route("/scwhitecompleted",methods=['POST'])
def scwhite_completed():
    input_dcodelist=request.values['domain_list']
    input_order=request.values['data_order']
    input_statistics=request.values['statistics']
    input_merchant=request.values['merchant']
    input_domain_merchant=request.values['domain_merchant']
    # print(input_dcodelist)
    # print(input_order)
    # print(input_statistics)
    # print(input_merchant)

    t1=threading.Thread(target=sc_white.main,args=(input_dcodelist,input_order,input_statistics,input_merchant,input_domain_merchant))
    t1.start()


    return render_template('scwhite_completed.html')


@app.route("/checkscwhite")
def checkscwhite():
    try:
        with open("scwhite.log") as f : 
            task=f.readlines()
        print(task)
    except FileNotFoundError : 
        task=['We currently do not have any log.']
    
    return render_template('checkscwhite.html',**locals())




@app.route("/ycaddcompleted",methods=['POST'])
def ycadd_completed():
    
    domain=request.values['domain_list']
    request_port=request.values['request_port']
    origin_addr=request.values['origin_addr']
    origin_port=request.values['origin_port']
    type_=request.values['type']
    redirect=request.values['redirect'] or None
    cusID=request.values['customer_ID']
    domainlist=re.findall(r'[a-zA-Z.:0-9-]+',domain)
    # domainlist=[ x for x in domain.split(',')]
    # print(domainlist)
    # with open("ycadd.log","r+") as f :
    #     old_content=f.read()
    #     f.seek(0)
    #     f.write(f"\n{datetime.now()}\n")
    #     f.write(old_content)
    
    t1=threading.Thread(target=yccdn_add_domain.add_domain,args=(cusID,domainlist,request_port,origin_addr,origin_port,type_,redirect))
    t1.start()
    
    
    # print(domainlist,request_port,origin_addr,origin_port,type_,redirect)
    return render_template('yc_add_completed.html',**locals())

@app.route("/checkyctask")
def checkyctask():
    try:
        with open("ycadd.log") as f : 
            task=f.readlines()
        print(task)
    except FileNotFoundError : 
        task=['We currently do not have any log.']
    
    return render_template('check_yc_task.html',**locals())

@app.route("/checkalidnsdomaintask")
def check_alidns_adddomainlog():
    with open("alidns_adddomain.log") as f : 
        task=f.readlines()
    print(task)
    
    return render_template('check_alidns_adddomainlog.html',**locals())


@app.route("/submit",methods=['POST'])
def submit():
    domain = request.values['test']
    
    try : banner = request.values['banner']
    except : banner = None

    statistics = request.values['statistics']
    merchant = request.values['merchant']
    # print(threading.active_count())
    t=threading.Thread(target=monitor_order.main,args=(domain,qlist,banner,statistics,merchant))
    
    # temp_1=monitor_order.main(domain)
    t.start()
    # lock.acquire()
    t.join()
    print("merchant:" + str(merchant))
    if str(merchant) == "0":
        check_banner_order=qlist.get()
        print("check: "+ str(check_banner_order))

    correct_count=qlist.get()
    temp_1 = qlist.get()
    print("correct_count:" + str(correct_count))
    print("temp:" + str(temp_1))
    temp_2=[(x.split('>')) for x in temp_1]
    result={ x:y for x,y in temp_2}
    # lock.release()
    
    print(result)

    return render_template('submit.html',**locals())
    

if __name__ == '__main__':
    app.run('0.0.0.0',debug=True)