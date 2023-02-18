import monitor_order
from flask import Flask, render_template, request
app = Flask(__name__)

# @app.route("/<name>",methods=['GET'])
# def hello(name):
#     return f"Hello,{name}"

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/form")
def form():
    return render_template('form.html')

@app.route("/ycadd")
def ycadd():
    return render_template('yc_add.html')

@app.route("/ycaddcompleted",methods=['POST'])
def ycadd_completed():
    domain=request.values['domain_list']
    request_port=request.values['request_port']
    origin_addr=request.values['origin_addr']
    origin_port=request.values['origin_port']
    type_=request.values['type']
    
    redirect=request.values['redirect'] or None

    
    print(domain,request_port,origin_addr,origin_port,type_,redirect)
    return render_template('yc_add_completed.html')


@app.route("/submit",methods=['POST'])
def submit():
    domain = request.values['test']
    temp_1=monitor_order.main(domain)
    temp_2=[(x.split('>')) for x in temp_1]
    result={ x:y for x,y in temp_2}
    print(result)
    return render_template('submit.html',**locals())
    

if __name__ == '__main__':
    app.run('0.0.0.0',debug=True)