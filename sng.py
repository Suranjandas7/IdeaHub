#Suranjan Das Poker SnG Tracker
import csv

class SnG(object):
	def __init__(self):
		f = open('config.cfg', 'rb')
		self.config = f.readlines()
		self.config = (str(self.config[0]).split(','))
		self.history = []
		self.T_matches = self.config[0]
		self.Name = self.config[1]
		self.in_stake = self.config[2]
		self.out_stake = self.config[3]
		self.Played = 0
		self.Won = 0
		self.Lost = 0
		data = csv.reader(open('data.csv', 'rb'))
		for a, b, c in data:
			self.Played = int(a)
			self.Won = int(b)
			self.Lost = int(c)
		self.hist_switch = 0
		f.close()

	def read_hist(self):
		k = open('history.dat', 'r')
		history = k.readlines()
		history = history[0].split(',')
		for element in history:
			self.history.append(element)
		k.close()
		
	def won_game(self):
		self.Played += 1
		self.Won += 1
		self.hist_switch = 1

	def lost_game(self):
		self.Played += 1
		self.Lost += 1

	def stats(self):
		GLTP = float(int(self.T_matches) - int(self.Played))
		c = round(100 - (GLTP/float(self.T_matches)*100),2)
		win_per = round(float((float(self.Won)/float(self.Played)) * 100),2)
		cash_won = int(self.out_stake)*int(self.Won)
		cash_lost = int(self.in_stake)*int(self.Lost)
		net_cash = cash_won - cash_lost
		projected_winnings = int(GLTP*(win_per/100)) * int(self.out_stake)  
		projected_loses = (int(GLTP) - int(GLTP*(win_per/100))) * int(self.in_stake)
		projected_net = projected_winnings - projected_loses

		print 'CURRENT PROGRESS:' + '\t' + str(c) +'\n\n'
		print 'Player Name: \t' + str(self.Name)
		print 'Played: ' + str(self.Played) + '\t' + 'Won: ' + str(self.Won) + '\t' + 'Lost: ' + str(self.Lost) + '\t'
		print 'Cash won: ' + str(cash_won) + '\t' + 'Cash lost: ' + str(cash_lost)
		print 'Net Cash: ' + str(net_cash)
		print '\n'
		print 'Current Win Rate: ' + str(win_per)
		print '\n'
		print 'Projected_net: ' + str(projected_net)
		print 'AWP: ' + str(int(net_cash) + int(projected_net))

	def write_to_data(self):
		writer = csv.writer(open('data.csv', 'w', buffering = 0))
		writer.writerows([(self.Played, self.Won, self.Lost)])
		k = open('history.dat', 'w')
		if self.hist_switch is 1:
			self.history.append('W')
		else:
			self.history.append('L')
		for element in self.history:
			k.write(str(element)+',')
		hist_switch = 0
		k.close()