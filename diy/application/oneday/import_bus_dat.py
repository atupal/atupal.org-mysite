#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import pymongo
import json

def imp(i):
    buses = pymongo.Connection("127.0.0.1", 27017).bus
    with open("/home/atupal/res/code/bus_"+str(i)+".dat", 'r') as fi:
        while 1:
            try:
                name = fi.readline().split(' ')
                if len(name) == 0:
                    break
                line = ''
                for i in xrange(0, len(name) - 1):
                    line += name[i + 1]
                line = line[:len(line) - 2]
                bus = fi.readline()
                bus = json.loads(bus)
                result_num = bus['result_num']
                if int(result_num) != 0:
                    dist = bus['buses']['bus'][0]['dist']
                    time  = bus['buses']['bus'][0]['time']
                    foot_dist = bus['buses']['bus'][0]['foot_dist']
                    last_foot_dist = bus['buses']['bus'][0]['last_foot_dist']
                    segments = bus['buses']['bus'][0]['segments']
                    print({
                        'line': line,
                        'dist': dist,
                        'time': time,
                        'foot_dist': foot_dist,
                        'last_foot_dist': last_foot_dist,
                        'segments': segments
                        }['line'])
            except:
                print bus



if __name__ == "__main__":
    imp(1)

