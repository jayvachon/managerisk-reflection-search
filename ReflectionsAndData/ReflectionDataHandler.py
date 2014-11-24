
import json

def get_ips():
	ips = []
	for reflection in _submissions:
		ips.append(reflection['ip'])
	return ips

def get_matches(game_ips):
	ips = get_ips()
	matches = []
	for i in range(len(ips)):
		ip = ips[i]
		if ip in game_ips:
			matches.append(ip)
	return matches

def get_reflection_from_ip(ip):
	for submission in _submissions:
		if ip == submission['ip']:
			return submission['reflection'].encode('utf-8')

data_file = open('../RiskHorizonReflections/submissions.json')
_data = json.load(data_file)
_submissions = _data['submissions']