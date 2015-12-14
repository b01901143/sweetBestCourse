import csv

sweety_dict = dict()
def readSweetyCsv():
	with open ("sweety_list.csv", 'r') as f :
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

readSweetyCsv()