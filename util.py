#!/usr/bin/python
# -*- coding: utf8 -*-

import csv
import cPickle

import Course
import State

sweety_list = "Data/sweety_list.csv"
NTUcourse = "Data/NTUcourse_stars.pkl"
EEComment = "Data/EE_comment_stars.pkl"

def readSweetList(class_stars, teacher_stars):
	c_count = 0
	total_c_stars = 0
	t_count = 0
	total_t_stars = 0
	with open(sweety_list, 'rb') as fh:
		courses = []
		data = csv.reader(fh, delimiter=',')
		for line in data:
			#classification = classify(line[0])
			newC = Course.Course(line[0],line[1],[l for l in line[5].split(' ') if l != '']\
								,line[2],[int(s) for s in line[8:]],line[4]) 
			courses.append(newC)
			if line[0] in class_stars:
				newC.setClassStars( class_stars[line[0]] )
				c_count+=1
				total_c_stars+=class_stars[line[0]]
			if line[1] in teacher_stars:
				newC.setTeacherStars( teacher_stars[line[1]] )
				t_count+=1
				total_t_stars+=teacher_stars[line[1]]
			general = line[7].split('A')
			if len(general)>1:
				try:
					general_num = int(general[1][0])
					if general_num in range(1,9):
						newC.setCategory(general_num)
						print newC
						general_num = int(general[1][1])
						if general_num in range(1,9):
							newC.setCategory(general_num)
							print newC
							general_num = int(general[1][2])
				except:
					continue
	fh.close()
	aver_c_stars = total_c_stars/float(c_count)
	aver_t_stars = total_t_stars/float(t_count)
	for course in courses:
		if course.class_stars == None:
			course.class_stars = aver_c_stars
		if course.teacher_stars == None:
			course.teacher_stars = aver_t_stars
	return courses

def readStars():
	fh = open(NTUcourse,'rb')
	teacher_stars,class_stars,teacher_classes,class_teachers = cPickle.load(fh)
	fh.close()
	return class_stars,teacher_stars

#def classify(name):

def readSweetyCsv():
	sweety_dict = dict()
	with open ("Data/sweety_list.csv", 'r') as f :
		for line in f :
			info = line.split(',')
			course_name = info[0].decode('utf-8')
			#print course_name
			#teacher = info[1]
			#credit = info[2]
			#class_for = info[3]
			#class_num = info[4]
			#class_time= info[5]
			#people_num= info[6]
			#remark = info[7]
			#F = info[8]
			#Cm = info[9]
			#C  = info[10]
			#Cp = info[11]
			#Bm = info[12]
			#B  = info[13]
			#Bp = info[14]
			#Am = info[15]
			#A  = info[16]
			#Ap = info[17]
			if course_name not in sweety_dict:
				sweety_dict[course_name] = [info[1:]]
			else:
				sweety_dict[course_name].append(info[1:])
	return sweety_dict

def checkRuleOut( courses, course, distrib, rule_out):
	if "PE" in course.ID:
		if distrib[4] <= 1:
			distrib[4] = 0
			for c in courses:
				if c!= course and "PE" in c.ID:
					print c.name
					rule_out.add(c)
		else:
			distrib[4] -= 1
	return distrib
