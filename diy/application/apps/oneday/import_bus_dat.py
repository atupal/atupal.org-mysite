#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import pymongo
import json
import time

def imp(i):
    cnt = 0
    #inf = 10000000000
    inf = -1
    #buses = pymongo.Connection("127.0.0.1", 27017).bus
    with open("/home/atupal/res/code/bus_"+str(i)+".dat", 'r') as fi:
        global time
        while 1:

            t = fi.readline()
            name = t.split(' ')
            if name[0] == '' or name[0] == None:
                break
            line = ''
            for i in xrange(0, len(name) - 1):
                line += name[i + 1] + ' '
            line = line[:len(line) - 3]
            bus = fi.readline()
            try:
                bus = json.loads(bus)
            except:
                cnt += 1
                continue
            result_num = bus['result_num']
            if int(result_num) != 0:
                dist = bus['buses']['bus'][0]['dist']
                time  = bus['buses']['bus'][0]['time']
                foot_dist = bus['buses']['bus'][0]['foot_dist']
                last_foot_dist = bus['buses']['bus'][0]['last_foot_dist']
                segments = bus['buses']['bus'][0]['segments']
                buses.buses.insert({
                    'line': line,
                    'dist': dist,
                    'time': time,
                    'foot_dist': foot_dist,
                    'last_foot_dist': last_foot_dist,
                    'segments': segments
                    })
            else:
                buses.buses.insert({
                    'line':line,
                    'dist':inf,
                    'time':inf,
                    'foot_dist':'',
                    'last_foot_dist':'',
                    'segments':''
                    })
        print cnt



if __name__ == "__main__":
    for i in xrange(12):
        imp(i +1)

