#coding=utf-8
from flask import render_template
import signal
from application import app
import os

if os.environ['HOME'] == '/home/atupal':
    OPENSHITF_DATA_DIR = '/home/atupal/tmp/'
    MONDO_ADR = '127.0.0.1'
else:
    OPENSHITF_DATA_DIR = '/var/lib/openshift/d06c01f430bd4b308790e4e01b409d6a/app-root/data/'
    MONDO_ADR = 'mongodb://admin:JryxhKULsAQc@127.9.114.1:27017/'

CONN_MONGO = None

@app.route('/manage')
def manage(name = None):
    return render_template('manage.html', name = name)

import re
@app.route('/applogs', methods = ['POST', 'GET'])
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
