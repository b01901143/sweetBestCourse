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
			newC = Course.Course(line[0],line[1],[l for l in line[5].split(' ') if l != '']\
								,line[2],[int(s) for s in line[8:]]) 
			courses.append(newC)
			if line[0] in class_stars:
				newC.setClassStars( class_stars[line[0]] )
				c_count+=1
				total_c_stars+=class_stars[line[0]]
			if line[1] in teacher_stars:
				newC.setTeacherStars( teacher_stars[line[1]] )
				t_count+=1
				total_t_stars+=teacher_stars[line[1]]
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
