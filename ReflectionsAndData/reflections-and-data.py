
import numpy as np
import json
import GameDataHandler as gdh
import ReflectionDataHandler as rdh
import QuintileCreator as qc
import ProfileWriter as pw

def get_quintiles():

	profiles_arr = profiles['profiles']

	quints = {}
	quints['games_played'] = qc.create_quintile_from_key(profiles_arr, 'games_played')
	quints['highest_level'] = qc.create_quintile_from_key(profiles_arr, 'highest_level')
	quints['minutes_played'] = qc.create_quintile_from_key(profiles_arr, 'minutes_played')
	
	for level in range(6):
		quints['research_time_level' + str(level)] = qc.create_quintile_from_key(profiles_arr, 'research_time', level)
	
	for level in range(6):
		quints['protection_percent_level' + str(level)] = qc.create_quintile_from_key(profiles_arr, 'protection_percent', level)

	for level in range(6):
		for i in range(8):
			arr = create_insurance_array(profiles_arr, level, i)
			quints['insurances_level'+ str(level) + insurance_types[i]] = qc.create_quintile(arr)
			
	return quints

def create_insurance_array(profiles_arr, level, insurance_type):
	arr = []
	for p in profiles_arr:
		arr.append(p['insurances'][level][insurance_type])
	return arr

def write_quintile_profile(profile):
	quint_profile = {}
	quint_profile['ip'] = profile['ip']
	quint_profile['games_played'] = qc.range_in_quintile(quintiles['games_played'], profile['games_played'])
	quint_profile['highest_level'] = qc.range_in_quintile(quintiles['highest_level'], profile['highest_level'])
	quint_profile['minutes_played'] = qc.range_in_quintile(quintiles['minutes_played'], profile['minutes_played'])
	
	for level in range(6):
		key = 'research_time_level' + str(level)
		res = profile['research_time'][level]
		if res != 'n/a':
			quint_profile[key] = qc.range_in_quintile(quintiles[key], res)
		else:
			quint_profile[key] = 'n/a'

	for level in range(6):
		key = 'protection_percent_level' + str(level)
		pro = profile['protection_percent'][level]
		if pro == 'n/a':
			quint_profile[key] = 'n/a'
		else:
			quint_profile[key] = qc.range_in_quintile(quintiles[key], pro, percentage=True)

	for level in range(6):
		for i in range(8):
			key = 'insurances_level' + str(level) + str(insurance_types[i])
			ins = profile['insurances'][level]
			if ins == [0,0,0,0,0,0,0,0] or ins == 'n/a':
				quint_profile[key] = 'n/a'
			else:
				quint_profile[key] = qc.range_in_quintile(quintiles[key], ins[i], percentage=True)

	quint_profile['reflection'] = profile['reflection']

	pw.write_profile_to_csv(quint_profile)

def write_quintile_profiles():
	for p in profiles['profiles']:
		write_quintile_profile(p)

def write_quintiles_to_json():

	profiles_arr = profiles['profiles']

	quints = {}
	quints['games_played'] = qc.create_quintile_from_key(profiles_arr, 'games_played')
	quints['highest_level'] = qc.create_quintile_from_key(profiles_arr, 'highest_level')
	quints['minutes_played'] = qc.create_quintile_from_key(profiles_arr, 'minutes_played')
	
	research_time = []
	for level in range(6):
		research_time.append(qc.create_quintile_from_key(profiles_arr, 'research_time', level))
	quints['research_time'] = research_time
	
	protection_percent = []
	for level in range(6):
		protection_percent.append(qc.create_quintile_from_key(profiles_arr, 'protection_percent', level))
	quints['protection_percent'] = protection_percent

	insurances = {}
	for level in range(6):
		insurance_level = {}
		for i in range(8):
			arr = create_insurance_array(profiles_arr, level, i)
			insurance_level[insurance_types[i]] = qc.create_quintile(arr)
		insurances['level ' + str(level+1)] = insurance_level

	quints['insurances'] = insurances
			
	with open('json/quintiles.json', 'w') as f:
		json.dump(quints, f, ensure_ascii=False, indent=4)

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

profiles = json.load(open('json/profiles.json'))
quintiles = get_quintiles()

write_quintile_profiles()
# write_quintiles_to_json()

