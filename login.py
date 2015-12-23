#!/usr/bin/python
# -*- coding: utf8 -*-

import requests
from bs4 import BeautifulSoup as bs
from requests.adapters import HTTPAdapter
import ssl
from requests.packages.urllib3.poolmanager import PoolManager
class MyAdapter(HTTPAdapter):
     def init_poolmanager(self, connections, maxsize, block=False):
         self.poolmanager = PoolManager(num_pools=connections,
                                        maxsize=maxsize,
                                        block=block,
                                        ssl_version=ssl.PROTOCOL_TLSv1)

def Login(user, password):
#def Login():
    ################################type here################################
    #user = raw_input('student id:')
    #password = raw_input('password:')
    ################################type here################################
    
    
    
    session1 = requests.session()
    session1.mount('https://', MyAdapter())
    
    pre = session1.get("https://if163.aca.ntu.edu.tw/eportfolio/login.asp")
    
    pre = session1.get("https://web2.cc.ntu.edu.tw/p/s/login2/p1.php")
    cookie =  requests.utils.dict_from_cookiejar(pre.cookies)
    
    
    header = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-TW,zh;q=0.8,en;q=0.6',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Content-Length':'51',
    'Content-Type':'application/x-www-form-urlencoded',
    'Host':'web2.cc.ntu.edu.tw',
    'Origin':'https://web2.cc.ntu.edu.tw',
    'Referer':'https://web2.cc.ntu.edu.tw/p/s/login2/p1.php',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'
    }
    
    
    login = { 
    'Submit':"%E7%99%BB%E5%85%A5"
    }
    
    login['user'] = user
    login['pass'] = password
    
    res = session1.post("https://web2.cc.ntu.edu.tw/p/s/login2/p1.php",data=login,cookies=cookie,headers=header)
    res.encoding = 'big5'
    
    reg = session1.get("https://if163.aca.ntu.edu.tw/eportfolio/student/GRC.asp",cookies = requests.utils.dict_from_cookiejar(res.cookies))
    reg.encoding = 'big5'
    
    
    soup = bs(reg.text, "html.parser")
    for items in soup.find_all('a',href=True,text="進入修課檢視系統"):
        des = session1.get(items['href'])
    des.encoding = 'big5'
    
    soup = bs(des.text, "html.parser")
    font = soup.select("tr")

    takenCourses =[]
    neccessaries = dict()
    
    for a in font:
        b = a.findAll("td")
        if len(b) == 1:
            if b[0].text[4:10] == '      ' and not b[0].text[10] == ' ': #text[4~9]
                neccessaries['指定選修'] = int(b[0].text[37:39])
                neccessaries['一般選修'] = int(b[0].text[48:50])
                neccessaries['通識'] = int(b[0].text[56:58])

        if len(b) == 9:
            if b[7].text == u' 未到 ' or b[7].text ==' F ' or  b[7].text == u' 停修 ':
                continue
            update(neccessaries,b)
            c = b[2].text
            c = c.split(" ")[0]
            takenCourses.append(c.encode('utf8'))

    for name in neccessaries:
        print name , neccessaries[name]
    
    #return takenCourses=(ID or 課名＋老師名), neccesaries=[系必(學分),系選,選修,通識,體育]
    return takenCourses,neccessaries

def update(nes , b):
    if b[0].text[1:3] == u'通識':
        nes['通識'] -= int(b[6].text)
    elif b[0].text[1:3] == u'選修' and b[8].text == u' 可當指定選修 ' and nes['指定選修']>0:
        nes['指定選修'] -= int(b[6].text)
    elif b[0].text[1:3] == u'選修':
        nes['一般選修'] -= int(b[6].text)
    for name in nes:
        if nes[name]<0:
            nes[name]=0
#p = Login("b01901143","s2264")
    
