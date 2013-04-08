
from application import app

from peewee import MySQLDatabase
import os

server_dir = '/var/lib/openshift/d06c01f430bd4b308790e4e01b409d6a/app-root/runtime/repo/diy/application/'

if (os.environ['HOME'] == '/home/atupal'):
    server_dir = './application/'

def connect_db():
    return MySQLDatabase(app.config['DATABASE'], host = app.config['DATABASEHOST'], user = app.config['USERNAME'], passwd = app.config['PASSWORD'])

@app.route('/googlef6a9c359439ec2c6.html')
def  google():
    return "google-site-verification: googlef6a9c359439ec2c6.html"

@app.route('/robots.txt')
def robots_txt():
    return open(server_dir + '/robots.txt', 'r').read().replace('\n', '<br>')
