import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# flask_login
from flask_login import LoginManager
from dotenv import load_dotenv
from flask_bootstrap import Bootstrap
import os 
# from myproject.models.user import User
# from myproject.models.audit_log import Audit
load_dotenv()
DB_USER=os.getenv('DB_USER')
DB_SECRET=os.getenv('DB_SECRET')

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY']= 'acretkeyinthisproject'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_SECRET}@host.docker.internal:3306/bill_tool'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
with app.app_context():
    db = SQLAlchemy(app)
    Migrate(app,db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message="You must login to access this page."
login_manager.message_category='warning'