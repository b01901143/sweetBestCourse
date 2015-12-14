import requests
import ssl
import csv
import os
from time import sleep
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
class MyAdapter(HTTPAdapter):
     def init_poolmanager(self, connections, maxsize, block=False):
         self.poolmanager = PoolManager(num_pools=connections,
                                        maxsize=maxsize,
                                        block=block,
                                        ssl_version=ssl.PROTOCOL_TLSv1)
def output_course_list():
    print "Writing course list ..."
    try :
        os.remove("sweety_list.csv")    
    except :
        print "create new csv"
    for i in range(len(courses)):
        with open("sweety_list.csv", 'a') as clist:
            fieldnames = ["Class name","Teacher","Credits","Class for","Class Number","Time","Limitation",\
                          "Remark","F","Cm","C","Cp","Bm","B","Bp","Am","A","Ap"]
            writer = csv.DictWriter(clist, fieldnames = fieldnames)
            #if(i == 0):
            #    writer.writerow({"Serial num":"Serial num","Designed for":"Designed for","Class no":"Class no","Class":"Class","Title":"Title","Credits":"Credits","ID":"ID",\
            #             "Year":"Year","Required/Elective":"Required/Elective","Instructor":"Instructor","Selection method":"Selection method","Schedule & room":"Schedule & room","Limit of students":"Limit of students",\
            #             "Limit of course":"Limit of course","Remark":"Remark","Website":"Website","Join":"Join"})
            writer.writerow({"Class name": courses[i][0], "Teacher": courses[i][1], "Credits": courses[i][2], "Class for": courses[i][3], \
                             "Class Number":courses[i][4], "Time": courses[i][5], "Limitation": courses[i][6], "Remark": courses[i][7], "F": courses[i][8],\
                             "Cm": courses[i][9], "C": courses[i][10], "Cp": courses[i][11], "Bm": courses[i][12], "B": courses[i][13], \
                             "Bp": courses[i][14], "Am": courses[i][15], "A": courses[i][16], "Ap": courses[i][17]})   

course_list = []        
s = requests.Session()
s.mount('https://', MyAdapter())
for index in range(602):
    if index % 100 == 0:
        sleep(5)
    #req = s.get("http://ntusweety.herokuapp.com/search?m=0&m=1&m=2&m=3&m=4&m=5&m=6&m=7&m=8&m=9&m=10&m=A&m=B&m=C&m=D&t=0&t=1&t=2&t=3&t=4&t=5&t=6&t=7&t=8&t=9&t=10&t=A&t=B&t=C&t=D&w=0&w=1&w=2&w=3&w=4&w=5&w=6&w=7&w=8&w=9&w=10&w=A&w=B&w=C&w=D&h=0&h=1&h=2&h=3&h=4&h=5&h=6&h=7&h=8&h=9&h=10&h=A&h=B&h=C&h=D&f=0&f=1&f=2&f=3&f=4&f=5&f=6&f=7&f=8&f=9&f=10&f=A&f=B&f=C&f=D&s=0&s=1&s=2&s=3&s=4&s=5&s=6&s=7&s=8&s=9&s=10&s=A&s=B&s=C&s=D&sem=104-1&faculty=&depart=&Acourse=A8&name=&teacher=")
    req = s.get("http://ntusweety.herokuapp.com/search?m=0&m=1&m=2&m=3&m=4&m=5&m=6&m=7&m=8&m=9&m=10&m=A&m=B&m=C&m=D&t=0&t=1&t=2&t=3&t=4&t=5&t=6&t=7&t=8&t=9&t=10&t=A&t=B&t=C&t=D&w=0&w=1&w=2&w=3&w=4&w=5&w=6&w=7&w=8&w=9&w=10&w=A&w=B&w=C&w=D&h=0&h=1&h=2&h=3&h=4&h=5&h=6&h=7&h=8&h=9&h=10&h=A&h=B&h=C&h=D&f=0&f=1&f=2&f=3&f=4&f=5&f=6&f=7&f=8&f=9&f=10&f=A&f=B&f=C&f=D&s=0&s=1&s=2&s=3&s=4&s=5&s=6&s=7&s=8&s=9&s=10&s=A&s=B&s=C&s=D&sem=104-1&faculty=&depart=&name=&teacher=&page=%i" % index)
    data = req.text
    soup = BeautifulSoup(data, "html.parser")
    for course in soup.find_all('tr', class_="data"):
        course_info = []
        course_info.append(course.find_all('a', href=True)[0]['href'])
        info = course.select('td')
        classtime = ""
        try :
            classtime = [info[11].text.encode('utf-8').split("(")[0]]
            if info[11].text.encode('utf-8').split("(")[1].split(")")[1] != "":
                classtime += [info[11].text.encode('utf-8').split("(")[1].split(")")[1]]
        except:
            pass
        classtimes = ""
        for time in classtime:
            try:
                if time[1] == " ":
                    time = time[2:]
                elif time[0] == " ":
                    time = time[1:]
                #print time
            
                hours = time[3:].split(',')
                for hour in hours:
                    if ord(time[0:3].decode('utf-8')) == 19968:
                        classtimes += "A" + hour + " "
                    elif ord(time[0:3].decode('utf-8')) == 20108:
                        classtimes += "B" + hour + " "
                    elif ord(time[0:3].decode('utf-8')) == 19977:
                        classtimes += "C" + hour + " "
                    elif ord(time[0:3].decode('utf-8')) == 22235:
                        classtimes += "D" + hour + " "
                    elif ord(time[0:3].decode('utf-8')) == 20116:
                        classtimes += "E" + hour + " "
                    elif ord(time[0:3].decode('utf-8')) == 20845:
                        classtimes += "F" + hour + " "
            except:
                pass
            
        course_info += [info[4].text.encode('utf-8'), info[9].text.encode('utf-8'), info[5].text.encode('utf-8'), info[1].text.encode('utf-8'),   \
                        info[2].text.encode('utf-8'), classtimes, info[13].text.encode('utf-8'), info[14].text.encode('utf-8')]
        course_list.append(course_info)
courses = []
counter = 0
for course in course_list:
    counter += 1
    if counter % 100 == 0:
        sleep(5)
    req = s.get("http://ntusweety.herokuapp.com%s" %course[0])
    data = req.text
    soup = BeautifulSoup(data, "html.parser")
    if soup.find('h2').text != "":
        course += [0]*10 
        courses.append(course[1:])
        continue
    semester = soup.select('.item')
    course_info = course[1:]
    for j in range(len(semester)):
        gpa = semester[j].select('td')
        if j == 0:
            for i in range(2,len(gpa)):
                if gpa[1].text.encode('utf-8') == course[2]:    
                    course_info.append(int(gpa[i].text))
                else:
                    course_info.append(0)
        else:
            for i in range(2,len(gpa)):
                if gpa[1].text.encode('utf-8') == course[2]:
                    course_info[6+i] += int(gpa[i].text)
                else:
                    course_info[6+i] += 0
    courses.append(course_info)


output_course_list()

    