# encoding:utf-8

import json
import requests
import pymysql as pl
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import config
from decorators import login_require
from datetime import datetime
from sqlalchemy import or_
from flask_bootstrap import Bootstrap
import html2text
import hashlib

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)  # 为应用初始化 bootstrap


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    authority = db.Column(db.Integer, nullable=False)


class Wxuser(db.Model):
    __talename__ = 'wxuser'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    wx_openid = db.Column(db.String(50), nullable=False)
    wx_nickname = db.Column(db.String(50), nullable=False)


class Search(db.Model):
    __talename__ = 'search'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    search_time = db.Column(db.DateTime, default=datetime.now)
    wxuser_id = db.Column(db.Integer, db.ForeignKey('wxuser.id'))
    s_wxuser = db.relationship('Wxuser', backref=db.backref('searchs'))
    address = db.Column(db.String(50), nullable=False)
    longitude = db.Column(db.Float(10), autoincrement=False)
    latitude = db.Column(db.Float(10), autoincrement=False)
    city = db.Column(db.String(50), nullable=False)

    def to_json(self):
        ctime = self.search_time.strftime("%Y-%m-%d %H:%M:%S")
        return {
            'id': self.id,
            'wxuser_id': self.wxuser_id,
            'time': ctime,
            'address': self.address,
            'longitude': self.longitude,
            'latitude': self.latitude,
            'city': self.city
        }


class Navigation(db.Model):
    __talename__ = 'navigation'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.DateTime, default=datetime.now)
    wxuser_id = db.Column(db.Integer, db.ForeignKey('wxuser.id'))
    n_wxuser = db.relationship('Wxuser', backref=db.backref('navigations'))
    start_address = db.Column(db.String(50), nullable=False)
    start_longitude = db.Column(db.Float(10), autoincrement=False)
    start_latitude = db.Column(db.Float(10), autoincrement=False)
    end_address = db.Column(db.String(50), nullable=False)
    end_longitude = db.Column(db.Float(10), autoincrement=False)
    end_latitude = db.Column(db.Float(10), autoincrement=False)
    city = db.Column(db.String(50), nullable=False)

    def to_json(self):
        ctime = self.time.strftime("%Y-%m-%d %H:%M:%S")
        return {
            'id': self.id,
            'wxuser_id': self.wxuser_id,
            'time': ctime,
            'start_address': self.start_address,
            'end_address': self.end_address,
            'start_longitude': self.start_longitude,
            'start_latitude': self.start_latitude,
            'end_longitude': self.end_longitude,
            'end_latitude': self.end_latitude,
            'city': self.city

        }


db.create_all()



@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('user/login.html')
    else:
        email = request.form.get('email')
        print(email)
        password = request.form.get('password')
        print(password)
        user = User.query.filter(User.email == email, User.password == password).first()
        if user:
            session['user_id'] = user.id
            session['authority'] = user.authority
            # 如果想在31天内都不需要登录
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return u'手机号或者密码错误，请确认后再登录!'


@app.route('/regist/', methods=['GET', 'POST'])
def regist():
    if request.method == 'GET':
        return render_template('user/reg.html')
    else:
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password')
        password2 = request.form.get('password2')
        authority = 2
        # 判断手机是否被注册
        user = User.query.filter(User.email == email).first()
        if user:
            return u'该邮箱已被注册，请更换邮箱!'
        else:
            # password1是否等于password2
            if password1 != password2:
                return u'两次密码不相等，请核对后再填写!'
            else:
                user = User(email=email, username=username, password=password1, authority=authority)
                db.session.add(user)
                db.session.commit()
                # 跳转到登录界面
                return redirect(url_for('login'))

        return u'错误'


@app.route('/logout/')
@login_require
def logout():
    session.pop('user_id')
    session.pop('authority')
    return redirect(url_for('login'))


@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user': user}
    return {}


@app.route('/user/', methods=['GET', 'POST'])
@login_require
def user():
    user_id = session['authority']
    context = {
        'users': Wxuser.query.order_by(Wxuser.wx_openid.desc()).all()
    }
    return render_template('user.html', **context)


@app.route('/userdetail/<user_id>/')
@login_require
def userdetail(user_id):
    wxuser = Wxuser.query.filter(Wxuser.id == user_id).first()
    try:
        na = Navigation.query.filter(Navigation.n_wxuser == wxuser).all()
        m = len(na)
        context = {
            'navigations': na
        }
        return render_template('userdetail.html', nickname=wxuser.wx_nickname, num=m, **context)
    except:
        return render_template('user.html')


@app.route('/userdetail_s/<user_id>/')
@login_require
def userdetail_s(user_id):
    wxuser = Wxuser.query.filter(Wxuser.id == user_id).first()
    try:
        na = Search.query.filter(Search.s_wxuser == wxuser).all()
        m = len(na)
        context = {
            'navigations': na
        }
        return render_template('userdetail1.html', nickname=wxuser.wx_nickname, num=m, **context)
    except:
        return render_template('user.html')

@app.route('/', methods=['GET', 'POST'])
@login_require
def index():
    na = Navigation.query.order_by(Navigation.id.desc()).all()
    n_m = len(na)
    sa = Search.query.order_by(Search.id.desc()).all()
    s_m = len(sa)
    wa =Wxuser.query.order_by(Wxuser.id.desc()).all()
    w_m = len(wa)
    ua = User.query.order_by(User.id.desc()).all()
    u_m = len(ua)
    return render_template('index.html',nm=n_m,sm=s_m,wm=w_m,um=u_m)


