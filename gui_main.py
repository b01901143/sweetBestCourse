#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os   
import collections
import Tkinter as tkinter
from tktable import *
from initial import *
from login import *
from util import *

class GUI:
    def __init__(self):
        self.bi_show = []
        self.fu_shuan_bi_show = []
        self.class_time = []
        self.current_state = []

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
        self.takenCourses = Login(self.user_field.get(), self.pswd_field.get())
        self.b_show.append(self.fu_shuan_bi_show[0])
        self.to_show = [course for course in self.bi_show if course not in self.takenCourses]
        self.updateBishow2Table(self.to_show)
        
    def updateBishow2Table(self, bi_show):
        for item in bi_show:
            for time in sweety_dict[item][0][4].split(" ")[ :-1]:
                self.current_state.append(sweety_dict[item])
                self.updateTable([time, item])

    def updateTable(self, time):
        index = "%i,%i" % (int(time[0][1]), (int(ord(time[0][0])-65)))
        value = time[1]
        self.var[index] = time[1]
        
    def loadMethod(self):
        print "Loading..."

    def searchMethod(self):
        print "Searching..."

    def createTable(self):
        self.user_label = tkinter.Label(self.root, text="帳號：")
        self.user_label.grid(row=0, column=0)
        self.user_field = tkinter.Entry(self.root, width=10)
        self.user_field.grid(row=0, column=1)
    
        self.pswd_label = tkinter.Label(self.root, text="密碼：")
        self.pswd_label.grid(row=1, column=0)
        self.pswd_field = tkinter.Entry(self.root, width=10, show="*")
        self.pswd_field.grid(row=1, column=1)

        self.grade_label = tkinter.Label(self.root, text="年級：")
        self.grade_label.grid(row=2, column=0)
        self.grade_field = tkinter.Entry(self.root, width=10)
        self.grade_field.grid(row=2, column=1)
        
        self.login_button = tkinter.Button(self.root, text="登入", command=self.loginMethod)
        self.login_button.grid(row=5, column=0)
    
        self.quit_button = tkinter.Button(self.root, text="離開", command=self.root.destroy)
        self.quit_button.grid(row=5, column=1)
    
        self.load_label = tkinter.Label(self.root, text="要帶入的課程：")
        self.load_label.grid(row=3, column=0)
        self.load_field = tkinter.Entry(self.root, width=15)
        self.load_field.grid(row=3, column=1)
        self.load_button = tkinter.Button(self.root, text="帶入", command=self.loadMethod)
        self.load_button.grid(row=3, column=2)
    
        self.search_button = tkinter.Button(self.root, text="搜尋最佳課程", command=self.searchMethod)
        self.search_button["width"] = 20
        self.search_button.grid(row=4, column=0, columnspan=3)
        
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
        self.test.grid(row=0, column=3, rowspan=10)
        self.test.tag_configure('sel', background='yellow')
        self.test.tag_configure('active', background='blue')
        self.test.tag_configure('title', anchor='w', bg='red', relief='sunken')
        self.root.mainloop()


