#coding=utf-8
from application import app
import os
from flask import render_template, send_from_directory, request, session

@app.route('/psb')
def psb():
    if "username" in session:
        pass
    else:
        pass
        #return redirect(url_for('lo'))
    return render_template('pintrest/test.html')

server_dir = '/var/lib/openshift/d06c01f430bd4b308790e4e01b409d6a/app-root/runtime/repo/diy/application/'
if (os.environ['HOME'] == '/home/atupal'):
    server_dir = './application/'
#@app.route('/js/<path:name>')
#def javascript(name):
#    fi = open(server_dir + "static/js/" + name)
#    return fi.read()
#
#@app.route('/images/<path:name>')
#def images(name):
#    fi = open(server_dir + "static/images/" + name)
#    return fi.read()
#
#@app.route('/css/<path:name>')
#def style(name):
#    fi = open(server_dir + "static/css/" + name)
#    return fi.read()
#
@app.route('/favicon.ico')
@app.route('/favicon.png')
def ico():
    #fi = open(server_dir + 'favicon.ico', "rb")
    #return fi.read()
    #return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')
    return send_from_directory(server_dir, 'favicon.ico', mimetype='image/vnd.microsoft.icon')
#
#@app.route('/static/<path:name>')
#def staticfile(name):
#    fi = open(server_dir + "static/" + name)
#    return fi.read()
#
@app.route('/getPic', methods = ['GET', 'POST'])
def getPic():
    startIndex = request.args.get('startIndex', '')
    count = request.args.get('count', '')
    startIndex = int(startIndex)
    count = int(count)
    result = ["psb_%d" % i for i in range(startIndex, startIndex + count)]
    result = ";".join(result)
    return result

