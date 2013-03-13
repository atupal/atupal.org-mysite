#coding=utf-8
import urllib
import time
import urllib2
import pymongo
import re
import math
import json
from xml.etree import ElementTree as ET
from random import randint
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Line:
    def __init__(self):
        connection = pymongo.Connection('localhost', 27017)
        db = connection.oneday
        self.flagset = set([])
        self.items = []

        self.class_cnt = 7
        self.item_classes = [[] for _ in xrange(self.class_cnt)]
        self.EAT, self.XIAOCHI, self.DRINK,self.JINDIAN, self.PLAY, self.KTK, self.OTHERS = xrange(self.class_cnt)
        self.pattern = []
        self.pattern.append(re.compile('豆皮|农家菜|粤菜|热干面|湘菜|卤味|东南亚菜|韩国料理|牛肉粉|比萨|西式简餐|火锅|川菜|烧烤|自助餐|湖北菜|小龙虾|汤包|日本料理|海鲜|牛排|快餐简餐|粉面馆|西餐'))
        self.pattern.append(re.compile('零食|面包糕点|小吃'))
        self.pattern.append(re.compile('甜品饮料|酒吧|咖啡厅|茶馆'))
        self.pattern.append(re.compile('景点|郊游|公园|文化艺术|电影院'))
        self.pattern.append(re.compile('台球室|游乐游艺|'))
        self.pattern.append(re.compile('KTV'))
        self.pattern.append(re.compile(''))
        self.avedist = 0.0
        self.place = None

        for _ in db.items.find():
            self.flagset.add(_['flag'][0])
            self.items.append(_)
            for i in xrange(self.class_cnt):
                if re.findall(self.pattern[i], _['flag'][0].encode('utf-8')):
                    self.item_classes[i].append(_)
                    break


        for _ in self.flagset:
            print _

        for i in self.item_classes:
            print len(i)
        print '**********************************'

    def itemType(self, item):
        #for i, pattern in enumerate(self.pattern):
        #    if re.findall(pattern, item['flag'][0].encode('utf-8')):
        #        return i
        #result = self.PLAY
        #s = item['flag'][0]
        #s = s.encode('utf-8')
        #if re.findall(self.eatPattern, s):
        #    result = self.EAT
        pass

        return result

    def main(self, lat, lng, flag, tag):
        cnt = 0
       # for item in self.items[1]:
       #     cnt += 1
       #     if item.has_key('lat'):
       #         print item['name'][0], item['lat'], item['lng']
        def dist(a, b):
            result = 100
            if a.has_key('lat') and b.has_key('lat'):
                result = math.sqrt( (a['lat'] - b['lat']) ** 2 + (a['lng'] - b['lng']) ** 2 )
            return result


        cnt = 0

        def getPlayLatlng():
            fi = open('res/play.dat', 'w')
            for i, itemplay in enumerate(self.items[1:]):
                for item in itemplay:
                    if item.has_key('lat') and item['lat'] // 1 == 30.0 and item['lng'] // 1 == 114.0:
                        fi.write(str(item['lat']) + ' '  + str(item['lng']) + ' ' + str(i) + '\r\n')
            fi.close()

        def isSameFlag(a, b):
            if a['flag'] == b['flag']:
                return 1
            if a['flag'].find('公园') != -1 and b['flag'].find('公园') != -1:
                return 1
            if a['flag'].find('景点') != -1 and b['flag'].find('景点') != -1:
                return 1
            if a['flag'].find('郊游') != -1 and b['flag'].find('郊游') != -1:
                return 1
            if a['flag'].find('文化') != -1 and b['flag'].find('文化') != -1:
                return 1
            if a['flag'].find('电影') != -1 and b['flag'].find('电影') != -1:
                return 1
            if a['name'].find('图书馆') != -1 and b['name'].find('图书馆') != -1:
                return 1

            if a['name'].find('剧院') != -1 and b['flag'].find('电影') != -1:
                return 1
            if b['name'].find('剧院') != -1 and a['flag'].find('电影') != -1:
                return 1



            if re.findall('书店|图书馆', a['flag'].encode('utf-8')) and re.findall('酒吧|KTV|台球室|桌面游戏|按摩|洗浴|电玩|游乐游艺', b['flag'].encode('utf-8')):
                return 1
            if re.findall('书店|图书馆', b['flag'.encode('utf-8')]) and re.findall('酒吧|KTV|台球室|桌面游戏|按摩|洗浴|电玩|游乐游艺', a['flag'].encode('utf-8')):
                return 1
            if re.findall('酒吧|KTV|台球室|桌面游戏|按摩|洗浴|电玩|游乐游艺', a['flag'].encode('utf-8')):
                if re.findall('文化|艺术', b['flag'].encode('utf-8')) and not re.findall('class', b['tags'].encode('utf-8')):
                    return 1
            if re.findall('酒吧|KTV|台球室|桌面游戏|按摩|洗浴|电玩|游乐游艺', b['flag'].encode('utf-8')):
                if re.findall('文化|艺术', a['flag'].encode('utf-8')) and not re.findall('class', a['tags'].encode('utf-8')):
                    return 1

            return 0

        def item_one_condition(item):
            if re.findall('酒吧|洗浴|按摩', item['flag'].encode('utf-8')):
                return 0
            return 1

        def item_two_condition(item):
            if re.findall('酒吧|洗浴|按摩', item['flag'].encode('utf-8')):
                return 0
            return 1

        def item_three_condition(item):
            #return 1 if randint(0, 100) < 1 else 0
            return 1


        def dist_latlng(a, b):
            R = 6371.004
            C = math.sin(a['lat']) * math.sin(b['lat']) * math.cos(a['lng'] - b['lng']) + math.cos(a['lat']) * math.cos(b['lat'])
            C = 1.0 if C > 1.0 else C
            return R * math.acos(C) *math.pi / 180

        def get_shortest_item(lat, lng):
            play = pymongo.Connection('localhost', 27017).oneday.play.find()
            play = [_ for _ in play]
            Min = []
            for b in play:
                try:
                    R = 6371.004
                    C = math.sin(lat) * math.sin(b['lat']) * math.cos(lng - b['lng']) + math.cos(lat) * math.cos(b['lat'])
                    if R * math.acos(C) *math.pi / 180 < 0.3:
                        Min.append(b)
                    #else: print R * math.acos(C) * math.pi
                except:
                    print 'erro'
            return Min

        def getTime(a, b):
            result = 100
            a = urllib.quote(str(a['lat']) + ',' + str(a['lng']))
            b = urllib.quote(str(b['lat']) + ',' + str(b['lng']))
            url = 'https://maps.googleapis.com/maps/api/directions/json?origin='+a+'&destination='+b+'&sensor=false&language=zh_cn&region=cn'
            req = urllib2.Request(url)
            req = urllib2.urlopen(url)
            req = json.load(req)
            try:
                print req['routes'][0]['legs'][0]['distance']['text'].split(' ')[0]
            except:
                print req

            return result

        def get_map(a, b):
            result = 100
            a = urllib.quote(str(a['lat']) + ',' + str(a['lng']))
            b = urllib.quote(str(b['lat']) + ',' + str(b['lng']))
            url = 'https://maps.googleapis.com/maps/api/directions/json?origin='+a+'&destination='+b+'&sensor=false&language=zh_cn&region=cn'
            req = urllib2.Request(url)
            req = urllib2.urlopen(url)
            req = json.load(req)
            return req

        def get_eat_count(item):
            cnt = 0
            for _ in self.item_classes[0]:
                if dist_latlng(item, _) < 0.5:
                    cnt += 1

            return cnt

        def decodePoly(encode):
            print encode
            res = []
            index = 0
            lat = 0
            lng = 0
            cnt = 0
            while index < len(encode):
                shift = 0
                result = 0
                while index < len(encode):
                    b = ord(encode[index]) - 63
                    index += 1
                    result |= (b & 0x1f) << shift
                    shift += 5
                    if (b < 0x20):
                        break
                dlat =  ~(result >> 1) if (result & 1) != 0  else result >> 1
                lat += dlat;

                shift = 0
                result = 0
                while index < len(encode):
                    b = ord(encode[index]) - 63
                    index += 1
                    result |= (b & 0x1f) << shift
                    shift += 5
                    if (b < 0x20):
                        break
                dlng =  ~(result >> 1) if (result & 1) != 0  else result >> 1
                lng += dlng;
                res.append((lat, lng))
                res = [str(_) for _ in res]
                cnt += 1
                if cnt > 10000: return res
            return res

        def get_time(start_lat, start_lng, end_lat, end_lng):
            url = 'http://openapi.aibang.com/bus/transfer?app_key=f41c8afccc586de03a99c86097e98ccb&city=%E6%AD%A6%E6%B1%89&start_lat='+start_lat+'&start_lng='+start_lng+'&end_lat='+end_lat+'&end_lng='+end_lng
            result = urllib2.urlopen(url)
            xml_root = ET.fromstring(result.read())
            buses = xml_root.find('buses')
            if not buses:
                L = math.sqrt(math.pow(float(start_lat) - float(end_lat), 2) + math.pow(float(start_lng) - float(end_lng), 2))
                if L < 0.02:
                    return {'dist':0, 'time':0, 'foot_dist':0, 'last_foot_dist':0, 'segs':""}
                else :
                    return {'dist':1000000, 'time':1000000, 'foot_dist':10000000, 'last_foot_dist':10000000, 'segs':""}
            dist = buses[0][0].text
            time = buses[0][1].text
            foot_dist = buses[0][2].text
            last_foot_dist = buses[0][3].text
            segments = buses[0][4].findall('segment')
            segs = []
            for seg in segments:
                segs.append({'start_stat':seg[0].text, 'end_stat':seg[1].text, 'line_name':seg[2].text, 'stats':seg[3].text})
            res = {'dist':dist, 'time':time, 'foot_dist':foot_dist, 'last_foot_dist':last_foot_dist, 'segs':segs}
            #print res
            return res

        def getline():
            play = pymongo.Connection('localhost', 27017).oneday.play.find()
            play = [_ for _ in play]
            for i, one in enumerate(play):
                if not item_one_condition(one):continue
                for j, two in enumerate(play):
                    if isSameFlag(one, two):continue
                    if not item_two_condition(two):continue
                    if one['time'] + two['time'] >= 130:
                        print one['name'], '--', two['name'];continue
                    if dist_latlng(one, two) > 5: continue
                    dist_one_two = get_time(str(one['lat']), str(one['lng']), str(two['lat']), str(two['lng']))
                    if int(dist_one_two['time'] > 30): continue
                    for k, three in enumerate(play):
                        if not item_three_condition(three):continue
                        if isSameFlag(one, three) or isSameFlag(two, three):continue
                        flag = 1 if re.findall('咖啡厅|茶馆', one['flag'].encode('utf-8')) else 0
                        flag += 1 if re.findall('咖啡厅|茶馆', two['flag'].encode('utf-8')) else 0
                        flag += 1 if re.findall('咖啡厅|茶馆|酒吧', three['flag'].encode('utf-8')) else 0
                        if (flag > 1):continue
                        if one['time'] + two['time'] + three['time'] > 200:continue
                        dist_one_three = get_time(str(one['lat']), str(one['lng']), str(three['lat']), str(three['lng']))
                        dist_two_three = get_time(str(two['lat']), str(two['lng']), str(three['lat']), str(three['lng']))
                        if dist_latlng(one, three) < dist_latlng(one, two) or dist_latlng(two, three) > 7:continue
                        if int(dist_one_three['dist']) < int(dist_two_three['dist']) or int(dist_two_three['time']) > 50:continue
                        print one['name'], '--',two['name'], '--',\
                                three['name']
            return []

        def getline_for_condition(lat, lng, flag, tag):
            self.item_one_condition = item_one_condition
            self.item_two_condition = item_two_condition
            self.item_three_condition = item_three_condition

            play = pymongo.Connection('localhost', 27017).oneday.play.find()
            play = [_ for _ in play]
            res = get_shortest_item(lat, lng)
            lines = []
            for i, item_one in enumerate(res):
                if not self.item_one_condition(item_one):
                    continue

                for j, item_two in enumerate(play):
                    if isSameFlag(item_one, item_two):
                        continue

                    if not self.item_two_condition(item_two):
                        continue

                    if item_one['time'] + item_two['time'] >= 130:
                        print item_one['name'], '--', item_two['name']
                        map_one = get_map(item_one, item_two)
                        point_one = decodePoly(str(map_one['routes'][0]['overview_polyline']['points']))
                        point_one = ",".join(point_one)

                        lines.append(
                                {
                                    'line':item_one['name'] + ' -- ' + item_two['name'],
                                    'times:':item_one['time'] + item_two['time'],
                                    'point_one':point_one
                                }
                                )
                        continue

                    if dist_latlng(item_one, item_two) > 0.3:
                        continue

                    for k, item_three in enumerate(play):
                        if not self.item_three_condition(item_three):
                            continue
                        if isSameFlag(item_one, item_three) or isSameFlag(item_two, item_three):
                            continue
                        flag = 1 if re.findall('咖啡厅|茶馆', item_one['flag'].encode('utf-8')) else 0
                        flag += 1 if re.findall('咖啡厅|茶馆', item_two['flag'].encode('utf-8')) else 0
                        flag += 1 if re.findall('咖啡厅|茶馆|酒吧', item_three['flag'].encode('utf-8')) else 0
                        if (flag > 1):
                            continue
                        if item_one['time'] + item_two['time'] + item_three['time'] > 200:
                            continue
                        if dist_latlng(item_one, item_three) < dist_latlng(item_one, item_two) or dist_latlng(item_two, item_three) > 0.2:
                            continue

                        print item_one['name'], '--',item_two['name'], '--',\
                                item_three['name']
                        map_one = get_map(item_one, item_two)
                        point_one = decodePoly(str(map_one['routes'][0]['overview_polyline']['points']))
                        point_one = ",".join(point_one)
                        lines.append(
                                {
                                    'line':item_one['name']+ ' -- ' + item_two['name'] + ' -- ' + item_three['name'],
                                    'times:':item_one['time'] + item_two['time'] + item_three['time'],
                                    'point_one':point_one
                                }
                                )
            return json.dumps(lines)

        #return getline_for_condition(lat, lng, flag, tag)
        #return get_time('30.531186', '114.36503', '30.584494', '114.299835')
        return getline()


if __name__ == '__main__':
    line = Line()
    print line.main(0,0,0,0)