#coding=utf-8

import urllib2
import requests
import pymongo
import math
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def test():
    url = 'http://openapi.aibang.com/bus/transfer?app_key=c5c75c0fd8976a5fa7b3dae640e08756&city=%E5%8C%97%E4%BA%AC&start_addr=%E8%A5%BF%E7%9B%B4%E9%97%A8&end_addr=%E4%B8%9C%E7%9B%B4%E9%97%A8'
    proxy = urllib2.ProxyHandler({'https': '5.199.132.164:443'})
    opener = urllib2.build_opener(proxy, urllib2.HTTPHandler)
    urllib2.install_opener(opener)
    req = urllib2.Request(url)
    req.add_header('x-forward-for', '202.204.76.254')
    #req = urllib2.urlopen(req)
    proxies = {'http':'80.90.12.36:8080'}
    req = requests.get(url, proxies = proxies)
    print req.content

def dist_latlng(a, b):
    R = 6371.004
    C = math.sin(a['lat']) * math.sin(b['lat']) * math.cos(a['lng'] - b['lng']) + math.cos(a['lat']) * math.cos(b['lat'])
    C = 1.0 if C > 1.0 else C
    return R * math.acos(C) *math.pi / 180

def count():
    con = pymongo.Connection('127.0.0.1', 27017)
    oneday = con.oneday.play.find()
    oneday = [_ for _ in oneday]
    cnt = int(raw_input("cnt:"))
    fi = open('./bus_3.dat', 'w')
    tmp = 0
    for _i, i in enumerate(oneday):
        for _j, j in enumerate(oneday):
            if _i < _j:
                tmp += 1
                if tmp >= cnt:
                    url = 'http://openapi.aibang.com/bus/transfer?app_key=f41c8afccc586de03a99c86097e98ccb&city=%E6%AD%A6%E6%B1%89&start_lat='+str(i['lat'])+'&start_lng='+str(i['lng'])+'&end_lat='+str(j['lat'])+'&end_lng='+str(j['lng'])+'&alt=json'
                    req = urllib2.urlopen(url)
                    content = req.read()
                    fi.write("%s %s %s:\n"%(str(tmp), i['name'], j['name']))
                    fi.write(content + "\n")
    fi.close()


if __name__ == '__main__':
    count()

