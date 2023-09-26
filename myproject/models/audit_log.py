from myproject import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

class Audit(db.Model, UserMixin):
    __tablename__ = 'audit'
    
    # columns
    id       = db.Column(db.Integer, primary_key = True,)
    email    = db.Column(db.String(64), db.ForeignKey('users.email'))
    action = db.Column(db.Text,)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    def __init__(self, email, action):
        """初始化"""
        self.email = email
        self.action = action

    def add_log(self,):
        db.session.add(self)
        db.session.commit()
        