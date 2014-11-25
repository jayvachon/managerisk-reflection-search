
# QuintileCreator.py

from __future__ import division
import numpy as np

def create_quintiles(profiles):
	
	quints = {}
	quints['games_played'] = create_quintile_from_key(profiles, 'games_played')
	quints['highest_level'] = create_quintile_from_key(profiles, 'highest_level')
	quints['minutes_played'] = create_quintile_from_key(profiles, 'minutes_played')
	
	for level in range(6):
		quints['research_time' + str(level)] = create_quintile_from_key(profiles, 'research_time', level)
	
	for level in range(6):
		quints['protection_percent' + str(level)] = create_quintile_from_key(profiles, 'protection_percent', level)
	
	"""
	for level in range(6):
		arr = []
		for insurance in range(3):
			arr.append(create_quintile(get_insurance_vals(level)[insurance]))
		quints['insurance_level' + str(level)] = arr
	"""
	"""
	print quints['games_played'], quints['highest_level'], quints['minutes_played'], quints['research_time1'], quints['research_time2'], quints['research_time3'], quints['research_time4'], quints['research_time5'], quints['protection_percent0'], quints['protection_percent1'], quints['protection_percent2'], quints['protection_percent3'], quints['protection_percent4'], quints['protection_percent5']
	"""
	return quints

def create_quintile_from_key(profiles, key, index=-1):
	if index > -1:
		arr = get_key_arr_at_index(profiles, key, index)
	else:
		arr = get_key_arr(profiles, key)
	return create_quintile(arr)

def get_key_arr(profiles, key):
	arr = []
	for p in profiles:
		arr.append(p[key])
	return arr

def get_key_arr_at_index(profiles, key, index):
	arr = []
	for p in profiles:
		val = p[key][index]
		if val != 'n/a':
			arr.append(val)
	return arr

def create_quintile(data_arr):
	return create_quantile(data_arr, 5)

def create_tertile(data_arr):
	return create_quantile(data_arr, 3)

def create_quantile(data_arr, q):
	arr = np.array(data_arr)
	quantile_arr = []
	quantile_arr.append(np.amin(arr))
	p = 100 / q
	for i in range(q):
		quantile_arr.append(np.percentile(arr, (i+1) * p))
	return quantile_arr

def write_quintile_to_profile(profiles, key, index=-1):
	for p in range(len(profiles)):
		if index > -1:
			val = profiles[p][key][index]
			if val == 'n/a':
				continue
			profiles[p][key][index] = group_data_in_quintile(key + str(index), val)
		else:
			val = profiles[p][key]
			if val == 'n/a':
				continue
			profiles[p][key] = group_data_in_quintile(key, val)

def write_insurance_quintile_to_profile(profiles, level):
	for p in range(len(profiles)):
		for i in range(3):
			val = profiles[p]['insurances'][level][i]
			profiles[p]['insurances'][level][i] = group_data_in_quintile('insurance_level' + str(level), val)
			# print profiles[p]['insurances'][level][i]

########### DEPRECATED ##########
def group_data_in_quintile(key, data):
	group = ""
	quintile = _quintiles[key]
	qlen = len(quintile)
	for i in range(qlen):
		if data < quintile[i] or i == qlen-1:
			from_val = quintile[i-1]
			to_val = quintile[i]
			if key.find('protection_percent') == False:
				from_val *= 100
				to_val *= 100
			from_val = round(from_val)
			to_val = round(to_val)
			group = str(from_val) + " to " + str(to_val)
			break
	if group == "":
		print "ERROR!!!!!", data, quintile
	return group

def range_in_quintile(quintile, data, round_vals=True, percentage=False):
	
	qlen = len(quintile)
	from_val = 0
	to_val = 0

	for i in range(qlen):
		if data <= quintile[i] and i > 0:
			from_val = quintile[i-1]
			to_val = quintile[i]
			break

	if from_val == 0 and to_val == 0:
		print "data point doesn't fit within the quintile", data, quintile
		return 'n/a'

	if percentage:
		from_val *= 100
		to_val *= 100

	if round_vals:
		from_val = round(from_val)
		to_val = round(to_val)

	fv_str = str(from_val)
	tv_str = str(to_val)

	fv_str = fv_str[:-2]
	tv_str = tv_str[:-2]

	label = fv_str + " to " + tv_str
	return label

def position_in_quintile(quintile, data, percentage=False):

	position = -1
	qlen = len(quintile)
	
	for i in range(qlen):
		if data <= quintile[i] and i > 0:
			position = i
			break

	if position == -1:
		print "data point doesn't fit within the quintile", data, quintile
		return 'n/a'

	# percentile = position * 20

	return str(percentile)

def get_insurance_vals(profiles, level):
	arr = []
	arr.append([])
	arr.append([])
	arr.append([])
	for p in profiles:
		level_vals = p['insurances'][level]
		if level_vals == 'n/a':
			continue
		for i in range(3):
			arr[i].append(level_vals[i])
	return arr

# _quintiles = create_quintiles()
