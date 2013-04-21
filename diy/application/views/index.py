#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask import Flask, session, request
app = Flask(__name__)

if __name__ != "__main__":
    from application import app
    from flask import render_template

@app.route("/")
def index(name = None):
    return render_template('views/index.html')
    return render_template('views/index.html', rsslist = getrsslist() )

@app.route("/about")
def about():
    return render_template("views/about.html")

@app.route("/contact")
def contanct():
    return render_template("views/contact.html")

#rsslist缓存对象
from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()

#从远程mysql数据库获取用户rss列表，默认是atupal的
from peewee import MySQLDatabase
#import MySQLdb
def setcache(username):
    db = MySQLDatabase(app.config['DATABASE'], host = app.config['DATABASEHOST'], user = app.config['USERNAME'], passwd = app.config['PASSWORD'])
    cur = db.get_cursor()
    #rsslist = db.execute('select name, xmlurl from rsslist where user="atupal"')
    #rsslist = rsslist.fetchall()
    cur.execute('select name, xmlurl from rsslist where user="' + str(username) + '"')
    rsslist = cur.fetchall()
    rsslist = formatrss(rsslist)
    cache.set('rsslist', rsslist, timeout = 60 * 60 * 24)
    return rsslist

def getrsslist():
    rsslist = cache.get('rsslist')
    username = 'atupal'
    if session.has_key('username'):
        username = session['username']
    if rsslist is None:
        return setcache(username)

    #db = MySQLdb.connect( host = 'db4free.net',
    #                      user = 'atupal',
    #                      passwd = 'LKYs4690102',
    #                      db = 'atupalsite'
    #        )

    #cur = db.cursor()

    #cur.execute('select * from rsslist')

    #for row in cur.fetchall():
    #    print row[0]
    return  rsslist

def formatrss(rsslist):
    rsslist = list(rsslist)
    for i, rss in enumerate(rsslist):
        rsslist[i] = list(rss)
        rsslist[i][0] = rsslist[i][0].decode('utf-8')
        rsslist[i][1] = rsslist[i][1].decode('utf-8')
    return rsslist

@app.route('/user/addrss', methods = ['POST', 'GET'])
def addrss():
    if session.has_key('username'):
        username = session['username']
    else:
        return 'no login'

    db = MySQLDatabase(app.config['DATABASE'], host = app.config['DATABASEHOST'], user = app.config['USERNAME'], passwd = app.config['PASSWORD'])
    cur = db.get_cursor()
    cur.execute('select count(id) from rsslist')
    count = cur.fetchall()
    count = int(count[0][0])
    cmd = 'insert into rsslist (id, name, xmlurl, htmlurl, user) values(' + str(count) + ',' + '"' + request.form['name'] + '"' + ',' + '"'+request.form['rssxml'] +'"'+ ',' + '"'+request.form['rsshtml'] +'"'+ ',' + '"'+username +'"'+ ')'
    cur.execute(cmd)
    #cur.commit()
    db.commit()
    setcache(username)
    return 'add finish'



#if __name__ == "__main__":
#    print getrsslist()


