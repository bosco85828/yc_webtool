from myproject.scripts import monitor_order
import re
import os 
import time
from flask import Flask, render_template, request , send_file , jsonify ,redirect, url_for,make_response ,flash ,abort
from flask_login import login_user, logout_user, login_required, current_user
from myproject.models.user import User
from myproject.models.audit_log import Audit
from myproject.form import LoginForm, RegistrationForm , ChangeForm, CloudflareDNS , ShowCloudflareDNS,AliDNS
from myproject import app, db
import threading
from queue import Queue
from myproject.scripts import yccdn_add_domain
from myproject.scripts.list_domain import get_domains
from myproject.scripts import uploadSSL
from myproject.scripts import alidns_set
from myproject.scripts import yc_https_set
from datetime import datetime
from myproject.scripts import sync_config
from myproject.scripts.alidns_set import main as ali_main
from myproject.scripts.cloudflare_dns import main as cf_main
from myproject.scripts.cloudflare_dns import search_record
from myproject.scripts.tclive import main
from myproject.scripts.sc_white import main
import json
from sqlalchemy import desc
from flask_paginate import Pagination
from wtforms import ValidationError


qlist=Queue()
lock = threading.Lock()
path=os.getcwd()


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
        

    
@app.errorhandler(401)
def unauthorized(error):
    return redirect(url_for('/login'),code="302")


@app.route("/")
def home():
    return render_template('index.html')

@app.route("/form")
@login_required
def form():
    return render_template('form.html')

@app.route("/yc_domains")
@login_required
def yc_domains():
    return render_template('yc_domains.html',**locals())

@app.route("/yc_domains_completed",methods=['POST'])
@login_required
def yc_domains_completed():
    customer_ID=request.values['customer_ID']
    file_name=request.values['file_name']
    t1=threading.Thread(target=get_domains,args=(customer_ID,file_name))
    t1.start()
    audit=Audit(
        email=current_user.email,
        action=json.dumps({
            'action':'List YCCDN  merchant domains.',
            'customer_ID':customer_ID,
            'file_name':file_name
        })
    )
    audit.add_log()
    
    return render_template('yc_domains_completed.html',**locals())

@app.route("/yc_domains_list")
@login_required
def yc_domains_list():
    files=os.listdir(f"{path}/myproject/scripts/domain_info")
    return render_template('file_list.html',**locals())

@app.route("/download/<filename>")
@login_required
def download_file(filename):
    file_path=f"{path}/myproject/scripts/domain_info/{filename}"
    return send_file(file_path, as_attachment=True)

@app.route("/scwhite_completed",methods=['POST'])
@login_required
def scwhite_completed():
    merchant=request.values['merchant']
    domain_merchant=request.values['domain_merchant']
    statistics=request.values['statistics']
    domain_list=request.values['domain_list']
    data_order=request.values['data_order']
    if not data_order : 
        data_order="5324617"

    t1=threading.Thread(target=main,args=(domain_list,data_order,statistics,merchant,domain_merchant))
    t1.start()

    flash("請求已送出，請查看 log 或者檢查目標網站是否設定成功。",category='success')
    return redirect(url_for('scwhite'))




@app.route("/scwite")
@login_required
def scwhite():
    return render_template('scwhite.html',**locals())


@app.route("/DeleteCdnw")
@login_required
def delete_cdnw():
    return render_template('delete_cdnw.html')

@app.route("/DeleteCdnwCompleted",methods=['POST'])
@login_required
def delete_cdnw_completed():
    input_domain=request.values['domain']
    domainlist=re.findall(r'[a-zA-Z.:0-9-]+',input_domain)

    t1=threading.Thread(target=sync_config.delete_domain,args=(domainlist,))
    t1.start()

    audit=Audit(
        email=current_user.email,
        action=json.dumps({
            'action':'Delete domains on CDNW.',
            'domains':domainlist
        })
    )
    audit.add_log()

    return render_template('delete_cdnw_completed.html',**locals())

@app.route("/DeleteCdnwLog")
@login_required
def check_delete_cdnw_log():
    try :
        with open('delete_cdnw.log') as f :
            task=f.readlines()
        print(task)
    except FileNotFoundError : 
        task=['We currently do not have any log.']

    return render_template('check_delete_cdnw_log.html',**locals())

