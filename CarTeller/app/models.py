# -*- coding: UTF-8 -*-

from app import db
from datetime import datetime

class User(db.Model):
    username = db.Column(db.String(255), primary_key=True)
    password = db.Column(db.String(255))
    key_token = db.Column(db.String(255), unique=True)
    count_access = db.Column(db.INT)

    def  __init__(self,username,password,key_token,count_access):
        self.username = username
        self.password = password
        self.key_token = key_token
        self.count_access = count_access

    def __repr__(self):
        return '<用户是 %r>' % self.username

    def serialize(self):
        return {
            "username": self.username,
            "password": self.password,
            "key_token": self.key_token,
            "count_access": self.count_access
        }


class Record(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(255))
    msg = db.Column(db.String(255))
    time = db.Column(db.DateTime,default=datetime.now())
    url = db.Column(db.String(255))

    def  __init__(self,username,msg,time,url):
        self.username = username
        self.msg = msg
        self.time = time
        self.url = url

    def __repr__(self):
        return '<用户%s在%s访问>' % self.username, self.time

    def serialize(self):
        return {
            "username": self.username,
            "msg": self.msg,
            "time":  self.time.strftime('%c'),
            "url":  self.url
        }
