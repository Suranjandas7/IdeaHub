#TO-DO: Get MatplotLib up in this shit.

import sqlite3
import pandas as pd

class PokerDataBase(object):
	def write(self, initial_write):
		conn = sqlite3.connect('SnG.db')
		c = conn.cursor()
		
		d = str(raw_input("Enter Date : "))
		p = float(raw_input("Enter P : "))
		w = float(raw_input("Enter W : "))
		
		l = p-w
		
		nc = float(raw_input("Enter NET CASH : "))
		wp = float(raw_input("Enter WIN PERC : "))
		
		in_s = int(raw_input('Enter in_stake : '))
		out_s = int(raw_input('Enter out_stake : '))
		
		if initial_write is 1:
			c.execute('''CREATE TABLE main_data
		              (d real, P real, W real, L real, NetCash real, WinPer real)''')
		
		c.execute("INSERT INTO main_data VALUES ({data})".format(data = str(d) + ',' + str(p) + ',' + str(w)+ ',' + str(l)+ ',' +str(nc)+ ',' +str(wp)))
		
		if initial_write is 1:
			c.execute('''CREATE TABLE minor_data
			 			(in_stake real, out_stake real)''')
		
		c.execute("INSERT INTO minor_data VALUES ({data})".format(data = str(in_s) + ',' + str(out_s)))
		
		conn.commit()
		c.close()
		conn.close()

	def read(self):
		conn = sqlite3.connect('SnG.db')
		c = conn.cursor()
		fd = pd.read_sql_query("SELECT * from main_data", conn)
		fd2 = pd.read_sql_query("SELECT * from minor_data", conn)
		print fd
		print fd2
		c.close()
		conn.close()

		played = str(int(fd['P'].sum()))
		won = str(int(fd['W'].sum()))
		winper = round((float((fd['W'].sum())/float(fd['P'].sum()))),3) * 100
		Net_Cash = round(float(fd['NetCash'].sum()),2)
		Per_Game = round(Net_Cash/float(played),2)
		ForeCast_Labels = self.forecastor(int(played))

		print '\nTotal'
		print 'Played : ' + played
		print 'Won    : ' + won
		print 'WinPerG: ' + str(winper)
		print 'NetCash: ' + str(Net_Cash)
		print 'PerGame: ' + str(Per_Game)
		print 'Forecast -'
		print 'Games' + '\t' + 'NetCash Estimated'
		for x in xrange(0,4): print ForeCast_Labels[x] + '\t' +  str(Per_Game * int(ForeCast_Labels[x]))

	def forecastor(self, games_played):
		d = round(float(games_played) / float(50),2)
		elements = []
		for x in xrange(games_played, games_played + 200,50):
			elements.append(str(x))
		return elements