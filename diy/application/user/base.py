#coding=utf-8

#from flask import Flask
from flask import render_template
import platform
import time
import signal
from application import app
#全局变量
#OPENSHITF_DATA_DIR = '/home/atupal/tmp/'
#MONDO_ADR = '127.0.0.1'

OPENSHITF_DATA_DIR = '/var/lib/openshift/d06c01f430bd4b308790e4e01b409d6a/app-root/data/'
MONDO_ADR = 'mongodb://admin:JryxhKULsAQc@127.9.114.1:27017/'
CONN_MONGO = None
import os
if (os.environ['HOME'] == '/home/atupal'):
    OPENSHITF_DATA_DIR = '/home/atupal/tmp/'
    MONDO_ADR = '127.0.0.1'

#记录pid到文件:profile.pid
##如果存在就kill掉当前进程
import sys
import pymongo

@app.route('/lo')
@app.route('/lo/<name>')
def lo(name = None):
    return render_template('login.html', name = name)

@app.route('/register', methods=['POST', 'GET'])
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
        p = subprocess.Popen(['mkdir', OPENSHITF_DATA_DIR + '/code/' + request.form['username']], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()
        return 'welcome' + user.find_one({'username':request.form['username']})['username']

from flask import session
@app.route('/deleteuser', methods = ['GET', 'POST'])
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

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
from flask import session,redirect,url_for,escape,request
@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'], request.form['password']):
            return log_the_user_in(request.form['username'])
        else :
            error = 'Invalid username/password'
    else:
        return 'your method is get'
    return error


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
    return 'welcome' + username

def logout():
    #如果会话中有用户名就删除他
    session.pop('username', None)

