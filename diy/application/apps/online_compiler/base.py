
#coding=utf-8

#from flask import Flask
from flask import render_template
import platform
import time
import signal
#application = Flask(__name__)
from application import app
#app.debug = True
import os

#全局变量
#OPENSHITF_DATA_DIR = '/home/atupal/tmp/'
#MONDO_ADR = '127.0.0.1'
server_dir = '/var/lib/openshift/d06c01f430bd4b308790e4e01b409d6a/app-root/runtime/repo/diy/application/'
OPENSHITF_DATA_DIR = '/var/lib/openshift/d06c01f430bd4b308790e4e01b409d6a/app-root/data/'
MONDO_ADR = 'mongodb://admin:JryxhKULsAQc@127.9.114.1:27017/'
CONN_MONGO = None
if (os.environ['HOME'] == '/home/atupal'):
    server_dir = './application/'
    OPENSHITF_DATA_DIR = '/home/atupal/tmp/'
    MONDO_ADR = '127.0.0.1'

#记录pid到文件:profile.pid
##如果存在就kill掉当前进程
import sys
#
#pid = str(os.getpid())
#pidfile = '/tmp/geventPythonServer.pid'

@app.route('/editCode')
@app.route('/editCode/<name>')
def editCode(name = None):
    return render_template('editCode.html', name = name)

