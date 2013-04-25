#coding=utf-8

from application import app
from flask import request
from application.apps.oneday import getLine
from application.apps.oneday import getInfo
from application.apps.oneday import shakeList

import urllib2
import json
import os
import pymongo

if os.environ['HOME'] == "/home/atupal":
    OPENSHIFT_ADR = '127.0.0.1'
    OPENSHIFT_DIR = '/home/atupal/src/rhc/py27/diy/'
else:
    OPENSHIFT_ADR = os.environ['OPENSHIFT_MONGODB_DB_URL']
    OPENSHIFT_DIR = os.environ['OPENSHIFT_REPO_DIR'] +'/diy/'

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
    return getLine.Line().getline(lat, lng, begin, end)

@app.route('/getLine', methods = ['GET', 'POST'])
def getLineInfo():
    bus = pymongo.Connection(OPENSHIFT_ADR, 27017).bus.buses
    line = str(request.form['line']).split('__')
    lat = float(request.form['lat'])
    lng = float(request.form['lng'])
    #img = []
    #intra = []
    #bus = []
    #map_1 = []
    ret = dict()
    for i in xrange(len(line)):
        tmp = getInfo.getInfo(line[i])
        tmp['img'] = tmp['img'][:2]
        tmp.pop('map')
        #img.append(tmp['img'])
        #intra.append(tmp['intra'])
        #bus.append(tmp['bus'])
        #map_1.append("http://api.map.baidu.com/staticimage?markers=" + urllib.quote(line[i]) + "&center=" + urllib.quote(line[i]))
        if i > 0:
            oneday = pymongo.Connection(OPENSHIFT_ADR, 27017).oneday.play
            p = oneday.find_one({'name': line[i - 1]})
            n = oneday.find_one({'name': line[i]})
            url = ('http://openapi.aibang.com/bus/transfer?app_key=f41c8afccc586de03a99c86097e98ccb&city=%E6%AD%A6%E6%B1%89&start_lat='
                    +str(p['lat'])+'&start_lng='+str(p['lng'])+'&end_lat='+str(n['lat'])+'&end_lng='+str(n['lng'])+'&alt=json')
            _bus = json.load(urllib2.urlopen(url))

            try:
                s = ''
                for index in xrange(len(_bus['buses']['bus'][0]['segments']['segment'])):
                    t = _bus['buses']['bus'][0]['segments']['segment'][index]
                    s += '步行' + t['foot_dist'] + '米至'  + t['start_stat'] + '\n'
                    s += '搭乘' + t['start_stat'] + '  经过' + t['stats'] + ' 到达' + t['end_stat']
                    s += '\n'
                tmp['bus'] = s
            except:
                tmp['bus'] = "没有公交或者距离很近步行可达"

            #数据库挂了，直接向api请求
            '''
            _bus = bus.find({'line': line[i - 1] + ' '  + line[i]})
            _bus = [b for b in _bus]
            if not _bus:
                _bus = bus.find({'line': line[i] + ' ' + line[i - 1]})
                _bus = [b for b in _bus]

            try:
                s = ''
                for index in xrange(len(_bus[0]['segments']['segment'])):
                    t = _bus[0]['segments']['segment'][index]
                    s += '步行' + t['foot_dist'] + '米至'  + t['start_stat'] + '\n'
                    s += '搭乘' + t['start_stat'] + '  经过' + t['stats'] + ' 到达' + t['end_stat']
                    s += '\n'
                tmp['bus'] = s
            except:
                tmp['bus'] = "没有公交或者距离很近步行可达"

            '''

        ret['name_' + str(i + 1)] = tmp

    oneday = pymongo.Connection(OPENSHIFT_ADR, 27017).oneday.play
    j = oneday.find_one({'name': line[0]})
    url = ('http://openapi.aibang.com/bus/transfer?app_key=f41c8afccc586de03a99c86097e98ccb&city=%E6%AD%A6%E6%B1%89&start_lat='
            +str(lat)+'&start_lng='+str(lng)+'&end_lat='+str(j['lat'])+'&end_lng='+str(j['lng'])+'&alt=json')
    _bus = json.load(urllib2.urlopen(url))
    print _bus['buses']['bus'][0]
    print ''

    try:
        s = ''
        for index in xrange(len(_bus['buses']['bus'][0]['segments']['segment'])):
            t = _bus['buses']['bus'][0]['segments']['segment'][index]
            s += '步行' + t['foot_dist'] + '米至'  + t['start_stat'] + '\n'
            s += '搭乘' + t['start_stat'] + '  经过' + t['stats'] + ' 到达' + t['end_stat']
            s += '\n'
        ret['name_1']['bus'] = s
    except:
        ret['name_1']['bus'] = "没有公交或者距离很近步行可达"

    j = oneday.find_one({'name': line[len(line) - 1]})
    url = ('http://openapi.aibang.com/bus/transfer?app_key=f41c8afccc586de03a99c86097e98ccb&city=%E6%AD%A6%E6%B1%89&start_lat='
    + str(j['lat'])+'&start_lng='+str(j['lng'])+'&end_lat='+str(lat)+'&end_lng='+str(lng)+'&alt=json')

    _bus = json.load(urllib2.urlopen(url))
    print _bus['buses']['bus'][0]
    print ''
    try:
        s = ''
        for index in xrange(len(_bus['buses']['bus'][0]['segments']['segment'])):
            t = _bus['buses']['bus'][0]['segments']['segment'][index]
            s += '步行' + t['foot_dist'] + '米至'  + t['start_stat'] + '\n'
            s += '搭乘' + t['start_stat'] + '  经过' + t['stats'] + ' 到达' + t['end_stat']
            s += '\n'
        ret['name_' + str(len(line))]['bus'] = s
    except Exception as e:
        print e
        ret['name_' + str(len(line))]['bus'] += "__" + "没有公交或者距离很近步行可达"


    map_3 = "http://api.map.baidu.com/staticimage?center=116.403874,39.914889&width=400&height=300&zoom=11&markers=116.288891,40.004261|116.487812,40.017524|116.525756,39.967111|116.536105,39.872374|116.442968,39.797022|116.270494,39.851993|116.275093,39.935251|116.383177,39.923743&markerStyles=l,A|m,B|l,C|l,D|m,E|,|l,G|m,H"
    ret['map'] = map_3
    #ret = {
    #        'map_3':map_3,
    #        'map_1':map_1,
    #        'img':img,
    #        'intra':intra,
    #        'bus':bus
    #        }

    return json.dumps(ret)

@app.route('/getPlace', methods = ['GET', 'POST'])
def getPlaceInfo():
    name = str(request.form['name'])
    tmp = getInfo.getInfo(name)
    return json.dumps(tmp)

@app.route('/shakeLine', methods = ['GET', 'POST'])
def oneday_api_shakeList():
    ret = shakeList.ShakeList().shakelist(request.form['lat'], request.form['lng'], request.form['place'], request.form['people'], request.form['transportation'], request.form['money'])
    ret = json.loads(ret)
    return json.dumps(ret[0])