@app.route('/authority_Management/', methods=['GET', 'POST'])
@login_require
def authority_Management():
    user_id = session['user_id']
    user = User.query.filter(User.id == user_id).first()

    if user.authority == 1:
        context = {
            'users': User.query.order_by(User.id.desc()).all()
        }
        return render_template('authority_Management.html', **context)
    else:
        return u'没有访问权限'


@app.route('/changeauthority/', methods=['POST'])
@login_require
def changeauthority():
    user_id = request.form.get('user_id')
    user = User.query.filter(User.id == user_id).first()
    if user.id == 1:
        return u'不能修改此用户的权限'
    else:

        if user.authority == 1:
            user.authority = 2
        else:
            user.authority = 1
        db.session.commit()
        return redirect(url_for('authority_Management'))


@app.route('/delauthority/', methods=['POST'])
@login_require
def delauthority():
    user_id = request.form.get('user_id')
    user = User.query.filter(User.id == user_id).first()
    if user.id == 1:
        return u'不能删除此用户'
    else:

        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('authority_Management'))


@app.route('/navigation/', methods=['GET', 'POST'])
@login_require
def navigation():
    context = {
        'navigations': Navigation.query.order_by(Navigation.time.desc()).all()
    }
    return render_template('navigation.html', **context)


@app.route('/wxuser_navigation_del/', methods=['POST'])
@login_require
def wxuser_navigation_del():
    navigation_id = request.form.get('navigation_id')
    try:
        navigation_wx = Navigation.query.filter(Navigation.id == navigation_id).first()
        db.session.delete(navigation_wx)
        db.session.commit()
        return redirect(url_for('navigation'))
    except:
        return {'result': u'删除失败'}


@app.route('/wxuser_search_del/')
@login_require
def wxuser_search_del():
    search_id = request.form.get('search_id')
    try:

        search_wx = Search.query.filter(Search.id == search_id).first()
        db.session.delete(search_wx)
        db.session.commit()
        return redirect(url_for('search'))
    except:
        return {'result': u'删除失败'}


@app.route('/search/', methods=['GET', 'POST'])
@login_require
def search():
    context = {
        'searchs': Search.query.order_by(Search.search_time.desc()).all()
    }
    return render_template('search.html', **context)


@app.route('/wxuser_add/<openid>/<nickname>/')
def wxuser_add(openid, nickname):
    wx_user = Wxuser.query.filter(Wxuser.wx_openid == openid).first()
    if wx_user:
        return {'result': u'用户已存在'}
    else:
        wx__user = Wxuser()
        wx__user.wx_openid = openid
        wx__user.wx_nickname = nickname
        db.session.add(wx__user)
        db.session.commit()
        return {'result': u'添加成功'}


@app.route(
    '/wxuser_navigation_add/<wxopenid>/<start_address>/<start_longitude>/<start_latitude>/<end_address>/<end_longitude>/<end_latitude>/<city>/')
def wxuser_navigation_add(wxopenid, start_address, start_longitude, start_latitude, end_address, end_longitude,
                          end_latitude, city):
    wxuser = Wxuser.query.filter(Wxuser.wx_openid == wxopenid).first()
    if wxuser:
        navigation_wx = Navigation()
        navigation_wx.n_wxuser = wxuser
        navigation_wx.start_address = start_address
        navigation_wx.start_longitude = start_longitude
        navigation_wx.start_latitude = start_latitude
        navigation_wx.end_address = end_address
        navigation_wx.end_longitude = end_longitude
        navigation_wx.end_latitude = end_latitude
        navigation_wx.city = city
        db.session.add(navigation_wx)
        db.session.commit()
        return {'result': u'上传成功'}
    else:
        return {'ressult': u'上传失败'}


@app.route('/wxuser_navigation_get/<wxopenid>/')
def wxuser_navigation_get(wxopenid):
    wxuser = Wxuser.query.filter(Wxuser.wx_openid == wxopenid).first()
    try:
        ns = Navigation.query.filter(Navigation.wxuser_id == wxuser.id).all()
        m = len(ns)
        for i in range(m):
            ns[i] = ns[i].to_json()
        return {'newslist': ns}
    except:
        return {'result': u'此用户没有导航记录'}


@app.route('/wxuser_search_add/<wxopenid>/<address>/<longitude>/<latitude>/<city>/')
def wxuser_search_add(wxopenid, address, longitude, latitude, city):
    wxuser = Wxuser.query.filter(Wxuser.wx_openid == wxopenid).first()
    if wxuser:
        search_wx = Search()
        # search_wx.wxuser_id = wxuser.id
        search_wx.s_wxuser = wxuser
        search_wx.address = address
        search_wx.longitude = longitude
        search_wx.latitude = latitude
        search_wx.city = city
        db.session.add(search_wx)
        db.session.commit()
        return {'result': u'上传成功'}
    else:
        return {'ressult': u'上传失败'}


@app.route('/wxuser_search_get/<wxopenid>/')
def wxuser_search_get(wxopenid):
    wxuser = Wxuser.query.filter(Wxuser.wx_openid == wxopenid).first()
    try:
        ns = Search.query.filter(Search.n_wxuser == wxuser).all()
        m = len(ns)
        for i in range(m):
            ns[i] = ns[i].to_json()
        return {'searchlist': ns}
    except:
        return {'result': u'此用户没有导航记录'}


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8090)
