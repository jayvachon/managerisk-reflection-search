
from __future__ import division
import json
import GameDataHandler as gdh

LEVEL_COUNT = 6
QUINT_SIZE = 5

def get_profile(ip):
	for p in profiles:
		if p['ip'] == ip:
			return p

def get_qprofile(ip):
	for p in qprofiles:
		if p['ip'] == ip:
			return p

########### Crosscheck two qprofiles ###########
def player_has_match(qprofile, key1, rank1, key2, rank2):
	return qprofile[key1] == str(rank1) and qprofile[key2] == str(rank2)

# returns the number of players whose keys match the given ranks
def rank_match_count(key1, rank1, key2, rank2):
	match_count = 0
	for p in qprofiles:
		if player_has_match(p, key1, rank1, key2, rank2):
			match_count += 1
	return match_count

# returns an array with the number of players per quint who match the rank in key1
def rank_match_counts_per_quint(key1, rank1, key2):
	match_counts = []
	for q in range(QUINT_SIZE):
		match_counts.append(rank_match_count(key1, rank1, key2, q+1))
	return match_counts

def crosscheck_quints(key1, key2):
	crosschecked_quints = []
	for q in range(QUINT_SIZE):
		crosschecked_quints.append(rank_match_counts_per_quint(key1, q+1, key2))
	return crosschecked_quints

########### Crosscheck a profile and qprofile ###########
def player_has_match_pq(profile, key1, value, key2, rank):
	qprofile = get_qprofile(profile['ip'])
	return profile[key1] == value and qprofile[key2] == str(rank)

# returns the number of players whose keys match the given ranks
def rank_match_count_pq(key1, value, key2, rank2):
	match_count = 0
	for p in profiles:
		if player_has_match_pq(p, key1, value, key2, rank2):
			match_count += 1
	return match_count

# returns an array with the number of players per quint who match the rank in key1
def rank_match_counts_per_quint_pq(key1, value, key2):
	match_counts = []
	for q in range(QUINT_SIZE):
		match_counts.append(rank_match_count_pq(key1, value, key2, q+1))
	return match_counts

def crosscheck_quints_pq(key1, max_value, key2):
	crosschecked_quints = []
	for v in range(max_value):
		crosschecked_quints.append(rank_match_counts_per_quint_pq(key1, v+1, key2))
	return crosschecked_quints

# so like for example, this would return the average research time in level 1 of players whose highest level was 1
def get_average_attribute_per_quintile(level, attribute, key, rank):
	value = 0
	count = 0
	for qp in qprofiles:
		if is_profile_in_quintile(qp, key, rank):
			v = gdh.get_level_average_attribute(level, attribute, qp['ip'])
			if v != 'n/a':
				value += v
				count += 1
	if count == 0:
		return 'n/a'
	return value/count

def is_profile_in_quintile(qprofile, key, rank):
	return qprofile[key] == str(rank)

use_matches = False
if use_matches == False:
	qprofiles_filename = 'json/quintile-profiles-all.json'
	profiles_filename = 'json/raw-profiles-all.json'
else:
	qprofiles_filename = 'json/quintile-profiles.json'
	profiles_filename = 'json/raw-profiles.json'

print "loading quintile profiles"
qprofiles_json = json.load(open(qprofiles_filename))
qprofiles = qprofiles_json['profiles']

print "loading raw profiles"
profiles_json = json.load(open(profiles_filename))
profiles = profiles_json['profiles']

# print "loading all game data"
# data = json.load(open('../RiskHorizonData/json_parser/data/risk_horizon.json'))

print "crosschecking"
# print crosscheck_quints_pq('highest_level', 6, 'research_time_level0')
# print crosscheck_quints('research_time_level0', 'highest_level')

# print gdh.get_level_average_attribute(1, 'research time', profiles[0]['ip'])

for level in range(LEVEL_COUNT):
	print "level" + str(level)
	for q in range(QUINT_SIZE):
		print get_average_attribute_per_quintile(level+1, 'protection end percent', 'highest_level', q+1)

