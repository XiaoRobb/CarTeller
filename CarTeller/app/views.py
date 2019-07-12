# -*- coding: UTF-8 -*-
# 200 == Success
# -1  == Error
# -2  == No more data
#
import random

from flask import request, jsonify, render_template, redirect
from app import app,db
from app.models import User, Record
from car_teller import CarTeller
import json
import base64
import numpy as np
import cv2
import datetime
import re
from io import BytesIO
from PIL import Image
import gc
import argparse
import torch
from torchvision import transforms
import scipy.io as mat_io
SOURCE_URL = 'http://localhost:63342/html5'
import json
import os

#验证session的字典
session_dict = {}
#
#简单的随机生成session码的函数
def create_session(username):
    try:
        #生成随机数赋值给字典中user的值
        session = random.randint(0, 1000)
        session_dict[username] = session
        return True
    except:
        return False


@app.route('/')
def index():
    user = User.query.filter_by().first()
    if user != None:
        return "数据库有数据"
    return "没连接上数据库呢"


@app.route('/login', methods=['POST', 'GET'])
def login():
    try:
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
        else:
            username = request.args.get('username')
            password = request.args.get('password')

        user = User.query.filter_by(username=username).first()
        #没有该用户的时候
        if user == None:
            return formattingData1(username=-1,msg='Not exist such account!')

        if user.password == password:
            #登陆成功的时候返回session验证
            create_session(username)#创建session码
            return formattingData(username=username, msg='Login success.', session=session_dict[username])
        else:
            return formattingData1(username=-1,msg='Incorrect password.')


    except KeyError as e:
        return formattingData1(username=-1,msg='Sorry,login failed.')



@app.route('/register', methods=['POST', 'GET'])
def registered():
    try:
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
        else:
            username = request.args.get('username')
            password = request.args.get('password')

        if username == None or password == None:
            return formattingData1(username=-1,msg='please insert both username and password')
        #检查数据库是否存在相同的
        user = User.query.filter_by(username=username).first()
        print(user)
        if user != None:
            return formattingData1(username=-1,msg='Sorry,this username already been registered!')

        key_token=username+"_access"
        count_access = 0
        user = User(username=username,password=password,key_token=key_token,count_access=count_access)
        db.session.add(user)
        db.session.commit()

        return formattingData1(username=username,msg='Register success!')

    except KeyError as e:
        return formattingData1(username=-1,msg='Sorry,register failed.')


@app.route('/record')
def get_record():
    try:
        #首先验证是否有username参数
        username = request.args.get('username')
        session = request.args.get('session')

        if username == None:
            return formattingData1(username=-1, msg='未输入用户名')
        elif session == None:
            return formattingData1(username=-1, msg='未登录')
        #此处保留有关页码的问题，暂时不做处理
        print("用户名"+username+"session"+session)
        print('键的数量'+str(len(session_dict)))
        if username not in session_dict.keys():
            print("session数据消失")
        print("sessname"+str(session_dict[username]))
        #现在进行验证session
        if username not in session_dict.keys():
            return formattingData1(username=-1, msg='未登录')
         
        if session_dict[username] != int(session):
            return formattingData1(username=-1, msg='被挤下线啦')


        record = Record.query.filter_by(username=username).all()
        my_record = []
        for item in record:
            r = Record(item.username, item.msg, item.time,item.url)
            my_record.append(r)
        str_json = json.dumps(my_record, default=Record.serialize, ensure_ascii=False)
        str_json = "{\"code\":0,\"msg\":\"\",\"count\":" + str(len(my_record)) + ",\"data\":" + str_json + "}"
        return str_json
    except KeyError as e:
        return formattingData1(username=-1, msg='Sorry,get record failed.')


@app.route('/isLogin', methods=['POST', 'GET'])
def is_login():
    try:
        if request.method == 'POST':
            username = request.form.get('username')
            session = request.form.get('session')
        else:
            username = request.args.get('username')
            session = request.args.get('session')
        # 现在进行验证session
        if username not in session_dict.keys():
            return formattingData1(username=-1, msg='未登录')
        if session_dict[username] != int(session):
            return formattingData1(username=-1, msg='已被挤下线')
        #session验证成功的话
        return formattingData1(username=username, msg='已登录')

    except:
        return formattingData1(username=-1, msg='处理错误')


