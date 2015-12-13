#!/usr/bin/python
# -*- coding: utf8 -*-

import requests
from bs4 import BeautifulSoup as bs

################################type here################################
user = raw_input('student id:')
password = raw_input('password:')
################################type here################################



session1 = requests.session()


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

res = session1.post("https://web2.cc.ntu.edu.tw/p/s/login2/p1.php",headers=header,data=login,cookies=cookie)
res.encoding = 'big5'

reg = session1.get("https://if163.aca.ntu.edu.tw/eportfolio/student/GRC.asp",cookies = requests.utils.dict_from_cookiejar(res.cookies))
reg.encoding = 'big5'


soup = bs(reg.text)
for items in soup.find_all('a',href=True,text="進入修課檢視系統"):
    des = session1.get(items['href'])
des.encoding = 'big5'

soup = bs(des.text)
font = soup.select("tr")

takenCourses =[]

for a in font:
    b = a.findAll("td")
    if len(b) == 9:
        takenCourses.append(b[2].text)
for course in takenCourses:
    print course