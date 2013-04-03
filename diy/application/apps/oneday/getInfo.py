#coding=utf-8

import urllib2
import urllib
import sys
import requests
import re

reload(sys)
sys.setdefaultencoding('utf-8')

def getInfo(name):
    url = 'http://www.dianping.com/search/keyword/16/0_' + urllib.quote(name)
    content = requests.get(url).content
    shopId = re.findall('shopIDs:\t\[(.*)\],\r', content)[0].split(',')

    url = 'http://www.dianping.com/shop/' + shopId[0]
    content = requests.get(url).content
    pattern = 'span class="J_full-cont">(.*)</span>\r'
    intra = re.findall(pattern, content)
    if len(intra) != 0:
        intra = intra[0].encode('utf-8')
    else:
        intra = "no"

    pattern = 'span class="J_full-cont Hide">([0-9/]*)'
    bus = re.findall(pattern, content)
    if len(bus) != 0:
        bus = bus[0]
    else:
        bus = "no bus"

    url = 'http://www.dianping.com/shop/'+ shopId[0] +'/photos'
    pattern = 'http://i[0-9].s[0-9].dpfile.com/pc/[0-9a-z()]*/thumb.jpg'
    content = requests.get(url).content
    img = re.findall(pattern ,content)

    ret = {
            'img':img,
            'intra':intra,
            'bus':bus
            }
    return ret

if __name__ == "__main__":
    print getInfo("光谷美食")
