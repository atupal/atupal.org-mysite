#coding=utf-8
from flask import render_template
from application import app

CONN_MONGO = None

@app.route('/manage')
def manage(name = None):
    return render_template('manage.html', name = name)

@app.route('/applogs', methods = ['POST', 'GET'])
def applogs():
    fi = open(app.config['APPLICATION_LOGS_DIR'] + 'app.log', 'r')
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