@app.route("/SyncCdnw")
@login_required
def sync_cdnw_config():
    return render_template('sync_cdnw_config.html')

@app.route("/SyncCdnwCompleted",methods=['POST'])
@login_required
def sync_cdnw_config_completed():
    input_domain=request.values['domain']
    try : input_refer=request.values['refer']
    except : 
        input_refer = None

    domainlist=re.findall(r'[a-zA-Z.:0-9-]+',input_domain)

    t1=threading.Thread(target=sync_config.main,args=(domainlist,input_refer))
    t1.start()

    audit=Audit(
        email=current_user.email,
        action=json.dumps({
            'action':'Sync YCCDN domain to CDNW.',
            'domains':input_domain,
            'refer_domain':input_refer
        })
    )
    audit.add_log()

    return render_template('sync_cdnw_config_completed.html',**locals())

@app.route("/CheckSyncCdnwLog")
@login_required
def check_sync_cdnw_log():
    try :
        with open('sync_cdnw.log') as f :
            task=f.readlines()
        print(task)
    except FileNotFoundError : 
        task=['We currently do not have any log.']

    return render_template('check_sync_cdnw_log.html',**locals())


@app.route("/ycopenhttps")
@login_required
def yc_openhttps():
    return render_template('yc_openhttps.html')
    # return "功能暫未開放" , 404

@app.route("/ycopenhttpscompleted",methods=['POST'])
@login_required
def yc_openhttps_completed():
    input_domain=request.values['domain_list']
    input_cusid=request.values['customer_ID']
    input_port=request.values['request_port']
    input_force=request.values['type']

    domainlist=re.findall(r'[a-zA-Z.:0-9-]+',input_domain)

    t1=threading.Thread(target=yc_https_set.change_set,args=(input_cusid,domainlist,input_port,input_force))
    t1.start()

    audit=Audit(
        email=current_user.email,
        action=json.dumps({
            'action':'YCCDN open https.',
            'domains':input_domain,
            'customer_id':input_cusid,
            'https_port':input_port,
            'force_https':input_force,
        })
    )
    audit.add_log()

    return render_template('yc_openhttps_completed.html',**locals())

@app.route("/checkychttps")
@login_required
def check_yc_https():
    try :
        with open('ychttps.log') as f :
            task=f.readlines()
        print(task)
    except FileNotFoundError : 
        task=['We currently do not have any log.']

    return render_template('check_yc_httpslog.html',**locals())


@app.route("/ycadd")
@login_required
def ycadd():
    return render_template('yc_add.html')
    # return "功能暫未開放" , 404


@app.route("/cdnwuploadssl")
@login_required
def cdnwuploadssl():
    return render_template('cdnw_uploadSSL.html')


# @app.route("/alidnsadddomain")
# @login_required
# def alidns_add_domain():
#     return render_template('alidns_add_domain.html')

# @app.route("/alidnsadddomaincompleted",methods=['POST'])
# @login_required
# def alidns_add_domain_completed():
#     input_customer_name=request.values['c_name']
#     input_domain=request.values['domain']
#     dlist=re.findall(r'[0-9a-zA-Z:.-]+',input_domain)
#     t1=threading.Thread(target=alidns_set.add_domain,args=(input_customer_name,dlist))
#     t1.start()
#     # result_list=alidns_set.add_domain(input_customer_name,dlist)
    
#     return render_template('alidns_add_domain_completed.html',**locals())

@app.route("/checkcdnwssllog")
@login_required
def check_cdnw_ssllog():
    try:
        with open('cdnw_uploadssl.log') as f :
            task=f.readlines()
        # print(task)
    except FileNotFoundError : 
        task=['We currently do not have any log.']

    return render_template('check_cdnw_ssllog.html',**locals())

@app.route("/cdnwuploadsslcompleted",methods=['POST'])
@login_required
def cdnw_uploadssl_completed():
    input_domain=request.values['domain']
    
    t1=threading.Thread(target=uploadSSL.main,args=(input_domain,))
    t1.start()
    
    audit=Audit(
        email=current_user.email,
        action=json.dumps({
            'action':'upload CDNW SSL',
            'domains':input_domain
        })
    )
    audit.add_log()

    return render_template('cdnw_uploadSSL_completed.html')