import subprocess,re
from flask import session,redirect,url_for,escape,request
@app.route('/action', methods=['POST', 'GET'])
def action():
    prefix = None
    if 'username' in session:
        prefix = OPENSHITF_DATA_DIR + '/code/' + session['username'] + '/'
    else :
        return redirect(url_for('lo'))
    #conn = pymongo.Connection(os.environ['OPENSHIFT_MONGODB_DB_URL'])
    #db = conn[os.environ['OPENSHIFT_APP_NAME']]
    #db.editCode.insert({"tmp": request.form['codestr']})

    reload(sys)
    sys.setdefaultencoding('utf-8')

    fi = open(prefix + '/tmp.cpp', 'w')
    if not fi:
        return 'error'
    #cmd = 'echo ' + '"' + request.form['codestr'] + '"' + '>'+ '
    headfile = re.findall("#include<([a-z.]{1,10})>", request.form['codestr'])
    valid_headfile = {'stdio.h','cstdio', 'stdlib.h', 'cstdlib', 'string.h','cstring', 'math.h', 'cmath','vector.h','vector', 'algorithm.h','algorithm' ,'queue.h', 'queue'}
    for i in headfile:
        print i
        if not i in valid_headfile:
            return "invalid headfile:" + i

    if request.form['codestr'].find('system(') != -1:
        return "invalid func system()"

    fi.write(request.form['codestr'])
    fi.close() #此处必须要close，不然会造成ast（抽象语法分析树，即源代码）仍停留在缓存当中，找成编译的时候找不到main函数入口等奇葩的错误
    fi = open(prefix + '/in.dat', 'w')
    if not fi:
        return 'error'
    fi.write(request.form['input'])
    fi.write('\r\n')
    fi.close()
    #tmp = os.popen(cmd)
    #tmp = os.popen('g++ -c ni.cpp')
    if request.form['codeType'] == 'python':
        p = subprocess.Popen(['python', prefix + '/tmp.cpp' + '<' + prefix + '/in.dat'], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        start = time.time()
        flag = 0
        while 1:
            runtime = time.time() - start
            if p.poll() == 0:
                break
            elif runtime >= 25:
                flag = 1
                p = subprocess.Popen(['pkill tmp.cpp'], shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
                p.wait()
                break
        stdoutdata, stderrdata = p.communicate()
        if p.returncode != 0 :
            return stderrdata

        if flag == 1:
            stdoutdata += '\ntime out!\n'
        stdoutdata = 'runtime:%fs\noutput:\n'%runtime + stdoutdata + stderrdata
        return stdoutdata
    p = subprocess.Popen(['g++', '-g', prefix + '/tmp.cpp', '-o', prefix + '/a.out'], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    p.wait()
    stdoutdata, stderrdata = p.communicate()
    if p.returncode != 0 :
        return stderrdata.replace(prefix, '...')

    p = subprocess.Popen([prefix + './a.out<' + prefix + 'in.dat'], shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    #这里原先是把a.out和<in.dat分开的，找成无法读取，这是因为subprocess会把<in.dat当成参数而不是命令的一部分，
    #同样，不能把参数和命令接在一起作为一个字符串，stdout和stderr是指定管道，不然在下面就无法获取程序执行结果的输出了
    #p.wait()
    start = time.time()
    flag = 0;
    while 1:
        runtime = time.time() - start
        if p.poll() == 0:
            break
        elif runtime >= 5:
            flag = 1;
            #os.kill(p.pid + 1, signal.SIGKILL)
            p = subprocess.Popen(['kill -9 `pgrep a.out`'], shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
            p.wait()
            break;
    stdoutdata, stderrdata = p.communicate()
    if p.returncode != 0 :
        return stderrdata

    if flag == 1:
        stdoutdata += '\ntime out!\n'
    stdoutdata = 'runtime:%fs\noutput:\n'%runtime + stdoutdata
    return stdoutdata

#@app.route('gdbapi', methods = ['GET', 'POST'])
#def gdbapi():
#    if 'username' in session:
#        prefix = OPENSHITF_DATA_DIR + '/code/' + session['username'] + '/'
#    else:
#        return redirect(url_for('lo'))
#    filename = request.form

@app.route('/saveCode', methods = ['GET', 'POST'])
def saveCode():
    if 'username' in session:
        prefix = OPENSHITF_DATA_DIR + '/code/' + session['username'] + '/'
    else :
        return redirect(url_for('lo'))
    filename = request.form['filename']
    codestr = request.form['codestr']
    fi = open(prefix + filename, 'w')
    if not fi:
        return 'no'
    fi.write(codestr)
    fi.close()
    return 'yes'

@app.route('/getCode', methods = ['GET', 'POST'])
def getCode():
    if 'username' in session:
        prefix = OPENSHITF_DATA_DIR + '/code/' + session['username'] + '/'
    else:
        return redirect(url_for('lo'))
    p = subprocess.Popen(['ls', prefix], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    p.wait()
    stdout, stderr = p.communicate()
    return stdout

@app.route('/getFile', methods = ['GET', 'POST'])
def getFile():
    if 'username' in session:
        prefix = OPENSHITF_DATA_DIR + '/code/' + session['username'] + '/'
        fi = open(prefix + request.form['file_name'], 'r')
        return fi.read()
    else:
        return redirect(url_for('lo'))


from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from flask import Flask, request, render_template

@app.route('/wstest', methods=['GET', 'POST'])
def wstest():
    return render_template('wstest.html')

@app.route('/api')
def api():
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']
        i = 0
#        while True:
#            i = i + 1
#            message = ws.receive()
#            try:
#                p = subprocess.Popen([message], stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
#                p.wait()
#                ws.send(p.communicate()[0])
#            except:
#                ws.send('exception:', message)
#            ws.send(str(i) + "nimei")
#    return "error"
        import select
        from subprocess import *
        proc = Popen(['gdb'], stdin = PIPE, stderr = PIPE, stdout = PIPE)
        while proc.poll() == None:
            import fcntl
            import os
            import urllib
            fcntl.fcntl(
                    proc.stdout.fileno(),
                    fcntl.F_SETFL,
                    fcntl.fcntl(proc.stdout.fileno(), fcntl.F_GETFL) | os.O_NONBLOCK,
                    )

            fcntl.fcntl(
                    proc.stderr.fileno(),
                    fcntl.F_SETFL,
                    fcntl.fcntl(proc.stderr.fileno(), fcntl.F_GETFL) | os.O_NONBLOCK,
                    )

            while proc.poll() == None:
                readx = select.select([proc.stdout.fileno()], [], [], 0.1)[0]
                readx_err = select.select([proc.stderr.fileno()], [], [], 0.1)[0]
                if readx:
                    chunk = proc.stdout.read()
                    print chunk
                    #chunk = urllib.quote(chunk.encode('utf-8'))
                    chunk = chunk.replace('<', '&lt;')
                    chunk = chunk.replace('>', '&gt;')
                    chunk = chunk.replace('\n', r'<br/>')
                    ws.send(chunk)
                elif readx_err:
                    chunk = proc.stderr.read()
                    print chunk
                    #chunk = urllib.quote_plus(chunk.encode('utf-8'))
                    chunk = chunk.replace('<', '&lt;')
                    chunk = chunk.replace('>', '&gt;')
                    chunk = chunk.replace('\n', r'<br/>')
                    ws.send(chunk)
                else:
                    break
           # cmd = raw_input("cmd:")
           # proc.stdin.write(cmd + '\n')
           # proc.stdin.flush()
            cmd = ws.receive()
            proc.stdin.write(cmd + '\n')
            proc.stdin.flush()
        proc.wait()

