#coding=utf-8

#from flask import Flask
#import platform
#import time
#import signal
from application import app
import application.views.index as index_mod
#全局变量
#OPENSHITF_DATA_DIR = '/home/atupal/tmp/'
#MONDO_ADR = '127.0.0.1'

import os
#这是硬编码。。。不具备通用性，改用环境变量
#OPENSHITF_DATA_DIR = '/var/lib/openshift/d06c01f430bd4b308790e4e01b409d6a/app-root/data/'
#MONDO_ADR = 'mongodb://admin:JryxhKULsAQc@127.9.114.1:27017/'


CONN_MONGO = None
if (os.environ['HOME'] == '/home/atupal'):
    OPENSHITF_DATA_DIR = '/home/atupal/tmp/'
    #因为使用两个数据库的话会很不方便，所以这里之使用openshift上的远程数据库，在本地测试的时候使用ssh的端口转发连接到openshift上的mongodb数据库上

    #后来想了一下，还是用本地的数据库测试吧。。哭，网速太慢了
    MONDO_ADR = '127.0.0.1'
else:
    OPENSHITF_DATA_DIR = os.environ['OPENSHIFT_DATA_DIR']
    MONDO_ADR = os.environ['OPENSHIFT_MONGODB_DB_URL']

#记录pid到文件:profile.pid
##如果存在就kill掉当前进程
#import sys
import pymongo

#from flask import session,redirect,url_for,escape,request, redirect
from flask import session, request, render_template,redirect, url_for, flash,abort
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

'''
@app.route('/lo')
@app.route('/lo/<name>')
def lo(name = None):
    return render_template('login.html', name = name)
'''


'''
注册用户
post 数据如下：
{
    username:'xx',
    password:'**'
}
'''
import subprocess
@app.route('/user/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        CONN_MONGO = pymongo.Connection(MONDO_ADR)
        editCode = CONN_MONGO['editCode']
        user = editCode['user']
        if (user.find_one({'username':request.form['username']}) != None):
            return 'user exit!'
        _user = {
                'username': request.form['username'],
                'password': request.form['password']
                }
        user.insert(_user)

        #为editCode用户新建一个代码文件夹
        p = subprocess.Popen(['mkdir', OPENSHITF_DATA_DIR + '/code/' + request.form['username']], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()
        return 'welcome' + user.find_one({'username':request.form['username']})['username']

'''
注销用户
post 数据如下：
{
    username:'xx'
}
'''
@app.route('/user/deleteuser', methods = ['GET', 'POST'])
def deleteuser():
    if 'username' in session:
        pass
    else :
        return 'no login'
    CONN_MONGO = pymongo.Connection(MONDO_ADR)
    editCode = CONN_MONGO['editCode']
    user = editCode['user']
    if request.method != 'POST':
        user.remove({'username':session['username']})
        p = subprocess.Popen(['rm', OPENSHITF_DATA_DIR + '/code/' + session['username'], 'r'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()
        return 'delete' + session['username']
    elif request.methods == 'POST':
        if session['username'] != 'atupal':
            return 'not admin'
        user.remove({'username':request.form['username']})
        p = subprocess.Popen(['rm', OPENSHITF_DATA_DIR + '/code/' + request.form['username'], 'r'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()
        return 'delete' + request.form['username']

'''
用户登录

post 数据如下
{
    username:'xx',
    password:'**'
}
'''
@app.route('/user/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'], request.form['password']):
            index_mod.setcache(request.form['username'])
            return log_the_user_in(request.form['username'])
        else :
            error = 'Invalid username/password'
    else:
        return 'your method is get'
    return abort(401)
    return error

#登录验证

def valid_login(username, password):
    CONN_MONGO = pymongo.Connection(MONDO_ADR)
    editCode = CONN_MONGO['editCode']
    user = editCode['user']
    _password = user.find_one({'username':username})['password']
    print _password
    print password
    if password == _password:
        return 1

def log_the_user_in(username):
    session['username'] = username
    return redirect(url_for('index'))
    return 'welcome' + username

@app.route('/user/logout')
def logout():
    #如果会话中有用户名就删除他
    session.pop('username', None)
    flash('You were logged out')
    return redirect(url_for('index'))

