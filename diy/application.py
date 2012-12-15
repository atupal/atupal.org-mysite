from flask import Flask
import platform
application = Flask(__name__)
 
@application.route("/")
def index():
	    return 'Hello from Flask'
 
@application.route("/info")
def info():
	    return platform.python_version()
