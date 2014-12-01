
# ProfileWriter.py

import os
import unicodecsv as csv

def create_csv(name):
	f = open(name, 'wt') 
	w = csv.writer(f, encoding='utf-8')
	row = ('ip', 'games_played', 'highest_level', 'minutes_played')

	for level in range(6):
		l = level + 1
		label = 'research_time_level' + str(l)
		row = row + (label,)

	for level in range(6):
		l = level + 1
		label = 'protection_percent_level' + str(l)
		row = row + (label,)

	insurance_types = [
		'nil', # didn't buy any insurance
		'a',   # only bought plan 1
		'b',   # only bought plan 2
		'c',   # only bought plan 3
		'ab',  # bought plans 1 and 2
		'ac',  # bought plans 1 and 3
		'bc',  # bought plans 2 and 3
		'abc'  # BUY ALL THE PLANS!!!
	]

	for level in range(6):
		l = level + 1
		for j in range(len(insurance_types)):
			label = 'insurance_level' + str(l) + str(insurance_types[j])
			row = row + (label,)

	row = row + ('reflection',)

	w.writerow(row)

	return w

def write_profile_to_csv(profile):
	row = (
		profile['ip'], 
		profile['games_played'], 
		profile['highest_level'],
		profile['minutes_played']
		)

	for level in range(6):
		label = profile['research_time_level' + str(level)]
		row = row + (label,)

	for level in range(6):
		label = profile['protection_percent_level' + str(level)]
		row = row + (label,)

	for level in range(6):
		for i in range(8):
			label = profile['insurances_level' + str(level) + str(insurance_types[i])]
			row = row + (label,)

	row = row + (profile['reflection'],)
	csv_writer.writerow(row)

insurance_types = [
	'nil', # didn't buy any insurance
	'a',   # only bought plan 1
	'b',   # only bought plan 2
	'c',   # only bought plan 3
	'ab',  # bought plans 1 and 2
	'ac',  # bought plans 1 and 3
	'bc',  # bought plans 2 and 3
	'abc'  # BUY ALL THE PLANS!!!
]

csv_writer = create_csv('csv/reflections-and-data-rank.csv')