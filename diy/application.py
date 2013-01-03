#coding=utf-8

from flask import Flask
from flask import render_template
import platform
application = Flask(__name__)
application.debug = True
#全局变量
OPENSHITF_DATA_DIR = '/home/atupal/tmp/'
MONDO_ADR = '127.0.0.1'

#OPENSHITF_DATA_DIR = '/var/lib/openshift/d06c01f430bd4b308790e4e01b409d6a/app-root/data/'
#MONDO_ADR = 'mongodb://admin:JryxhKULsAQc@127.9.114.1:27017/'
CONN_MONGO = None
i = 0

#记录pid到文件:profile.pid
##如果存在就kill掉当前进程
import os
import sys
#
#pid = str(os.getpid())
#pidfile = '/tmp/geventPythonServer.pid'



@application.route("/")
def index():
    global i
    return str(++ i)
    return 'Hello from Flask !'

@application.route("/info")
def info():
    return platform.python_version()

import random
@application.route('/ts')
def ts():
    return 'just for s test!' + str(random.random())

@application.route('/hello')
@application.route('/hello/<name>')
def hello(name = None):
    return render_template('hello.html', name = name)

@application.route('/lo')
@application.route('/lo/<name>')
def lo(name = None):
    return render_template('login.html', name = name)

@application.route('/register', methods=['POST', 'GET'])
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

@application.route('/deleteuser', methods = ['GET', 'POST'])
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

from flask import request
@application.route('/login', methods=['POST', 'GET'])
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

@application.route('/editCode')
@application.route('/editCode/<name>')
def editCode(name = None):
    return render_template('editCode.html', name = name)

@application.route('/game')
@application.route('/game/<name>')
def game(name = None):
    return render_template('gameset.html', name = name)

@application.route('/games/chidouren/chidouren.html')
def chidouren():
    return render_template('games/chidouren/chidouren.html')

