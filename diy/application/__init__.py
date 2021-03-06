
from flask import Flask
app = Flask(__name__)
app.debug = app.config['DEBUG']

import application.base
import application.views.index
import application.views.blog
import application.views.oneday
import application.user.base
import application.mongodb.base
import application.others.base
import application.site_manager.base
import application.user.user_profile

import application.apps.online_compiler.base
import application.apps.oneday.base
import application.apps.oneday.map_api
import application.apps.oneday.getLine

import application.apps.github_api.base
