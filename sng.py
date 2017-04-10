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
		ecp = float(raw_input("Enter ECPTOTAL : "))
		in_s = int(raw_input('Enter in_stake : '))
		out_s = int(raw_input('Enter out_stake : '))
		
		if initial_write is 1:
			c.execute('''CREATE TABLE main_data
		              (d real, P real, W real, L real, NetCash real, WinPer real, ECP real)''')
		c.execute("INSERT INTO main_data VALUES ({data})".format(data = str(d) + ',' + str(p) + ',' + str(w)+ ',' + str(l)+ ',' +str(nc)+ ',' +str(wp)+ ',' +str(ecp)))
		
		if intial_write is 1:
			c.execute('''CREATE TABLE minor_data
			 			(in_stake real, out_stake real)''')
		
		c.execute("INSERT INTO minor_data VALUES ({data})".format(data = str(in_s) + ',' + str(out_s)))
		conn.commit()
		c.close()
		conn.close()

	def read():
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

		print '\nTotal'
		print 'Played : ' + played
		print 'Won    : ' + won
		print 'WinPer : ' + str(winper)
		print 'NetCash: ' + str(Net_Cash)
		print 'PerGame: ' + str(Per_Game)
		print 'Forecast -' + '\n100: ' + str(Per_Game * 100) + ' 150: ' + str(Per_Game * 150) + ' 200: ' + str(Per_Game*200) + ' 250: ' + str(Per_Game*250)