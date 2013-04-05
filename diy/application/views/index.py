#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask import Flask
app = Flask(__name__)

if __name__ != "__main__":
    from application import app
    from flask import render_template

@app.route("/")
def index(name = None):
    return render_template('views/index.html', rsslist = formatrss(getrsslist()) )

@app.route("/about")
def about():
    return render_template("views/about.html")

@app.route("/contact")
def contanct():
    return render_template("views/contact.html")

@app.route("/blog")
def blog():
    return render_template("views/blog.html")


#从远程mysql数据库获取用户rss列表，默认是atupal的
from peewee import *
#import MySQLdb
def getrsslist():
    db = MySQLDatabase('atupalsite', user='atupal', host='db4free.net', passwd='LKYs4690102')
    #conn = MySQLdb.connect(host = 'db4free.net', user = 'atupal', passwd = 'LKYs4690102', db = 'atupalsite')
    #cur = conn.cursor()
    rsslist = db.execute('select name, xmlurl from rsslist where user="atupal"')
    rsslist = rsslist.fetchall()
    #rsslist = cur.fetchall()

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

#if __name__ == "__main__":
#    print getrsslist()