import subprocess
application.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
from flask import session,redirect,url_for,escape,request
@application.route('/action', methods=['POST', 'GET'])
def action():
    prefix = None
    if 'username' in session:
        prefix = OPENSHITF_DATA_DIR + '/code/' + session['username'] + '/'
    else :
        return redirect(url_for('lo'))
    #conn = pymongo.Connection(os.environ['OPENSHIFT_MONGODB_DB_URL'])
    #db = conn[os.environ['OPENSHIFT_APP_NAME']]
    #db.editCode.insert({"tmp": request.form['codestr']})

    reload(sys)
    sys.setdefaultencoding('utf-8')

    fi = open(prefix + '/tmp.cpp', 'w')
    if not fi:
        return 'error'
    #cmd = 'echo ' + '"' + request.form['codestr'] + '"' + '>'+ '
    fi.write(request.form['codestr'])
    fi.close() #此处必须要close，不然会造成ast（抽象语法分析树，即源代码）仍停留在缓存当中，找成编译的时候找不到main函数入口等奇葩的错误
    fi = open(prefix + '/in.dat', 'w')
    if not fi:
        return 'error'
    fi.write(request.form['input'])
    fi.write('\r\n')
    fi.close()
    #tmp = os.popen(cmd)
    #tmp = os.popen('g++ -c ni.cpp')
    p = subprocess.Popen(['g++', prefix + '/tmp.cpp', '-o', prefix + '/a.out'], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    p.wait()
    stdoutdata, stderrdata = p.communicate()
    if p.returncode != 0 :
        return stderrdata.replace(prefix, '...')

    p = subprocess.Popen([prefix + './a.out<' + prefix + 'in.dat'], shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    #这里原先是把a.out和<in.dat分开的，找成无法读取，这是因为subprocess会把<in.dat当成参数而不是命令的一部分，
    #同样，不能把参数和命令接在一起作为一个字符串，stdout和stderr是指定管道，不然在下面就无法获取程序执行结果的输出了
    #p.wait()
    import time
    import signal
    start = time.time()
    flag = 0;
    while 1:
        runtime = time.time() - start
        if p.poll() == 0:
            break
        elif runtime >= 5:
            flag = 1;
            #os.kill(p.pid + 1, signal.SIGKILL)
            p = subprocess.Popen(['kill -9 `pgrep a.out`'], shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
            p.wait()
            break;
    stdoutdata, stderrdata = p.communicate()
    if p.returncode != 0 :
        return stderrdata

    if flag == 1:
        stdoutdata += '\ntime out!\n'
    stdoutdata = 'runtime:%fs\noutput:\n'%runtime + stdoutdata
    return stdoutdata

#@application.route('gdbapi', methods = ['GET', 'POST'])
#def gdbapi():
#    if 'username' in session:
#        prefix = OPENSHITF_DATA_DIR + '/code/' + session['username'] + '/'
#    else:
#        return redirect(url_for('lo'))
#    filename = request.form

@application.route('/saveCode', methods = ['GET', 'POST'])
def saveCode():
    if 'username' in session:
        prefix = OPENSHITF_DATA_DIR + '/code/' + session['username'] + '/'
    else :
        return redirect(url_for('lo'))
    filename = request.form['filename']
    codestr = request.form['codestr']
    fi = open(prefix + filename, 'w')
    if not fi:
        return 'no'
    fi.write(codestr)
    fi.close()
    return 'yes'

@application.route('/getCode', methods = ['GET', 'POST'])
def getCode():
    if 'username' in session:
        prefix = OPENSHITF_DATA_DIR + '/code/' + session['username'] + '/'
    else:
        return redirect(url_for('lo'))
    p = subprocess.Popen(['ls', prefix], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    p.wait()
    stdout, stderr = p.communicate()
    return stdout

@application.route('/getFile', methods = ['GET', 'POST'])
def getFile():
    if 'username' in session:
        prefix = OPENSHITF_DATA_DIR + '/code/' + session['username'] + '/'
        fi = open(prefix + request.form['file_name'], 'r')
        return fi.read()
    else:
        return redirect(url_for('lo'))



@application.route('/manage')
def manage(name = None):
    return render_template('manage.html', name = name)

import re
@application.route('/applogs', methods = ['POST', 'GET'])
def applogs():
    fi = open('/var/lib/openshift/d06c01f430bd4b308790e4e01b409d6a/diy-0.1/logs/app.log', 'r')
    re = 'logs' + r'<hr/>'
    logs = fi.read()
    logs = logs.replace('<', '&lt;')
    logs = logs.replace('>', '&gt;')
    logs = logs.replace('\n', r'<br/>')
    logs = logs.split('*** Starting uWSGI 1.2.3 (64bit) on ')
    logs = logs[::-1]
    #reduce(lambda x,y:y+x,logs)
    for log in logs:
        re += log + r'<hr/>'
    return re

server_dir = '/var/lib/openshift/d06c01f430bd4b308790e4e01b409d6a/app-root/runtime/repo/diy/'
if (os.environ['HOME'] == '/home/atupal'):
    server_dir = './'
@application.route('/js/<path:name>')
def javascript(name):
    fi = open(server_dir + "static/js/" + name)
    return fi.read()

@application.route('/css/<path:name>')
def style(name):
    fi = open(server_dir + "static/css/" + name)
    return fi.read()

@application.route('/favicon.ico')
def ico():
    fi = open(server_dir + 'favicon.ico', "rb")
    return fi.read()

import pymongo
import json
from bson import json_util
from bson import objectid
import re
@application.route("/ws/parks")
def parks():
    #setup the connection
    conn = pymongo.Connection(os.environ['OPENSHIFT_MONGODB_DB_URL'])
    db = conn[os.environ['OPENSHIFT_APP_NAME']]

    #query the DB for all the parkpoints
    result = db.parkpoints.find()

    #Now turn the results into valid JSON
    return str(json.dumps({'results':list(result)},default=json_util.default))


#return a specific park given it's mongo _id
@application.route("/ws/parks/park/<parkId>")
def onePark(parkId):
    #setup the connection
    conn = pymongo.Connection(os.environ['OPENSHIFT_MONGODB_DB_URL'])
    db = conn[os.environ['OPENSHIFT_APP_NAME']]

    #query based on the objectid
    result = db.parkpoints.find({'_id': objectid.ObjectId(parkId)})

    #turn the results into valid JSON
    return str(json.dumps({'results' : list(result)},default=json_util.default))


#find parks near a lat and long passed in as query parameters (near?lat=45.5&lon=-82)
@application.route("/ws/parks/near")
def near():
    #setup the connection
    conn = pymongo.Connection(os.environ['OPENSHIFT_MONGODB_DB_URL'])
    db = conn[os.environ['OPENSHIFT_APP_NAME']]

    #get the request parameters
    lat = float(request.args.get('lat'))
    lon = float(request.args.get('lon'))

    #use the request parameters in the query
    result = db.parkpoints.find({"pos" : { "$near" : [lon,lat]}})

    #turn the results into valid JSON
    return str(json.dumps({'results' : list(result)},default=json_util.default))


#find parks with a certain name (use regex) near a lat long pair such as above
@application.route("/ws/parks/name/near/<name>")
def nameNear(name):
    #setup the connection
    conn = pymongo.Connection(os.environ['OPENSHIFT_MONGODB_DB_URL'])
    db = conn[os.environ['OPENSHIFT_APP_NAME']]

    #get the request parameters
    lat = float(request.args.get('lat'))
    lon = float(request.args.get('lon'))

    #compile the regex we want to search for and make it case insensitive
    myregex = re.compile(name, re.I)

    #use the request parameters in the query along with the regex
    result = db.parkpoints.find({"Name" : myregex, "pos" : { "$near" : [lon,lat]}})

    #turn the results into valid JSON
    return str(json.dumps({'results' : list(result)},default=json_util.default))


#if __name__ == '__main__':
#    application.run()


from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from flask import Flask, request, render_template

@application.route('/wstest')
def wstest():
    return render_template('wstest.html')

@application.route('/api')
def api():
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']
        i = 0
        while True:
            i = i + 1
            message = ws.receive()
            ws.send(str(i))
    return

if __name__ == '__main__':
    http_server = WSGIServer(('127.9.114.1',8080), application, handler_class=WebSocketHandler)
    http_server.serve_forever()
