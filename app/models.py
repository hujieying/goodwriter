#encoding:utf-8
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, login_manager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    email = db.Column(db.String(100),nullable=False)
    password_hash = db.Column(db.String(100),nullable=False)
    openid = db.Column(db.String(50))
    wechatid = db.Column(db.String(50))
    confirmed = db.Column(db.Boolean, default=False)
    material = db.relationship('Material', backref='user', lazy='dynamic')
    article = db.relationship('Article', backref='user', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    #生成一个令牌，有效期默认为一小时
    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    #检验令牌，验证通过，设置confirmed属性为True
    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        return True

    def __repr__(self):
        return '<User %r>' % self.email

class Material(db.Model):
    __tablename__ = 'material'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    mater_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    content = db.Column(db.Text,nullable=False)
    user_id =  db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    tag = db.Column(db.String(20),nullable=False)
    edit_time = db.Column(db.DateTime,nullable=False,default=datetime.utcnow())


class Article(db.Model):
    __tablename__ = "article"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    artic_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(20),nullable=False)
    content = db.Column(db.Text,nullable=False)
    user_id =  db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    edit_time = db.Column(db.DateTime,nullable=False,default=datetime.utcnow())

#加载用户的回调函数
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
