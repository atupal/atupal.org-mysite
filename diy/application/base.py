
from application import app

from peewee import MySQLDatabase

def connect_db():
    return MySQLDatabase(app.config['DATABASE'], host = app.config['DATABASEHOST'], user = app.config['USERNAME'], passwd = app.config['PASSWORD'])

@app.route('/googlef6a9c359439ec2c6.html')
def  google():
    return "google-site-verification: googlef6a9c359439ec2c6.html"

@app.route('/robots.txt')
def robots_txt():
    return open('./application/robots.txt', 'r').read()
