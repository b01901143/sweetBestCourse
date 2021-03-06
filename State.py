#!/usr/bin/python
# -*- coding: utf8 -*-

import Course

class State:
  def __init__( self, prevState = None ):
    if prevState != None :
      self.taken = set(prevState.taken) #set of course taken (type = Course)
      self.free = set(prevState.free)	#set of free time slot
      self.credit = prevState.credit
      #[shibi,shishuan,shuanshow,general,PE]
      self.distrib = prevState.distrib
      self.rule_out = prevState.rule_out
      self.personDepart = prevState.personDepart
      """
      Mon  Tues Wed  Thur Fri  Sat  Sun
      A0   B0   C0   D0   E0   F0   G0
      .    .    .    .    .    .    .
      .    .    .    .    .    .    .
      .    .    .    .    .    .    .
      A5   B5   C5   D5   E5   F5   G5
      .    .    .    .    .    .    .
      .    .    .    .    .    .    .
      .    .    .    .    .    .    .
      A14  B14  C14  D14  E14  F14  G14
      """
    else:
      self.taken = set()
      self.free = set()
      self.credit = 0
      dayList = ['A','B','C','D','E','F','G']
      for day in dayList:
        for i in range(0,15):
          self.free.add(day+str(i))
      self.distrib = [4,4,4,4,1]
      self.rule_out = set()
      self.personDepart = "None"

  def __eq__( self , other ):
  	return self.taken == other.taken

  def __str__( self ):
    a = ""
    dayList = ['A','B','C','D','E','F','G']
    for i in range(0,15):
      for day in dayList:
        if day+str(i) not in self.free:
          a += day+str(i)+"  "
          if i<10: a += " "
        else : 
          a += "□    "
      a += "\n"
    a += "                           " + str(self.credit) + "學分"
    return a


  def __hash__( self ):
    return hash(self.taken)

  def canTake( self , course ):
    for time in course.getTime():
      if time not in self.free:
        return False
    return True

  def generateSuccessor( self , course ,credit_limit):
    if course.credit == 0 or course in self.rule_out:
      return None
    if not self.canTake(course) or self.credit+course.credit>credit_limit:
      #raise Exception("Cannot take course "+str(course))
      return None
    state = State(self)
    for time in course.getTime():
      state.free.remove(time)
    state.taken.add(course)
    state.credit += course.credit
    return state

  def setPersonDepart( self,department ):
    self.personDepart = department

  def setPersonDistrib( self, distrib):
    self.distrib = distrib



