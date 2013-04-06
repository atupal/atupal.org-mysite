
from application import app

from peewee import MySQLDatabase

def connect_db():
    return MySQLDatabase(app.config['DATABASE'], host = app.config['DATABASEHOST'], user = app.config['USERNAME'], passwd = app.config['PASSWORD'])
