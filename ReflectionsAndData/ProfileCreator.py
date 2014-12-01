
# ProfileCreator.py

import json
import GameDataHandler as gdh
import ReflectionDataHandler as rdh

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

# if use_matches is true, only ips that have corresponding reflections will be included
use_matches = True
filename = ''
if use_matches == True:
	matches = rdh.get_matches(gdh.get_ips())
	filename = 'json/raw-profiles.json'
else:
	matches = gdh.get_ips()
	filename = 'json/raw-profiles-all.json'

_profiles = {}
_profiles['profiles'] = create_profiles(matches)

with open(filename, 'w') as f:
	json.dump(_profiles, f, ensure_ascii = False, indent = 4)
