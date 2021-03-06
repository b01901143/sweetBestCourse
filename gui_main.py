#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os   
import collections
import Tkinter as tkinter
from tktable import *
from initial import *
from login import *
from util import *
import State
import Course
from operator import itemgetter
import pdb

class GUI:
    def __init__(self):
        self.bi_show = []
        self.fu_shuan_bi_show = []
        self.class_time = []
        self.current_state = []
        self.courses, self.general_courses, self.PE_courses = readCoursePickle()
        self.EmptyState = State.State()
        self.InitialState = State.State()
        self.InitialState.setPersonDepart("EE") #for testing
        self.credit_limit = 25
        self.total_score = 1
        
    def test_cmd(self, event):
        if event.i == 0:
            return '%i, %i' % (event.r, event.c)
        else:
            return 'set'

    def browsecmd(self, event):
        print("event:", event.__dict__)
        print("curselection:", self.test.curselection())
        print("active cell index:", self.test.index('active'))
        print("active:", self.test.index('active', 'row'))
        print("anchor:", self.test.index('anchor', 'row'))
        b_index = self.test.index('active')
        course_name = self.var[b_index]
        for i in range(len(self.current_state)):
            if course_name == self.current_state[i][0]:
                self.current_state.pop(i)
                break
        for x in range(0,6):
            for y in range(0,15):
                index = "%i,%i" % (y, x)
                try:
                    if course_name == self.var[index]:
                        self.var[index] = ""
                except:
                    pass
        
    def initVar(self):
        self.root = tkinter.Tk()
        self.var = ArrayVar(self.root)
        for y in range(-1, 15):
            index = "%i,%i" % (y, -1)
            self.var[index] = index
            if y == -1:
                self.var[index] = ""
            elif 0 <= y <= 10:
                self.var[index] = y
            else:
                self.var[index] = chr(54+y)
        for x in range(-1,6):
            index = "%i,%i" % (-1, x)
            self.var[index] = index
            if x == -1:  self.var[index] = ""
            elif x == 0: self.var[index] = "ㄧ"
            elif x == 1: self.var[index] = "二"
            elif x == 2: self.var[index] = "三"
            elif x == 3: self.var[index] = "四"
            elif x == 4: self.var[index] = "五"
            elif x == 5: self.var[index] = "六"
           
    def loginMethod(self):
        print "Logging..."
        self.bi_show, self.fu_shuan_bi_show = Initial(self.user_field.get(), self.grade_field.get())
        self.takenCourses,self.toGraduate = Login(self.user_field.get(), self.pswd_field.get())
        self.ruleOutTaken()
        self.InitialState.setPersonDepart("EE")
        for to in self.toGraduate:
            print to
        #self.bi_show.append(self.fu_shuan_bi_show[0])通識
        #self.to_show = [course for course in self.bi_show if course not in self.takenCourses]
        #self.updateBishow2Table(self.to_show)
        
    def updateBishow2Table(self, bi_show):
        sweety_dict = readSweetyCsv()
        for item in bi_show:
            for time in sweety_dict[item][0][4].split(" ")[ :-1]:
                self.current_state.append(sweety_dict[item])
                self.updateTable([time, item])

    def updateTable(self, time):
        #time[0] = time ,time[0][1]=class time,time[0][0]=weekdays
        #time[1] = course name
        index = "%i,%i" % (int(time[0][1]), (int(ord(time[0][0])-65)))
        value = time[1]
        self.var[index] = time[1]
        
    def loadMethod(self):
        print "Loading..."

    def searchMethod(self):
        (nextState,score,class_stars,GPA,course) = max([(self.InitialState.generateSuccessor(course,self.credit_limit),\
                    (course.class_stars/5.0*3.66)+course.GPA,course.class_stars,course.GPA,course)\
                    for course in self.courses if self.InitialState.generateSuccessor(course,self.credit_limit) != None],key=itemgetter(1))
        print nextState.distrib, nextState.rule_out
        nextState.distrib = checkRuleOut(self.courses, course, nextState.distrib, nextState.rule_out)
        print nextState.distrib, nextState.rule_out
        while True:
            try:
                (nextState,score,class_stars,GPA,course) = max([(nextState.generateSuccessor(course,self.credit_limit),\
                        (course.class_stars/5.0*3.66)+course.GPA,course.class_stars,course.GPA,course)\
                        for course in self.courses if nextState.generateSuccessor(course,self.credit_limit) != None],key=itemgetter(1))
                print nextState.distrib, nextState.rule_out
                nextState.distrib = checkRuleOut(self.courses, course, nextState.distrib, nextState.rule_out)
                print nextState.distrib, nextState.rule_out
                for c in nextState.taken:
                    for t in c.time:
                        index = "%i,%i" % (int(t[1]), (int(ord(t[0])-65)))
                        self.var[index] = c.name
            except:
                print "Greedy finished!!!"
                break

    def updateScore(self):
        self.total_score = int(self.shibi_spin.get()) + int(self.shish_spin.get()) + \
                           int(self.shush_spin.get()) + int(self.tonsh_spin.get()) + int(self.sport_spin.get())
        self.shibi_spin.config(to=(40-self.total_score))
        self.shish_spin.config(to=(40-self.total_score))
        self.shush_spin.config(to=(40-self.total_score))
        self.tonsh_spin.config(to=(40-self.total_score))
        self.sport_spin.config(to=(40-self.total_score))
        if self.total_score >= 20:
            self.shibi_spin.config(to=self.shibi_spin.get())
            self.shish_spin.config(to=self.shish_spin.get())
            self.shush_spin.config(to=self.shush_spin.get())
            self.tonsh_spin.config(to=self.tonsh_spin.get())
            self.sport_spin.config(to=self.sport_spin.get())
        self.score_label.config(text="能力點數：%i" % (20-self.total_score))
        print self.total_score

    def ruleOutTaken(self):
        flag=0
        for taken in self.takenCourses:
            for c in self.courses:
                if str(taken)==c.name:
                    print c
                    self.courses.remove(c)
                    flag=1
                    break
            if flag==1:
                continue
            for c in self.general_courses:
                if str(taken)==c.name:
                    print c
                    self.general_courses.remove(c)
                    flag=1
                    break
            if flag==1:
                continue
            for c in self.PE_courses:
                if str(taken)==c.name:
                    print c
                    self.PE_courses.remove(c)
                    flag=1
                    break
            if flag==1:
                continue
            else:
                print "Can't find"

    def createTable(self):
        self.user_label = tkinter.Label(self.root, text="帳號：")
        self.user_label.grid(row=0, column=0)
        self.user_field = tkinter.Entry(self.root, width=15)
        self.user_field.grid(row=0, column=1, columnspan=3)
    
        self.pswd_label = tkinter.Label(self.root, text="密碼：")
        self.pswd_label.grid(row=1, column=0)
        self.pswd_field = tkinter.Entry(self.root, width=15, show="*")
        self.pswd_field.grid(row=1, column=1, columnspan=3)

        self.grade_label = tkinter.Label(self.root, text="年級：")
        self.grade_label.grid(row=2, column=0)
        self.grade_field = tkinter.Entry(self.root, width=15)
        self.grade_field.grid(row=2, column=1, columnspan=3)

        self.load_label = tkinter.Label(self.root, text="帶入課程：")
        self.load_label.grid(row=3, column=0)
        self.load_field = tkinter.Entry(self.root, width=20)
        self.load_field.grid(row=3, column=1, columnspan=3)
        self.load_button = tkinter.Button(self.root, text="帶入", command=self.loadMethod)
        self.load_button.grid(row=3, column=4)

        self.shibi_label = tkinter.Label(self.root, text="系必")
        self.shibi_label.grid(row=4, column=0)
        self.shibi_spin = tkinter.Spinbox(self.root, from_=0, to=self.total_score, command=self.updateScore, width=4)
        self.shibi_spin.grid(row=5, column=0)

        self.shish_label = tkinter.Label(self.root, text="系選")
        self.shish_label.grid(row=4, column=1)
        self.shish_spin = tkinter.Spinbox(self.root, from_=0, to=self.total_score, command=self.updateScore, width=4)
        self.shish_spin.grid(row=5, column=1)

        self.shush_label = tkinter.Label(self.root, text="選修")
        self.shush_label.grid(row=4, column=2)
        self.shush_spin = tkinter.Spinbox(self.root, from_=0, to=self.total_score, command=self.updateScore, width=4)
        self.shush_spin.grid(row=5, column=2)

        self.tonsh_label = tkinter.Label(self.root, text="通識")
        self.tonsh_label.grid(row=4, column=3)
        self.tonsh_spin = tkinter.Spinbox(self.root, from_=0, to=self.total_score, command=self.updateScore, width=4)
        self.tonsh_spin.grid(row=5, column=3)

        self.sport_label = tkinter.Label(self.root, text="體育")
        self.sport_label.grid(row=4, column=4)
        self.sport_spin = tkinter.Spinbox(self.root, from_=0, to=self.total_score, command=self.updateScore, width=4)
        self.sport_spin.grid(row=5, column=4)
        
        self.score_label = tkinter.Label(self.root, text="能力點數：%i" % (21-self.total_score))
        self.score_label.grid(row=6, column=0, columnspan=2)
        
        self.search_button = tkinter.Button(self.root, text="搜尋最佳課程", command=self.searchMethod)
        self.search_button["width"] = 20
        self.search_button.grid(row=6, column=2, columnspan=3)
        
        self.login_button = tkinter.Button(self.root, text="登入", command=self.loginMethod)
        self.login_button.grid(row=7, column=1)
    
        self.quit_button = tkinter.Button(self.root, text="離開", command=self.root.destroy)
        self.quit_button.grid(row=7, column=3)
    

        self.test = Table(self.root,
                     rows=16,
                     cols=7,
                     state='disabled',
                     width=200,
                     height=100,
                     titlerows=1,
                     titlecols=1,
                     roworigin=-1,
                     colorigin=-1,
                     selectmode='browse',
                     selecttype='row',
                     rowstretch='unset',
                     colstretch='last',
                     browsecmd=self.browsecmd,
                     flashmode='on',
                     variable=self.var,
                     usecommand=0,
                     command=self.test_cmd)
        self.test.grid(row=0, column=5, rowspan=20)
        self.test.tag_configure('sel', background='yellow')
        self.test.tag_configure('active', background='blue')
        self.test.tag_configure('title', anchor='w', bg='red', relief='sunken')
        self.root.mainloop()

gui = GUI()
gui.initVar()
gui.createTable()
