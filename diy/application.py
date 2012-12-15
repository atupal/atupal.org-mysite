from flask import Flask
from flask import render_template
import platform
application = Flask(__name__)
 
@application.route("/")
def index():
	    return 'Hello from Flask'
 
@application.route("/info")
def info():
	    return platform.python_version()

@application.route('/hello/')
@application.route('/hello/<name>')
def hello(name = None):
	return render_template('hello.html', name = name)
