from operator import itemgetter

import Course
import State
from util import *

credit_limit = 25

#======== Preparing and parsing data =======
class_stars,teacher_stars = readStars()
courses = readSweetList(class_stars,teacher_stars)

#======== State Algorithm ======
EmptyState = State.State()

#======== +bi show Initial State ======
InitialState = EmptyState

#Greedy Algorithm
(nextState,score,class_stars,GPA) = max([(InitialState.generateSuccessor(course,credit_limit),\
				(course.class_stars/5.0*3.66)+course.GPA,course.class_stars,course.GPA)\
				for course in courses if InitialState.generateSuccessor(course,credit_limit) != None],key=itemgetter(1))
print nextState
print score
print class_stars
print GPA

while True:
	try:
		(nextState,score,class_stars,GPA) = max([(nextState.generateSuccessor(course,credit_limit),\
				(course.class_stars/5.0*3.66)+course.GPA,course.class_stars,course.GPA)\
				for course in courses if nextState.generateSuccessor(course,credit_limit) != None],key=itemgetter(1))
		print nextState
		print score
		print class_stars
		print GPA
	except:
		print "Greedy finished!!!"
		break




'''
nextState = max([EmptyState.generateSuccessor(courses[0]),course.])
if nextState:
	print nextState.free, nextState.credit
else:
	print nextState
'''