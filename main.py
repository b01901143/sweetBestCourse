from operator import itemgetter

import Course
import State
from util import *

#======== Preparing and parsing data =======
class_stars,teacher_stars = readStars()
courses = readSweetList(class_stars,teacher_stars)

#======== State Algorithm ======
EmptyState = State.State()
print EmptyState.free

print max([(course.getAverageSweet(),course.name) for course in courses],key=itemgetter(0))[1]
print max([(course.getAverageSweet(),course.teacher) for course in courses],key=itemgetter(0))[1]

'''
nextState = EmptyState.generateSuccessor(courses[0])
print nextState.canTake(courses[0])
'''