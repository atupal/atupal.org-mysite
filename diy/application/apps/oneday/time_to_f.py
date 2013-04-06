#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import json

times = dict()

def imp(i):
    cnt = 0

    with open("/home/atupal/res/code/bus_"+str(i)+".dat", 'r') as fi:
        global times
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
                time  = bus['buses']['bus'][0]['time']
                if int(time) == 10000000000:
                    time[line] = -1
                else:
                    times[line] = time
            else:
                times[line] = -1
        print cnt



if __name__ == "__main__":
    for i in xrange(12):
        imp(i +1)
    fi = open('time_bak.dat', 'w')
    fi.write(json.dumps(times))
    fi.close()
