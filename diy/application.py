from flask import Flask
from flask import render_template
import platform
application = Flask(__name__)
 
@application.route("/")
def index():
	    return 'Hello from Flask !'
 
@application.route("/info")
def info():
	    return platform.python_version()

@application.route('/ts')
def ts():
	return 'just for s test!'

@application.route('/hello')
@application.route('/hello/<name>')
def hello(name = None):
	return render_template('hello.html', name = name)

@application.route('/lo')
@application.route('/lo/<name>')
def lo(name = None):
	return render_template('login.html', name = name)

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