@app.route("/ycaddcompleted",methods=['POST'])
@login_required
def ycadd_completed():
    
    domain=request.values['domain_list']
    request_port=request.values['request_port']
    origin_addr=request.values['origin_addr']
    origin_port=request.values['origin_port']
    type_=request.values['type']
    redirect=request.values['redirect'] or None
    cusID=request.values['customer_ID']
    domainlist=re.findall(r'[a-zA-Z.:0-9-]+',domain)

    t1=threading.Thread(target=yccdn_add_domain.add_domain,args=(cusID,domainlist,request_port,origin_addr,origin_port,type_,redirect))
    t1.start()
    audit=Audit(
        email=current_user.email,
        action=json.dumps({
            'action':'add YCCDN domains.',
            'domains':domainlist,
            'request_port':request_port,
            'origin_addr':origin_addr,
            'origin_port':origin_port,
            'type':type_,
            'redirect':redirect,
            'customer_id':cusID
        })
    )
    audit.add_log()
    
    return render_template('yc_add_completed.html',**locals())

@app.route("/checkyctask")
@login_required
def checkyctask():
    try:
        with open("ycadd.log") as f : 
            task=f.readlines()
        print(task)
    except FileNotFoundError : 
        task=['We currently do not have any log.']
    
    return render_template('check_yc_task.html',**locals())


@app.route("/checkscwhite")
@login_required
def checksctask():
    try:
        with open("scwhite.log") as f : 
            task=f.readlines()
        print(task)
    except FileNotFoundError : 
        task=['We currently do not have any log.']
    
    return render_template('checkscwhite.html',**locals())

@app.route("/checkalidnsdomaintask")
@login_required
def check_alidns_adddomainlog():
    with open("alidns_adddomain.log") as f : 
        task=f.readlines()
    print(task)
    
    return render_template('check_alidns_adddomainlog.html',**locals())


# @app.route("/submit",methods=['POST'])
# @login_required
# def submit():
#     domain = request.values['test']
    
#     try : banner = request.values['banner']
#     except : banner = None

#     statistics = request.values['statistics']
#     merchant = request.values['merchant']
#     # print(threading.active_count())
#     t=threading.Thread(target=monitor_order.main,args=(domain,qlist,banner,statistics,merchant))
    
#     # temp_1=monitor_order.main(domain)
#     t.start()
#     # lock.acquire()
#     t.join()
#     print("merchant:" + str(merchant))
#     if str(merchant) == "0":
#         check_banner_order=qlist.get()
#         print("check: "+ str(check_banner_order))

#     correct_count=qlist.get()
#     temp_1 = qlist.get()
#     print("correct_count:" + str(correct_count))
#     print("temp:" + str(temp_1))
#     temp_2=[(x.split('>')) for x in temp_1]
#     result={ x:y for x,y in temp_2}
#     # lock.release()
    
#     print(result)

#     return render_template('submit.html',**locals())
 


