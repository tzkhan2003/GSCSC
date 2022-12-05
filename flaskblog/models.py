from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flaskblog import db, login_manager
from flask_login import UserMixin
import json

#    comnt = db.relationship('Comment', backref='author')
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class Member(db.Model, UserMixin):
    token = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    passwordorg = db.Column(db.String(60), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    birth_date = db.Column(db.DateTime, nullable=False)
    father_name = db.Column(db.String(20), nullable=False)
    father_ocu = db.Column(db.String(20), nullable=False)
    mother_name = db.Column(db.String(20), nullable=False)
    mother_ocu = db.Column(db.String(20), nullable=False)
    parents_no = db.Column(db.String(20), nullable=False)
    present_address = db.Column(db.String(20), nullable=False)
    permanent_address = db.Column(db.String(20), nullable=False)
    roll = db.Column(db.String(20),unique=True, nullable=False)
    year = db.Column(db.String(20), nullable=False)
    nid = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    facebook = db.Column(db.String(20), nullable=False)
    picture = db.Column(db.String(20), nullable=False, default='default.jpg')
    exp = db.Column(db.String(20), nullable=False)
    school = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(5), nullable=False, default='pending')
    memberid= db.Column(db.String(60))

    def __repr__(self):
        return f"Member('{self.id}', '{self.name}')"



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    birth_date = db.Column(db.DateTime, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    type = db.Column(db.String(5), nullable=False, default='user')
    status = db.Column(db.String(5), nullable=False, default='pending')

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"




class SellerId(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    birth_date = db.Column(db.DateTime, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    trade = db.Column(db.String(60), nullable=False)
    nid = db.Column(db.String(60), nullable=False)
    address = db.Column(db.String(60), nullable=False)
    phone = db.Column(db.String(60), nullable=False)
    shopname = db.Column(db.String(60), nullable=False)
    status = db.Column(db.String(5), nullable=False, default='pending')

    def __repr__(self):
        return f"Comment('{self.username}', '{self.email}', '{self.birth_date}', '{self.password}', '{self.address}', '{self.phone}', '{self.shopname}')"

class JsonEcodedDict(db.TypeDecorator):
    impl = db.Text
    def process_bind_param(self, value, dialect):
        if value is None:
            return '{}'
        else:
            return json.dumps(value)
    def process_result_value(self, value, dialect):
        if value is None:
            return {}
        else:
            return json.loads(value)

