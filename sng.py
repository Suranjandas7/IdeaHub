import sqlite3
import pandas as pd
import matplotlib.pyplot as plt 

from calc import *

class PokerDataBase(object):
	# def display_winper(self):
	# 	conn = sqlite3.connect('SnG.db')
	# 	c = conn.cursor()
	# 	fd = pd.read_sql_query("SELECT * from main_data", conn)
	# 	values = fd['WinPer'].tolist()
	# 	c.close()
	# 	conn.close()

	def write(self, initial_write):	
		def return_stats(config):
			T_matches = config[0]
			in_stake = config[1]
			out_stake = config[2]
			Played = config[3]
			Won = config[4]
			Lost = config[5]
			GLTP = float(int(T_matches) - int(Played))
			c = round(100 - (GLTP/float(T_matches)*100),2)
			win_per = round(float((float(Won)/float(Played)) * 100),2)
			cash_won = int(out_stake)*int(Won)
			cash_lost = int(in_stake)*int(Lost)
			net_cash = cash_won - cash_lost
			projected_winnings = int(GLTP*(win_per/100)) * int(out_stake)  
			projected_loses = (int(GLTP) - int(GLTP*(win_per/100))) * int(in_stake)
			projected_net = projected_winnings - projected_loses
			worst_ECP = -int(GLTP * int(in_stake)) + net_cash
			best_ECP = int(GLTP * int(out_stake)) + net_cash
			return net_cash, win_per

		conn = sqlite3.connect('SnG.db')
		c = conn.cursor()
		
		d = str(raw_input("Enter Date : "))
		p = float(raw_input("Enter P : "))
		w = float(raw_input("Enter W : "))
		in_s = int(raw_input('Enter in_stake : '))
		out_s = int(raw_input('Enter out_stake : '))
		
		l = p-w
		
		data = [p, in_s, out_s, p, w, l]
		nc, wp = return_stats(data)
		#nc = float(raw_input("Enter NET CASH : "))
		#find out by func
		#wp = float(raw_input("Enter WIN PERC : "))
		#find out by func
		
		if initial_write is 1:
			c.execute('''CREATE TABLE main_data
		              (d real, P real, W real, L real, NetCash real, WinPer real)''')
		
		c.execute("INSERT INTO main_data VALUES ({data})".format(data = str(d) + ',' + str(p) 
		+ ',' + str(w) + ',' + str(l)+ ',' +str(nc)+ ',' +str(wp)))
		
		if initial_write is 1:
			c.execute('''CREATE TABLE minor_data
			 			(in_stake real, out_stake real)''')
		
		c.execute("INSERT INTO minor_data VALUES ({data})".format(data = str(in_s) + ',' 
		+ str(out_s)))
		
		conn.commit()
		c.close()
		conn.close()

	def read(self):

		def forecastor(games_played):
			d = round(float(games_played) / float(50),2)
			elements = []
			for x in xrange(games_played, games_played + 200,50):
				elements.append(str(x))
			return elements
		
		conn = sqlite3.connect('SnG.db')
		c = conn.cursor()
		fd = pd.read_sql_query("SELECT * from main_data", conn)
		print fd
		
		c.close()
		conn.close()

		played = str(int(fd['P'].sum()))
		won = str(int(fd['W'].sum()))
		winper = round((float((fd['W'].sum())/float(fd['P'].sum()))),3) * 100
		Net_Cash = round(float(fd['NetCash'].sum()),2)
		Per_Game = round(Net_Cash/float(played),2)
		ForeCast_Labels = forecastor(int(played))

		print '\nTotal'
		print 'Played : ' + played
		print 'Won    : ' + won
		print 'WinPerG: ' + str(winper)
		print 'NetCash: ' + str(Net_Cash)
		print 'PerGame: ' + str(Per_Game)
		print 'Forecast -'
		print 'Games' + '\t' + 'NetCash Estimated'
		for x in xrange(0,4): print ForeCast_Labels[x] + '\t' +  str(Per_Game * 
														int(ForeCast_Labels[x]))