@app.route('/getInfo', methods=['POST', 'GET'])
def get_info():
    try:
        if request.method == 'POST':
            username = request.form.get('username')
            session = request.form.get('session')
        # 现在进行验证session
        if username not in session_dict.keys():
            return formattingData1(username=-1, msg='未登录')
        if session_dict[username] != int(session):
            return formattingData1(username=-1, msg='已被挤下线')
        # session验证成功的话获取用户信息
        user = User.query.filter_by(username=username).first()
        return jsonify(
            {
                "username": username,
                "msg": "成功",
                "password": user.password,
                "email": user.password,
                "key_token": user.key_token
            }
        )
    except:
        return formattingData1(username=1, msg='获取数据失败')


@app.route('/carboard', methods=['POST', 'GET'])
def getCarNum():
    try:
        if request.method == 'POST':
            username = request.form.get('username')
            image = request.form.get('image')
        else:
            username = request.args.get('username')
            image = request.args.get('image')

        image = image.split(',')[1]
        image = base64_cv2(image)
        car_boards,_,_ = CarTeller.car_board_tell(image)
        string = ''
        for str1 in car_boards:
            string += str1
        #del car_boards
        gc.collect()
        return formattingData1(username=username, msg=string)
    except KeyError as e:
        return formattingData1(username=-1, msg='Sorry,get num failed.')


@app.route('/cartypemore', methods=['POST', 'GET'])
def getCarTypeMore():
    try:
        if request.method == 'POST':
            username = request.form.get('username')
            image = request.form.get('image')
        else:
            username = request.args.get('username')
            image = request.args.get('image')



        image = image.split(',')[1]
        print(image)
        image = base64_cv2(image)
        detections_img, type_dict=CarTeller.car_type_more_tell(image)
        string_base=image_to_base64(detections_img)
        print(string_base)
        string = json.dumps(type_dict)
        del detections_img
        del type_dict
        gc.collect()
        return formattingData2(username=username, msg=string,img=string_base)
    except KeyError as e:
        return formattingData2(username=-1, msg='Sorry,get num failed.',img="null")


@app.route('/carattribute', methods=['POST', 'GET'])
def getCarAttr():
    try:
        if request.method == 'POST':
            username = request.form.get('username')
            image = request.form.get('image')
        else:
            username = request.args.get('username')
            image = request.args.get('image')

        image = image.split(',')[1]
        string=CarTeller.car_attribute_tell(image)
        return formattingData1(username=username, msg=string)
    except KeyError as e:
        return formattingData1(username=-1, msg='Sorry,get num failed.')


@app.route('/carinfo', methods=['POST', 'GET'])
def getCarInfo():
    try:
        if request.method == 'POST':
            username = request.form.get('username')
            image = request.form.get('image')
        else:
            username = request.args.get('username')
            image = request.args.get('image')


        image = image.split(',')[1]
        if username == None:
            return formattingData1(username=-1, msg='Sorry,get type failed.')
        image = base64_cv2(image)
        car_info_li,pros_li = CarTeller.car_info_tell(image)
        carname = ["carone", "cartwo", "carthree", "carfour", "carfive"]
        mydict1 = []
        for name, pro in zip(car_info_li, pros_li):
            mydict2 = {}
            mydict2["carname"] = name
            mydict2["pro"] = pro
            mydict1.append(mydict2)
        dictstr=dict(zip(carname,mydict1))
        jsonstring=json.dumps(dictstr)
        string = jsonstring
        del car_info_li
        del pros_li
        gc.collect()
        return formattingData1(username=username, msg=string)
    except KeyError as e:
        return formattingData1(username=-1, msg='Sorry,get num failed.')


@app.route('/driverBehavior', methods=['POST', 'GET'])
def getDriverBehavior():
    try:
        if request.method == 'POST':
            username = request.form.get('username')
            image = request.form.get('image')
        else:
            username = request.args.get('username')
            image = request.args.get('image')


        image = image.split(',')[1]
        image = base64_cv2(image)
        behavior ,pros = CarTeller.behavior_tell(image)
        string =behavior+':'+str(pros)
        del behavior
        del pros
        gc.collect()
        return formattingData1(username=username, msg=string)
    except KeyError as e:
        return formattingData1(username=-1, msg='Sorry,get num failed.')


