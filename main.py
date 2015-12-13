import Course
import State

from util import *

#======== Preparing and parsing data =======
class_stars,teacher_stars = readStars()
courses = readSweetList(class_stars,teacher_stars)

#
EmptyState = State.State()
print EmptyState.free
nextState = EmptyState.generateSuccessor(courses[0])
print nextState.canTake(courses[0])