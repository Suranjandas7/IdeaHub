#DONE: Write a dict like {0:2, 1:3, 2:4 etc} to correspond with hand rankings.
#DONE: Write a func that creates a numpy chart with x and os to fit a players's range of starting hands.

#To-DO: Provide a written range too. For example A7-A8, K5o-K8o etc...


import numpy as np
import matplotlib.pyplot as plt

back_board = np.zeros(shape = (13,13), dtype = 'int')
Specific_Range = np.zeros(shape = (13,13), dtype = 'int')

#loads data from data.dat to numpy 2-d array back_board
def load_data():
	f = open('data.dat', 'rb')
	raw_lines = []
	for line in f.readlines(): raw_lines.append(line[:-2])
	for x in xrange(0,13): back_board[x] = raw_lines[x].split('|')
	f.close()

#makes a specific range based on inputed percentile and stores it in 2D array Specific_Range
def make_specific_range(percent):
	hand_range_maximus = (float(percent)/100)*169
	for x in xrange(0,13): 
		for y in xrange(0,13):
			if back_board[x][y] < hand_range_maximus: Specific_Range[x][y] = 1
			else: Specific_Range[x][y] = 0

#formats the range to look pretty on screen
def show_range():
	plt.grid(True, linestyle = "-")
	ax = plt.axes()
	ax.set_xticks(np.arange(0,15,1))
	ax.set_yticks(np.arange(0,15,1))
	ax.plot(xrange(0,13), xrange(0,13), '-g', label = 'DIVIDE')
	plt.imshow(Specific_Range, cmap = 'prism')

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
	
	plt.scatter(x,y)
	ax.set_xticklabels(labels)
	ax.set_yticklabels(labels)
	plt.show()		

#procedure: 
load_data()
make_specific_range(raw_input('Enter percentile : '))
print Specific_Range
show_range()