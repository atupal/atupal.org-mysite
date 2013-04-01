
from flask import Flask
app = Flask(__name__)
app.debug = True

#import application.base
import application.oneday.map_api
import application.oneday.getLine
import application.views.index
import application.oneday.base
import application.online_compiler.base
import application.user.base
import application.mongodb.base
import application.others.base
import application.site_manager.base

