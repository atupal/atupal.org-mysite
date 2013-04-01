
from flask import Flask
app = Flask(__name__)
app.debug = True

#import application.base
import application.views.index
import application.user.base
import application.mongodb.base
import application.others.base
import application.site_manager.base

import application.apps.online_compiler.base
import application.apps.oneday.base
import application.apps.oneday.map_api
import application.apps.oneday.getLine
