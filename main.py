from operator import itemgetter
import Course
import State
from gui_main import *
from util import *
from initial import *
from login import *

#======== Preparing and parsing data =======
class_stars,teacher_stars = readStars()
courses = readSweetList(class_stars,teacher_stars)

#======== Login, init states ========
gui = GUI()
gui.initVar()
gui.createTable()

#bi_show, fu_shuan_bi_show = gui.bi_show, gui.fu_shuan_bi_show
#takenCourses = Login(user, password)

#======== State Algorithm ======
EmptyState = State.State()
print EmptyState.free

print max([(course.getAverageSweet(),course.name) for course in courses],key=itemgetter(0))[1]
print max([(course.getAverageSweet(),course.teacher) for course in courses],key=itemgetter(0))[1]

'''
nextState = EmptyState.generateSuccessor(courses[0])
print nextState.canTake(courses[0])
'''