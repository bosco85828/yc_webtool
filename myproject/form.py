from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField , SelectField,TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, email_validator
from wtforms import ValidationError
from myproject.models.user import User

class LoginForm(FlaskForm):
    email = StringField('電子郵件', validators=[DataRequired(), Email()])
    password = PasswordField('密碼',validators=[DataRequired()])
    submit = SubmitField('登入系統')

class RegistrationForm(FlaskForm):
    email = StringField('電子郵件', validators=[DataRequired(), Email()])
    # username = StringField('使用者', validators=[DataRequired()])
    password = PasswordField('密碼', validators=[DataRequired()])
    #EqualTo('pass_confirm', message='密碼需要吻合')
    # pass_confirm = PasswordField('確認密碼', validators=[DataRequired()])
    submit = SubmitField('註冊')
    def check_email(self, input_email):
        """檢查Email"""
        if User.query.filter_by(email=input_email).first():
            raise ValidationError('電子郵件已經被註冊過了')
    # def check_username(self, field):
    #     """檢查username"""
    #     if User.query.filter_by(username=field.data).first():
    #         raise ValidationError('使用者名稱已經存在')

class ChangeForm(FlaskForm):
    password=PasswordField('密碼', validators=[DataRequired(),EqualTo('pass_confirm', message='密碼需要吻合')])
    pass_confirm = PasswordField('確認密碼', validators=[DataRequired()])
    submit = SubmitField('送出')

class CloudflareDNS(FlaskForm):
    # choices=[('add','Add record'),('modify','Modify record'),('delete','Delete record'),('create','Create zone')]
    choices=[('add','Add record'),('modify','Modify record'),('delete','Delete record')]
    action=SelectField('操作',choices=choices)
    infos=TextAreaField('填入所需資訊',render_kw={"class":"custom-textarea","placeholder": """
請按照以下格式輸入，多筆紀錄換行添加按照相同格式即可。
1. Add >> Domain DNS_type Value
2. Modify >> Domain Old_value DNS_type New_value
3. Delete >> Domain Value
4. Create Zone >> root_domain
Example for Add record:
bill.com CNAME www.google.com
1.bill.com CNAME www.google.com

""",
})
    submit = SubmitField('送出')