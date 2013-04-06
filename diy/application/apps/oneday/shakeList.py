#coding=utf-8

from  application.apps.oneday import getLine

place=''
transportation=''
money=''
people=''

class ShakeList:
    def __init__(self):
        pass

    def shakelist(self, lat, lng, _place, _people, _transportation, _money):
        global place
        global transportation
        global money
        global people
        place = _place
        transportation = _transportation
        money = _money
        people = _people

        def condition(items):
            global place
            global transportation
            global money
            global people
            s = {
                    'movie': u'电影'.encode('utf-8'),
                    'ktv': 'KTV'.encode('utf-8'),
                    'table game': u'台球'.encode('utf-8'),
                    'coffee shop': u'咖啡'.encode('utf-8'),
                    'bar': u'酒吧'.encode('utf-8'),
                    'tea house': u'茶'.encode('utf-8'),
                    'attractions': '',
                    'book shop': u'书'.encode('utf-8')
                    }

            _place = place.split('-')
            for p in _place:
                flag = 0
                for item in items:
                    if item['flag'].encode('utf-8').find(s[p]) != -1:
                        flag = 1
                        break
                if not flag:
                    return 0

            s = {
                    'myself':'single'.encode('utf-8'),
                    'couple':'couple'.encode('utf-8'),
                    'girls':'women'.encode('utf-8'),
                    'boys':'men'.encode('utf-8'),
                    'class party':'class'.encode('utf-8')
                    }

            _people = people.split('-')
            for p in _people:
                flag = 0
                for item in items:
                    if item['tags'].encode('utf-8').find(s[p]) != -1:
                        flag = 1
                        break
                if not flag:
                    return 0

            _sum = 0
            _money = money.split('-')
            for i in items:
                _sum += int(i['money'])

            if _sum < int(_money[0]) or _sum > int(_money[1]):
                return 0

            return 1

        return getLine.Line().getline(lat, lng, 0, 1, condition)
