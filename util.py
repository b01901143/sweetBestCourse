import csv
import cPickle

import Course
import State

sweety_list = "Data/sweety_list.csv"
NTUcourse = "Data/NTUcourse_stars.pkl"
EEComment = "Data/EE_comment_stars.pkl"

def readSweetList(class_stars, teacher_stars):
	with open(sweety_list, 'rb') as fh:
		courses = []
		data = csv.reader(fh, delimiter=',')
		for line in data:
			newC = Course.Course(line[0],line[1],line[5],line[2],[int(s) for s in line[8:]]) 
			courses.append(newC)
			if line[0] in class_stars:
				newC.setClassStars(class_stars[line[0]])
			if line[1] in teacher_stars:
				newC.setTeacherStars(teacher_stars[line[1]])
	fh.close()
	return courses

def readStars():
	fh = open(NTUcourse,'rb')
	teacher_stars,class_stars,teacher_classes,class_teachers = cPickle.load(fh)
	fh.close()
	return class_stars,teacher_stars