#下方为api接口
@app.route('/api/carboard', methods=['POST', 'GET'])
def getCarNumApi():
    try:
        if request.method == 'POST':
            username = request.form.get('username')
            image = request.form.get('image')
            key_token=request.form.get('key_token')
        else:
            username = request.args.get('username')
            image = request.args.get('image')
            key_token=request.form.get('key_token')

        if username == None:
            return formattingData1(username=-1, msg='未登录')
        # 此处保留有关页码的问题，暂时不做处理
        if key_token == None:
            return formattingData1(username=-1,msg='key_token值错误')
        user = User.query.filter_by(username=username).first()
        if(int(user.count_access) > int(500)):
            return formattingData1(username=-1,msg='此用户接口使用次数已达上限')
        if(user.key_token != key_token):
            return formattingData1(username=-1,msg='用户名和key_token值不符合')
        user.count_access+=1
        db.session.commit()#调用接口次数加一

        imagetemp=image
        image = base64_cv2(image)
        car_boards,_,_ = CarTeller.car_board_tell(image)
        string = ''
        for str1 in car_boards:
            string += str1
        del car_boards
        gc.collect()
        time1=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        url1="jpg/"+username+time1+".jpg"
        url1 = url1.replace(" ","1")
        record = Record(username=username, msg="车牌识别一次:" + string, time=time1,url=url1)
        db.session.add(record)
        db.session.commit()
        imgdata(imagetemp,username,time1)
        return formattingData1(username=username, msg=string)
    except KeyError as e:
        return formattingData1(username=-1, msg='Sorry,get num failed.')


@app.route('/api/cartypemore', methods=['POST', 'GET'])
def getCarTypeMoreApi():
    try:
        if request.method == 'POST':
            username = request.form.get('username')
            image = request.form.get('image')
            key_token=request.form.get('key_token')
        else:
            username = request.args.get('username')
            image = request.args.get('image')
            key_token=request.form.get('key_token')

        if username == None:
            return formattingData1(username=-1, msg='未登录')
        if key_token == None:
            return formattingData1(username=-1,msg='key_token值错误')
        user = User.query.filter_by(username=username).first()
        if(user.count_access > 500):
            return formattingData1(username=-1,msg='此用户接口使用次数已达上限')
        if(user.key_token != key_token):
            return formattingData1(username=-1,msg='用户名和key_token值不符合')
        user.count_access+=1
        db.session.commit()#调用接口次数加一


        imagetemp=image
        image = base64_cv2(image)
        detections_img, type_dict=CarTeller.car_type_more_tell(image)
        string_base = image_to_base64(detections_img)
        string = json.dumps(type_dict)
        del detections_img
        del type_dict
        gc.collect()
        time1=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        url1="jpg/"+username+time1+".jpg"
        url1=url1.replace(" ", "1")
        record = Record(username=username, msg="车辆检测一次:" + string, time=time1,url=url1)
        db.session.add(record)
        db.session.commit()
        imgdata(imagetemp,username,time1)
        print(formattingData2(username=username, msg=string,img=string_base))
        return formattingData2(username=username, msg=string,img=string_base)
    except KeyError as e:
        return formattingData1(username=-1, msg='Sorry,get num failed.')


@app.route('/api/carattribute', methods=['POST', 'GET'])
def getCarAttrApi():
    try:
        if request.method == 'POST':
            username = request.form.get('username')
            image = request.form.get('image')
            key_token=request.form.get('key_token')
        else:
            username = request.args.get('username')
            image = request.args.get('image')
            key_token=request.form.get('key_token')

        if username == None:
            return formattingData1(username=-1, msg='未登录')
        # 此处保留有关页码的问题，暂时不做处理
        if key_token == None:
            return formattingData1(username=-1,msg='key_token值错误')
        user = User.query.filter_by(username=username).first()
        if(user.count_access > 500):
            return formattingData1(username=-1,msg='此用户接口使用次数已达上限')
        if(user.key_token != key_token):
            return formattingData1(username=-1,msg='用户名和key_token值不符合')
        user.count_access+=1
        db.session.commit()#调用接口次数加一

        string=CarTeller.car_attribute_tell(image)
        time1=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        url1="jpg/"+username+time1+".jpg"
        url1=url1.replace(" ","1")
        record = Record(username=username, msg="属性检测一次:" + string, time=time1,url=url1)
        db.session.add(record)
        db.session.commit()
        imgdata(image,username,time1)
        return formattingData1(username=username, msg=string)
    except KeyError as e:
        return formattingData1(username=-1, msg='Sorry,get num failed.')


