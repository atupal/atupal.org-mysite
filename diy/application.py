#coding=utf-8

from flask import Flask
from flask import render_template
import platform
application = Flask(__name__)
application.debug = True
 
@application.route("/")
def index():
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
	if username == 'atupal' and password == '123':
		return 1

def log_the_user_in(username):
	return 'welcome' + username

application.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
from flask import session,redirect,url_for,escape,request
@application.route('/editCode')
@application.route('/editCode/<name>')
def editCode(name = None):
	if usernmae in session:
		return render_template('editCode.html', name = name)
	else :
		return render_template('login.html', name = name)

@application.route('/game')
@application.route('/game/<name>')
def game(name = None):
	return render_template('gameset.html', name = name)

@application.route('/games/chidouren/chidouren.html')
def chidouren():
	return render_template('games/chidouren/chidouren.html')

import os
import subprocess
@application.route('/action', methods=['POST', 'GET'])
def nimei():
	#conn = pymongo.Connection(os.environ['OPENSHIFT_MONGODB_DB_URL'])
	#db = conn[os.environ['OPENSHIFT_APP_NAME']]
	#db.editCode.insert({"tmp": request.form['codestr']})
	fi = open('ni.cpp', 'w')
	#cmd = 'echo ' + '"' + request.form['codestr'] + '"' + '>'+ '
	fi.write(request.form['codestr'])
	fi.close() #此处必须要close，不然会造成ast（抽象语法分析树，即源代码）仍停留在缓存当中，找成编译的时候找不到main函数入口等奇葩的错误
	fi = open('in.dat', 'w')
	fi.write(request.form['input'])
	fi.write('\r\n')
	fi.close()
	#tmp = os.popen(cmd)
	#tmp = os.popen('g++ -c ni.cpp')
	p = subprocess.Popen(['g++', 'ni.cpp'], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
	p.wait()
	stdoutdata, stderrdata = p.communicate()
	if p.returncode != 0 :
		return stderrdata

	p = subprocess.Popen(['./a.out<in.dat'], shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
	#这里原先是把a.out和<in.dat分开的，找成无法读取，这是因为subprocess会把<in.dat当成参数而不是命令的一部分，
	#同样，不能把参数和命令接在一起作为一个字符串，stdout和stderr是指定管道，不然在下面就无法获取程序执行结果的输出了
	p.wait()
	stdoutdata, stderrdata = p.communicate()
	if p.returncode != 0 :
		return stderrdata

	return stdoutdata

@application.route('/manage')
def manage(name = None):
	return render_template('manage.html', name = name)

import re
@application.route('/applogs', methods = ['POST', 'GET'])
def applogs():
	fi = open('/var/lib/openshift/d06c01f430bd4b308790e4e01b409d6a/diy-0.1/logs/app.log', 'r')
	patter = re.compile(r'[***]')
	logs = fi.read().replace('***', '\n')
	return logs

@application.route("/ts")
def ts():
	return 'sdf'
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


@application.route("/test")
def test():
	return "<strong>It actually worked</strong>"