@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()
        
        if user and  form.email.data == user.email and  user.check_password(form.password.data):
            login_user(user)
            print('登入成功')
            flash("您已經成功的登入系統",category='success')
            next = request.args.get('next')
            if next == None or not next[0]=='/':
                next = url_for('home')
            print(current_user.email)
            audit=Audit(
                email=current_user.email,
                action=json.dumps({
                    'action':"Login success."
                })
            )
            audit.add_log()

            return redirect(next)
        else : 
            flash("Login failed.",category='warning')        
            return render_template('login.html',form=form)
    
    return render_template('login.html',form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("您已經登出系統")
    return redirect(url_for('home'))

@app.route('/cfdns',methods=['GET','POST'])
@login_required
def cloudflare_dns():
    form=CloudflareDNS()
    if form.validate_on_submit():
        action=form.action.data
        
        if action == 'delete' : len_limit=2
        elif action == 'add' : len_limit=3       
        elif action == "modify" : len_limit=4
            
        try : infos=[ tuple(x.split()) for x in form.infos.data.split('\n') if x and len(x.split()) == len_limit  ]
        except : 
            flash('輸入格式有誤，麻煩確認後重新輸入!',category='warning')
            return redirect(url_for('home'))
        
        if not infos : 
            flash('輸入格式有誤，麻煩確認後重新輸入!',category='warning')
            return redirect(url_for('home'))

        t1=threading.Thread(target=cf_main,args=(action,infos))
        t1.start()        

        flash('送出成功!',category='success')
        audit=Audit(
            email=current_user.email,
            action=json.dumps({
                    'action':f'{action} for cloudflare DNS.',
                    'data':infos
                })
        )
        audit.add_log()
        return redirect(url_for('home'))
    
    return render_template('cf_dns.html',form=form)


@app.route('/cfdns_search',methods=['GET','POST'])
@login_required
def show_cloudflare_dns():
    form=ShowCloudflareDNS()
    if form.validate_on_submit():
        domain=form.domain.data
        try : results = search_record(domain)
        except IndexError : 
            flash('查無此域名，麻煩確認後重新輸入!',category='warning')
            return render_template('show_cloudflare_dns.html',form=form)
        return render_template('show_cloudflare_dns_completed.html',data=results)



    return render_template('show_cloudflare_dns.html',form=form)



@app.route('/alidns',methods=['GET','POST'])
@login_required
def ali_dns():
    form=AliDNS()
    if form.validate_on_submit():
        action=form.action.data
        c_name=form.c_name.data
        if action == 'delete' : len_limit=2
        elif action == 'add_record' : len_limit=3       
        elif action == "modify" : len_limit=4
        elif action == "get_record" : len_limit=1
        elif action == "add_domain" : len_limit=1
        elif action == "switch" : len_limit = 3
            
        try : infos=[ tuple(x.split()) for x in form.infos.data.split('\n') if x and len(x.split()) == len_limit  ]
        except : 
            flash('輸入格式有誤，麻煩確認後重新輸入!',category='warning')
            return redirect(url_for('home'))
        
        if not infos : 
            flash('輸入格式有誤，麻煩確認後重新輸入!',category='warning')
            return redirect(url_for('home'))
        
        if action == "get_record" : 
            try : results=ali_main(action,c_name,infos)
            except Exception as err : 
                flash('查無域名，請確認域名是否存在。',category="warning")
                return redirect(url_for('ali_dns'))
            return render_template('ali_dns_show.html',data=results)
        else : 
            t1=threading.Thread(target=ali_main,args=(action,c_name,infos))
            t1.start()        

            flash('送出成功!',category='success')
            audit=Audit(
                email=current_user.email,
                action=json.dumps({
                        'action':f'{action} for Aliyun DNS.',
                        'data':infos
                    })
            )
            audit.add_log()
            return redirect(url_for('home'))
    
    return render_template('ali_dns.html',form=form)


@app.route('/set_password',methods=['GET','POST'])
@login_required
def set_password():
    form=ChangeForm()
    if form.validate_on_submit():
        current_user.change_password(form.password.data)
        flash('修改密碼成功!',category='success')
        return redirect(url_for('login'))
    return render_template('set_password.html',form=form)


@app.route('/register_bill',methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        try : 
            form.check_email(form.email.data)

        except ValidationError : 

            flash("email 已被使用過",category="success")
            return render_template('register.html',form=form)
        user = User(email=form.email.data,password=form.password.data)
        # add to db table
        db.session.add(user)
        db.session.commit()

        flash("感謝註冊本系統成為會員",category='success')
        audit=Audit(
            email=user.email,
            action=json.dumps({
                'action':"Created account."
            })
        )
        audit.add_log()

        return redirect(url_for('login'))
    return render_template('register.html',form=form)

@app.route('/welcome')
@login_required
def welcome_user():
    return render_template('welcome_user.html')


@app.route('/audit_log')
@login_required
def audit_log(limit=15):
    page = request.args.get('page', type=int, default=1)
    print(page)
    data=db.session.query(Audit).all()
    start=(page-1)*limit
    end =  page * limit if len(data) > page * limit  else len(data)
    print(start,end)
    paginate = Pagination(page=page,per_page=limit, total=len(data))
    print(paginate.links)

    ret = db.session.query(Audit).order_by(desc(Audit.created_at)).slice(start, end)
    return render_template('audit_log.html', data=ret, paginate=paginate)

@app.route('/tclive',methods=['GET'])
@login_required
def tclive_list():
    domains=main('get')
    return render_template('tclive.html', domains=domains)


@app.route('/tclive',methods=['POST'])
@login_required
def tclive_post():
    domain=request.values['domain']
    _type=request.values['type']
    
    result=main(_type,domain)
    return redirect('/tclive')
    # return render_template('tclive.html', domains=domains)



if __name__ == '__main__':
    app.run("0.0.0.0",debug=True)