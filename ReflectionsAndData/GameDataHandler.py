
from __future__ import division
import json, re

def get_level_average_attribute(level_number, attribute, ip='n/a'):
	total_attribute = 0
	level_count = 0
	levels = get_levels(ip, level_number)
	
	for level in levels:
		total_attribute += level[attribute]
		level_count += 1

	# return 'n/a' if the player never reached the given level
	if level_count == 0:
		return 'n/a'
	return total_attribute / level_count

def get_levels_average_attribute(attribute, ip='n/a'):
	attributes = []
	for i in range(6):
		attributes.append(get_level_average_attribute(i+1, attribute, ip))
	return attributes

def get_level_average_insurance(level_number, ip='n/a'):
	
	total_insurances = [0,0,0,0,0,0,0,0]
	average_insurances = [0,0,0,0,0,0,0,0]

	insurance_types = []
	insurance_types.append([0,0,0])
	insurance_types.append([1,0,0])
	insurance_types.append([0,1,0])
	insurance_types.append([0,0,1])
	insurance_types.append([1,1,0])
	insurance_types.append([1,0,1])
	insurance_types.append([0,1,1])
	insurance_types.append([1,1,1])

	levels = get_levels(ip, level_number)
	level_count = len(levels)
	for level in levels:
		insurances = level['insurances']
		plans = []
		for plan in insurances:
			plans.append(1 if plan else 0)
		for i in range(len(insurance_types)):
			if plans == insurance_types[i]:
				total_insurances[i] += 1

	average_insurances = [ti/level_count for ti in total_insurances if level_count > 0]

	return average_insurances

	"""
	total_insurances = [0,0,0]
	average_insurances = [0,0,0]
	level_count = 0
	levels = get_levels(ip, level_number)
	for level in levels:
		insurances = level['insurances']
		for insurance in range(len(total_insurances)):
			if insurances[insurance]:
				total_insurances[insurance] += 1
		level_count += 1
	
	if level_count == 0:
		return 'n/a'
	for insurance in range(len(total_insurances)):
		average_insurances[insurance] = total_insurances[insurance] / level_count
	return average_insurances
	"""

def get_levels_average_insurance(ip='n/a'):
	insurances = {}
	for i in range(6):
		insurances[i] = get_level_average_insurance(i+1, ip)
	return insurances

def get_level_attribute_deviations(ip, attribute, percentage=True):
	# for this ip, the attribute at each level
	attributes = get_levels_average_attribute(attribute, ip)

	# across all sessions, the attribute average at each level
	total_attribute = _average_attributes[attribute]
	deviations = []
	for i in range(6):
		a = attributes[i]
		if a == 'n/a':
			deviations.append('n/a')
		else:
			deviations.append(a - total_attribute[i])
	return deviations

def get_level_insurance_deviations(ip):
	
	insurances = get_levels_average_insurance(ip)
	average_insurances = _average_attributes['insurances']

	deviations = []
	for level in range(6):
		if insurances[level] == 'n/a':
			deviations.append('n/a')
			continue
		deviations.append([0,0,0,0,0,0,0,0])
		for d in range(len(insurances[level])):
			i = insurances[level][d]
			a = average_insurances[str(level)][d]
			deviations[level][d] = i-a

	return deviations

	"""
	total_insurances = _average_attributes['insurances']
	deviations = []
	for l in range(6):
		if insurances[l] == 'n/a':
			deviations.append('n/a')
			continue
		deviations.append([0,0,0])
		for i in range(3):
			deviations[l][i] = insurances[l][i] - total_insurances[l][i]
	return deviations
	"""

def get_ips():
	ips = []
	for i in range(len(_data)):
		ip = _data[i]['ipv4']
		ip = filter_ip(ip)
		ips.append(ip)
	return ips

def get_levels(ip='n/a', level_number=None):
	
	levels = []
	levels_of_number = []
	
	# if no ip address was provided, get all the levels
	if ip == 'n/a':
		levels = get_all_levels()
	else:
		levels = get_ip_levels(ip)
	if level_number == None:
		return levels
	for level in levels:
		if level['level'] == level_number:
			levels_of_number.append(level)
	return levels_of_number

def filter_ip(ip):
	return re.match(r'[^,]*', ip).group(0)

def get_player_by_ip(ip):
	for player in _data:
		if filter_ip(player['ipv4']) == ip:
			return player

def get_ip_sessions(ip):
	return get_player_by_ip(ip)['session']

def get_game_count_from_ip(ip):
	sessions = get_ip_sessions(ip)
	game_count = 0
	for i in range(len(sessions)):
		levels = sessions[i]['levels']
		for l in levels:
			if l['level'] == 1:
				game_count += 1

	# in case data from level 1s wasn't collected, count level 2s played
	if game_count == 0:
		for i in range(len(sessions)):
			levels = sessions[i]['levels']
			for l in levels:
				if l['level'] == 2:
					game_count += 1
	
	return game_count

def get_all_sessions():
	all_sessions = []
	for i in range(len(_data)):
		sessions = _data[i]['session']
		for session in range(len(sessions)):
			all_sessions.append(sessions[session])
	return all_sessions

def get_all_levels():
	all_levels = []
	sessions = get_all_sessions()
	for session in sessions:
		levels = session['levels']
		for level in levels:
			all_levels.append(level)
	return all_levels

def get_ip_levels(ip):
	sessions = get_ip_sessions(ip)
	all_levels = []
	for i in range(len(sessions)):
		levels = sessions[i]['levels']
		for level in levels:
			all_levels.append(level)
	return all_levels

def get_highest_level_from_ip(ip):
	sessions = get_ip_sessions(ip)
	highest_level = 0
	for i in range(len(sessions)):
		levels = sessions[i]['levels']
		for j in range(len(levels)):
			level = levels[j]['level']
			if level > highest_level:
				highest_level = level
	return highest_level

def get_time_played_from_ip(ip):
	sessions = get_ip_sessions(ip)
	time = 0
	level_duration = 3 # minutes
	for i in range(len(sessions)):
		levels = sessions[i]['levels']
		for l in levels:
			time += level_duration
	return time

data_file = open('../RiskHorizonData/json_parser/data/risk_horizon.json')
_data = json.load(data_file)

_average_attributes = json.load(open('json/average-attributes.json'))

"""
_average_attributes = {}
_average_attributes['research time'] = get_levels_average_attribute('research time')
_average_attributes['protection end percent'] = get_levels_average_attribute('protection end percent')
_average_attributes['insurances'] = get_levels_average_insurance()

with open('json/average-attributes.json', 'w') as f:
	json.dump(_average_attributes, f, ensure_ascii = False, indent = 4)
"""