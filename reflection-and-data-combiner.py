
import re, json

class GameDataHandler:

	_data = {}

	def __init__(self):
		data_file = open('RiskHorizonData/json_parser/data/risk_horizon.json')
		self._data = json.load(data_file)

	def get_average_research_time_per_level(self, level):
		#TODO: why does this break??
		d = self._data
		# count = 0
		# for i in range(len(d)):
		# 	session = d[i]['session']

	def get_ips(self):
		ips = []
		for i in range(len(self._data)):
			ip = self._data[i]['ipv4']
			ip = self.filter_ip(ip)
			ips.append(ip)
		return ips

	def filter_ip(self, ip):
		return re.match(r'[^,]*', ip).group(0)

	def get_player_by_ip(self, ip):
		for player in self._data:
			if self.filter_ip(player['ipv4']) == ip:
				return player

	def get_game_count_from_ip(self, ip):
		sessions = self.get_player_by_ip(ip)['session']
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

	def get_levels_from_ip(self, ip):
		sessions = self.get_player_by_ip(ip)['session']
		all_levels = []
		for i in range(len(sessions)):
			levels = sessions[i]['levels']
			for level in levels:
				all_levels.append(level)
		return all_levels

	def get_highest_level_from_ip(self, ip):
		sessions = self.get_player_by_ip(ip)['session']
		highest_level = 0
		for i in range(len(sessions)):
			levels = sessions[i]['levels']
			for j in range(len(levels)):
				level = levels[j]['level']
				if level > highest_level:
					highest_level = level
		return highest_level

	def get_average_research_per_level(self, ip):
		levels = self.get_levels_from_ip(ip)
		total_research = 0
		for level in levels:
			total_research += level['research time']
		return total_research / len(levels)

	def get_time_played_from_ip(self, ip):
		sessions = self.get_player_by_ip(ip)['session']
		time = 0
		level_duration = 3 # minutes
		for i in range(len(sessions)):
			levels = sessions[i]['levels']
			for l in levels:
				time += level_duration
		return time

class ReflectionDataHandler:

	_data = {}
	_submissions = []

	def __init__(self):
		data_file = open('RiskHorizonReflections/submissions.json')
		self._data = json.load(data_file)
		self._submissions = self._data['submissions']

	def get_ips(self):
		ips = []
		for reflection in self._submissions:
			ips.append(reflection['ip'])
		return ips

	def get_matches(self, game_ips):
		ips = self.get_ips()
		matches = []
		for i in range(len(ips)):
			ip = ips[i]
			if ip in game_ips:
				matches.append(ip)
		return matches

	def get_reflection_from_ip(self, ip):
		for submission in self._submissions:
			if ip == submission['ip']:
				return submission['reflection'].encode('utf-8')

class ProfileCreator:

	def __init__(self):
		reflection_data = ReflectionDataHandler()
		game_data = GameDataHandler()
		matches = reflection_data.get_matches(game_data.get_ips())
		self.create_profile(matches[0], reflection_data, game_data)

	def create_profile(self, ip, reflection_data, game_data):
		profile = {}
		profile['ip'] = ip
		profile['reflection'] = reflection_data.get_reflection_from_ip(ip)
		profile['games_played'] = game_data.get_game_count_from_ip(ip)
		profile['highest_level'] = game_data.get_highest_level_from_ip(ip)
		profile['time_played'] = game_data.get_time_played_from_ip(ip)
		profile['average_level1_research'] = game_data.get_average_research_per_level(1)
		# game_data.get_average_research_per_level(ip)
		print profile

profile_creator = ProfileCreator()
