#coding=utf-8

try:
    from  application.apps.oneday import getLine
except:
    pass

class ShakeList:
    def __init__(self):
        pass

    def comm(self, items, n = None):
        if n is None:
            n = len(items)
        for i in xrange(len(items)):
            v = items[i:i+1]
            if n == 1:
                yield v
            else:
                for c in self.comm(items[i+1:], n - 1):
                    yield v + c

    def shakelist(self, lat, lng, place, people, transportation, money):
        _place = set(place.split('-'))
        index = 0
        while  index < len(_place) - 3:
            _place.pop()

        _people = set(people.split('-'))
        _money = money.split('-')

        def condition(items):
            s = {
                    'hang out'        : u'逛街'.encode('utf-8'),
                    'art'             : u'文化'.encode('utf-8'),
                    'book'            : u'书'.encode('utf-8'),
                    'nature'          : u'自然'.encode('utf-8'),
                    'humanism'        : u'人文'.encode('utf-8'),
                    'tea'             : u'茶馆'.encode('utf-8'),
                    'park'            : u'公园'.encode('utf-8'),
                    'shower'          : u'按摩/洗浴'.encode('utf-8'),
                    'ktv'             : u'KTV'.encode('utf-8'),
                    'table game'      : u'桌面游戏'.encode('utf-8'),
                    'coffee'          : u'咖啡'.encode('utf-8'),
                    'electrical play' : u'电玩'.encode('utf-8'),
                    'amusement'       : u'游乐游艺'.encode('utf-8'),
                    'billiard'        : u'台球室'.encode('utf-8'),
                    'bar'             : u'酒吧'.encode('utf-8'),
                    'cinema'          : u'电影'.encode('utf-8'),
                }


            cnt = 0
            for p in _place:
                for item in items:
                    if item['flag'].encode('utf-8').find(s[p]) != -1:
                        cnt += 1
            if cnt < 3:
                return 0

            s = {
                    'myself'      : 'single'.encode('utf-8'),
                    'couple'      : 'couple'.encode('utf-8'),
                    'girls'       : 'women'.encode('utf-8'),
                    'boys'        : 'men'.encode('utf-8'),
                    'class party' : 'class'.encode('utf-8')
                }

            cnt = 0
            for p in _people:
                for item in items:
                    if item['tags'].encode('utf-8').find(s[p]) != -1:
                        cnt += 1
            if cnt < 3:
                return 0

            _sum = 0
            for i in items:
                _sum += int(i['money'])

            if _sum < int(_money[0]) or _sum > int(_money[1]):
                return 0

            return 1

        ret = getLine.Line().getline(lat, lng, 0, 1, condition)
        cnt = 0
        while not ret and cnt < 10:
            cnt += 1
            if len(_place) > 0:
                _place.pop
            elif len(_people) > 0:
                _people.pop()
            else:
                _money[0] = '0'
                _money[1] = '10000'
            ret = getLine.Line().getline(lat, lng, 0, 1, condition)
        return ret

    def test(self):
        for i in self.comm([i + 1 for i in xrange(5)], 4):
            print i
            pass

if __name__ == "__main__":
    ShakeList().test()
