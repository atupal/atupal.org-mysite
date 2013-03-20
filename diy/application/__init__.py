
from flask import Flask
app = Flask(__name__)
app.debug = True

import application.base
import application.oneday.map_api
import application.oneday.getLine
import application.views.index

