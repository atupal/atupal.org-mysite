
from application import app
from flask import request
from application.oneday import getLine

@app.route('/getmap', methods = ['GET', 'POST'])
def getmap():
    lat = request.args.get('lat', '')
    lng = request.args.get('lng', '')
    lat = float('lat')
    lng = float('lng')

@app.route('/getList', methods = ['GET', 'POST'])
def getList():
    lat = float(request.form['lat'])
    lng = float(request.form['lng'])
    begin = int(request.form['begin'])
    end = int(request.form['end'])
    return getLine.Line().getList(lat, lng, begin, end)

