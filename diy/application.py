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
	return 'just for s testi nimei'

@application.route('/hello')
@applicatoin.route('/hello/<name>')
def hello(name = None):
	return render_template('hello.html', name = name)
