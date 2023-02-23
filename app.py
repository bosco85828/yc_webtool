import monitor_order
import time
from flask import Flask, render_template, request
import threading
from queue import Queue
import yccdn_add_domain
import sc_white
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

@app.route("/ycadd")
def ycadd():
    return render_template('yc_add.html')

@app.route("/scwhite")
def scwhite():
    return render_template('scwhite.html')

@app.route("/scwhitecompleted",methods=['POST'])
def scwhite_completed():
    input_dcodelist=request.values['domain_list']
    input_order=request.values['data_order']
    input_statistics=request.values['statistics']
    input_merchant=request.values['merchant']
    # print(input_dcodelist)
    # print(input_order)
    # print(input_statistics)
    # print(input_merchant)

    t1=threading.Thread(target=sc_white.main,args=(input_dcodelist,input_order,input_statistics,input_merchant))
    t1.start()


    return render_template('scwhite_completed.html')


@app.route("/ycaddcompleted",methods=['POST'])
def ycadd_completed():
    
    domain=request.values['domain_list']
    request_port=request.values['request_port']
    origin_addr=request.values['origin_addr']
    origin_port=request.values['origin_port']
    type_=request.values['type']
    redirect=request.values['redirect'] or None
    cusID=request.values['customer_ID']

    domainlist=[ x for x in domain.split(',')]


    t1=threading.Thread(target=yccdn_add_domain.add_domain,args=(cusID,domainlist,request_port,origin_addr,origin_port,type_,redirect))
    t1.start()
    
    # print(domainlist,request_port,origin_addr,origin_port,type_,redirect)
    return render_template('yc_add_completed.html')


@app.route("/submit",methods=['POST'])
def submit():
    domain = request.values['test']
    # print(threading.active_count())
    t=threading.Thread(target=monitor_order.main,args=(domain,qlist))
    
    # temp_1=monitor_order.main(domain)
    t.start()
    # lock.acquire()
    t.join()

    temp_1 = qlist.get()
    # print(temp_1)
    temp_2=[(x.split('>')) for x in temp_1]
    result={ x:y for x,y in temp_2}
    # lock.release()
    print(result)
    return render_template('submit.html',**locals())
    

if __name__ == '__main__':
    app.run('0.0.0.0',debug=True)