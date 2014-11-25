
# ProfileCreator.py

import json
import unicodecsv as csv
import GameDataHandler as gdh
import ReflectionDataHandler as rdh

########## DEPRECATED ##########
def create_csv(name):
	f = open(name, 'wt') 
	w = csv.writer(f, encoding='utf-8')
	w.writerow((
		'ip', 
		'games_played', 
		'highest_level', 
		'minutes_played', 
		'research_time_level1',
		'research_time_level2',
		'research_time_level3',
		'research_time_level4',
		'research_time_level5',
		'research_time_level6',
		'protection_percent_level1',
		'protection_percent_level2',
		'protection_percent_level3',
		'protection_percent_level4',
		'protection_percent_level5',
		'protection_percent_level6',
		'insurance_level1',
		'insurance_level2',
		'insurance_level3', 
		'insurance_level4',
		'insurance_level5',
		'insurance_level6',
		'reflection'
		))
	return w

def create_profile(ip):
	profile = {}
	profile['ip'] = ip
	profile['reflection'] = rdh.get_reflection_from_ip(ip)
	profile['games_played'] = gdh.get_game_count_from_ip(ip)
	profile['highest_level'] = gdh.get_highest_level_from_ip(ip)
	profile['minutes_played'] = gdh.get_time_played_from_ip(ip)
	profile['research_time'] = gdh.get_level_attribute_deviations(ip, 'research time')
	profile['protection_percent'] = gdh.get_level_attribute_deviations(ip, 'protection end percent')
	profile['insurances'] = gdh.get_level_insurance_deviations(ip)
	return profile

def create_profiles(matches):
	profiles = []
	count = 0
	matches_count = len(matches)
	for m in matches:
		profiles.append(create_profile(m))
		count += 1
		print str(count) + " of " + str(matches_count)
	return profiles

def write_profile_to_csv(profile, csv_writer):
	row = (
		profile['ip'], 
		profile['games_played'], 
		profile['highest_level'],
		profile['minutes_played']
		)
	research = cleanup_research_time(profile['research_time_level'])
	for r in research:
		row = row + (r,)
	protection = cleanup_protection(profile['protection_percent_level'])
	for p in protection:
		row = row + (p,)
	insurances = cleanup_insurances(profile['insurances_level'])
	for i in insurances:
		row = row + (i,)
	row = row + (cleanup_reflection(profile['reflection']),)
	csv_writer.writerow(row)

def write_profile_to_csv_noclean(profile, csv_writer):
	row = (
		profile['ip'], 
		str(profile['games_played']), 
		str(profile['highest_level']),
		str(profile['minutes_played'])
		)
	research = profile['research_time']
	for r in research:
		row = row + (str(r),)
	protection = profile['protection_percent']
	for p in protection:
		row = row + (str(p),)
	insurances = profile['insurances']
	for i in insurances:
		row = row + (str(i),)
	row = row + (profile['reflection'],)
	csv_writer.writerow(row)

def cleanup_research_time(research_time):
	clean_research_time = []
	for t in research_time:
		if t == 'n/a':
			clean_research_time.append('n/a')
		else:
			clean_research_time.append(str(round(t)))
	return clean_research_time

def cleanup_protection(protection):
	clean_protection = []
	for t in protection:
		if t == 'n/a':
			clean_protection.append('n/a')
		else:
			clean_protection.append(str(round(t * 100)) + "%")
	return clean_protection

def cleanup_insurances(insurances):
	clean_insurances = []
	for t in insurances:
		if t == 'n/a':
			clean_insurances.append('n/a')
		else:
			new_cell = ""
			for i in range(3):
				new_cell += str(round(t[i] * 100)) + "%"
				if i < 2:
					new_cell += ", "
			clean_insurances.append(new_cell)
	return clean_insurances

def cleanup_reflection(reflection):
	# return reflection
	# r = repr(reflection)
	# r = re.sub('\n', '', r)
	# r = reflection.encode('utf-8')
	return reflection

matches = rdh.get_matches(gdh.get_ips())
# csv_writer = create_csv('rh-reflections-and-data.csv')
_profiles = {}
_profiles['profiles'] = create_profiles(matches)

with open('json/profiles.json', 'w') as f:
	json.dump(_profiles, f, ensure_ascii = False, indent = 4)