@app.route('/api/carinfo', methods=['POST', 'GET'])
def getCarInfoApi():
    try:
        if request.method == 'POST':
            username = request.form.get('username')
            image = request.form.get('image')
            key_token=request.form.get('key_token')
        else:
            username = request.args.get('username')
            image = request.args.get('image')
            key_token=request.form.get('key_token')

        if username == None:
            return formattingData1(username=-1, msg='未登录')
        # 此处保留有关页码的问题，暂时不做处理
        if key_token == None:
            return formattingData1(username=-1,msg='key_token值错误')
        user = User.query.filter_by(username=username).first()
        if(user.count_access > 500):
            return formattingData1(username=-1,msg='此用户接口使用次数已达上限')
        if(user.key_token != key_token):
            return formattingData1(username=-1,msg='用户名和key_token值不符合')
        user.count_access+=1
        db.session.commit()


        imagetemp=image
        image = base64_cv2(image)
        car_info_li,pros_li = CarTeller.car_info_tell(image)
        carname = ["carone", "cartwo", "carthree", "carfour", "carfive"]
        mydict1 = []
        for name, pro in zip(car_info_li, pros_li):
            mydict2 = {}
            mydict2["carname"] = name
            mydict2["pro"] = pro
            mydict1.append(mydict2)
        dictstr=dict(zip(carname,mydict1))
        jsonstring=json.dumps(dictstr)
        string = jsonstring
        del car_info_li
        del pros_li
        gc.collect()
        time1=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        url1="jpg/"+username+time1+".jpg"
        url1=url1.replace(" ","1")
        record = Record(username=username, msg="车辆检测一次:" + string, time=time1,url=url1)
        db.session.add(record)
        db.session.commit()
        imgdata(imagetemp,username,time1)
        return formattingData1(username=username, msg=string)
    except KeyError as e:
        return formattingData1(username=-1, msg='Sorry,get num failed.')


@app.route('/api/driverBehavior', methods=['POST', 'GET'])
def getDriverBehaviorApi():
    try:
        if request.method == 'POST':
            username = request.form.get('username')
            image = request.form.get('image')
            key_token=request.form.get('key_token')
        else:
            username = request.args.get('username')
            image = request.args.get('image')
            key_token=request.form.get('key_token')

        if username == None:
            return formattingData1(username=-1, msg='未登录')
        # 此处保留有关页码的问题，暂时不做处理
        if key_token == None:
            return formattingData1(username=-1,msg='key_token值错误')
        user = User.query.filter_by(username=username).first()
        if(user.count_access > 500):
            return formattingData1(username=-1,msg='此用户接口使用次数已达上限')
        if(user.key_token != key_token):
            return formattingData1(username=-1,msg='用户名和key_token值不符合')
        user.count_access+=1
        db.session.commit()#调用接口次数加一


        imagetemp = image
        image = base64_cv2(image)
        behavior, pros = CarTeller.behavior_tell(image)
        string = '{\"behavior\":'+behavior+',\"pros\":'+str(pros)+'}'
        del behavior
        del pros
        gc.collect()
        time1=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        url1="jpg/"+username+time1+".jpg"
        url1=url1.replace(" ","1")
        record = Record(username=username, msg="车辆检测一次:" + string, time=time1,url=url1)
        db.session.add(record)
        db.session.commit()
        imgdata(imagetemp,username,time1)#这里是否用imagetemp还是个疑问
        return formattingData1(username=username, msg=string)
    except KeyError as e:
        return formattingData1(username=-1, msg='Sorry,get num failed.')


def formattingData1(username,msg):
    return jsonify(
        {
            "username": username,
            "msg": msg,
        }
    )


def formattingData2(username,msg,img):
    return jsonify(
        {
            "username": username,
            "msg": msg,
            "img": img,
        }
    )

def formattingData(username,msg,session):
    return jsonify(
        {
            "username": username,
            "msg": msg,
            "session": session
        }
    )


def base64_cv2(base64_str):
    imgString = base64.b64decode(base64_str)
    nparr = np.fromstring(imgString,np.uint8)
    image = cv2.imdecode(nparr,cv2.COLOR_BAYER_BG2BGR)
    return image


def base64_to_image(base64_str, image_path=None):
    base64_data = re.sub('^data:image/.+;base64,', '', base64_str)
    byte_data = base64.b64decode(base64_data)
    image_data = BytesIO(byte_data)
    img = Image.open(image_data)
    if image_path:
        img.save(image_path)
    return img


def image_to_base64(image_np):
    image = cv2.imencode('.jpg', image_np)[1]
    image_code=str(base64.b64encode(image))[2:-1]
    return image_code


def imgdata(base6, username, time1):
    imgda=base64.b64decode(base6)
    name=username+str(time1)
    url="/var/www/html/jpg/"+name+".jpg"
    url=url.replace(" ", "1")
    file=open(url, 'wb')
    file.write(imgda)
    file.close()
    return url


