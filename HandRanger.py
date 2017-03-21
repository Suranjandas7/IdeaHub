#Make and Save Poker Hand Ranges
#using numpy and matplotlib

import numpy as np
import matplotlib.pyplot as plt

back_board = np.zeros(shape = (13,13), dtype = 'int')

class range_maker(object):
	def __init__(self, name):
		#loads data from data.dat to numpy 2-d array back_board
		self.range = np.zeros(shape = (13,13), dtype = 'int')
		self.name = name
		f = open('data.dat', 'rb')
		raw_lines = []
		for line in f.readlines(): raw_lines.append(line[:-2])
		for x in xrange(0,13): back_board[x] = raw_lines[x].split('|')
		f.close()

	def translate(self, input):
		refer = {'A':0,'K':1,'Q':2,'J':3,'T':4,9:5,8:6,7:7,6:8,5:9,4:10,3:11,2:12}
		output = refer[input]
		return output

	#makes a specific range based on inputed percentile and stores it in 2D array Specific_Range
	def Overall_percentile(self, percent):
		hand_range_maximus = (float(percent)/100)*169
		for x in xrange(0,13): 
			for y in xrange(0,13):
				if back_board[x][y] < hand_range_maximus: self.range[x][y] = 1
				else: self.range[x][y] = 0

	def Xxs(self, MainString, OyS):
	 	if OyS is 1:
	 		MainString = self.translate(MainString)
	 		for x in range(MainString,12):
				self.range[MainString][x+1] = 1
			for x in range(MainString,0, -1):
				self.range[x-1][MainString] = 1
	# 	else:
	# 		//code here

def show_range(Range):
	plt.grid(True, linestyle = "-")
	ax = plt.axes()
	ax.set_xticks(np.arange(0,15,1))
	ax.set_yticks(np.arange(0,15,1))
	ax.plot(xrange(0,13), xrange(0,13), '-g', label = 'DIVIDE')
	plt.style.use('seaborn-whitegrid')
	plt.title(RM.name)
	plt.imshow(Range, cmap = 'summer') #summer, blues, autumn_r

	points = []
	for x in xrange(0,13):
		for y in xrange(0,13):
			points.append([x,y])
	x = map(lambda x: x[0], points)
	y = map(lambda x: x[1], points)

	labels = [item.get_text() for item in ax.get_xticklabels()]
	labels[0] = 'A'
	labels[1] = 'K'
	labels[2] = 'Q'
	labels[3] = 'J'
	labels[4] = 'T'
	labels[5] = '9'
	labels[6] = '8'
	labels[7] = '7'
	labels[8] = '6'
	labels[9] = '5'
	labels[10] = '4'
	labels[11] = '3'
	labels[12] = '2'
	
	plt.scatter(x,y, color = 'gray')
	ax.set_xticklabels(labels)
	ax.set_yticklabels(labels)
	plt.show()
	plt.close()		

#main ->
user_range_name = str(raw_input('Enter name for your range : ')) 
percentile = float(raw_input('Enter percentile : '))

RM = range_maker(user_range_name)
RM.Overall_percentile(percentile)
#RM.Xxs('A', 1)
show_range(RM.range)