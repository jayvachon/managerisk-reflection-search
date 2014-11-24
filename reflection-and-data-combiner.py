
# Deprecated. Go to ReflectionsAndData directory

from __future__ import division
import re, json, sys
import unicodecsv as csv
import numpy as np

class GameDataHandler:

	_data = {}
	_average_attributes = {}

	def __init__(self):
		data_file = open('RiskHorizonData/json_parser/data/risk_horizon.json')
		self._data = json.load(data_file)
		self._average_attributes['research time'] = self.get_levels_average_attribute('research time')
		self._average_attributes['protection end percent'] = self.get_levels_average_attribute('protection end percent')
		self._average_attributes['insurances'] = self.get_levels_average_insurance()

	def get_level_average_attribute(self, level_number, attribute, ip='n/a'):
		total_attribute = 0
		level_count = 0
		levels = self.get_levels(ip, level_number)
		
		for level in levels:
			total_attribute += level[attribute]
			level_count += 1

		# return 'n/a' if the player never reached the given level
		if level_count == 0:
			return 'n/a'
		return total_attribute / level_count

	def get_levels_average_attribute(self, attribute, ip='n/a'):
		attributes = []
		for i in range(6):
			attributes.append(self.get_level_average_attribute(i + 1, attribute, ip))
		return attributes

	def get_level_average_insurance(self, level_number, ip='n/a'):
		total_insurances = [0,0,0]
		average_insurances = [0,0,0]
		level_count = 0
		levels = self.get_levels(ip, level_number)
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

	def get_levels_average_insurance(self, ip='n/a'):
		insurances = {}
		for i in range(6):
			insurances[i] = self.get_level_average_insurance(i + 1, ip)
		return insurances

	def get_level_attribute_deviations(self, ip, attribute, percentage=True):
		# for this ip, the attribute at each level
		attributes = self.get_levels_average_attribute(attribute, ip)

		# across all sessions, the attribute average at each level
		total_attribute = self._average_attributes[attribute]
		deviations = []
		for i in range(6):
			a = attributes[i]
			if a == 'n/a':
				deviations.append('n/a')
			else:
				deviations.append(a - total_attribute[i])
		return deviations

	def get_level_insurance_deviations(self, ip):
		insurances = self.get_levels_average_insurance(ip)
		total_insurances = self._average_attributes['insurances']
		deviations = []

		for l in range(6):
			if insurances[l] == 'n/a':
				deviations.append('n/a')
				continue
			deviations.append([0,0,0])
			for i in range(3):
				deviations[l][i] = insurances[l][i] - total_insurances[l][i]
		return deviations


	def get_ips(self):
		ips = []
		for i in range(len(self._data)):
			ip = self._data[i]['ipv4']
			ip = self.filter_ip(ip)
			ips.append(ip)
		return ips

	def get_levels(self, ip='n/a', level_number=None):
		levels = []
		levels_of_number = []
		# if no ip address was provided, get all the levels
		if ip == 'n/a':
			levels = self.get_all_levels()
		else:
			levels = self.get_ip_levels(ip)
		if level_number == None:
			return levels
		for level in levels:
			if level['level'] == level_number:
				levels_of_number.append(level)
		return levels_of_number

	def filter_ip(self, ip):
		return re.match(r'[^,]*', ip).group(0)

	def get_player_by_ip(self, ip):
		for player in self._data:
			if self.filter_ip(player['ipv4']) == ip:
				return player

	def get_ip_sessions(self, ip):
		return self.get_player_by_ip(ip)['session']

	def get_game_count_from_ip(self, ip):
		sessions = self.get_ip_sessions(ip)
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

	def get_all_sessions(self):
		all_sessions = []
		for i in range(len(self._data)):
			sessions = self._data[i]['session']
			for session in range(len(sessions)):
				all_sessions.append(sessions[session])
		return all_sessions

	def get_all_levels(self):
		all_levels = []
		sessions = self.get_all_sessions()
		for session in sessions:
			levels = session['levels']
			for level in levels:
				all_levels.append(level)
		return all_levels

	def get_ip_levels(self, ip):
		sessions = self.get_ip_sessions(ip)
		all_levels = []
		for i in range(len(sessions)):
			levels = sessions[i]['levels']
			for level in levels:
				all_levels.append(level)
		return all_levels

	def get_highest_level_from_ip(self, ip):
		sessions = self.get_ip_sessions(ip)
		highest_level = 0
		for i in range(len(sessions)):
			levels = sessions[i]['levels']
			for j in range(len(levels)):
				level = levels[j]['level']
				if level > highest_level:
					highest_level = level
		return highest_level

	def get_time_played_from_ip(self, ip):
		sessions = self.get_ip_sessions(ip)
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

	_profiles = []

	def __init__(self, create_profiles=True):
		reflection_data = ReflectionDataHandler()
		game_data = GameDataHandler()
		matches = reflection_data.get_matches(game_data.get_ips())
		csv_writer = self.create_csv('rh-reflections-and-data.csv')
		# profile = self.create_profile(matches[4], reflection_data, game_data)
		if create_profiles:
			self._profiles = self.create_profiles(matches, reflection_data, game_data)
		"""
		# self.write_profile_to_csv(profile, csv_writer)
		profiles_count = len(profiles)
		count = 0
		for p in profiles:
			self.write_profile_to_csv(p, csv_writer)
			count += 1
			print str(count) + " of " + str(profiles_count)
		# self.write_profile_to_csv(profiles[1], csv_writer)
		"""

	def get_profiles(self):
		return self._profiles

	def create_csv(self, name):
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

	def create_profile(self, ip, reflection_data, game_data):
		profile = {}
		profile['ip'] = ip
		profile['reflection'] = reflection_data.get_reflection_from_ip(ip)
		profile['games_played'] = game_data.get_game_count_from_ip(ip)
		profile['highest_level'] = game_data.get_highest_level_from_ip(ip)
		profile['minutes_played'] = game_data.get_time_played_from_ip(ip)
		profile['research_time'] = game_data.get_level_attribute_deviations(ip, 'research time')
		profile['protection_percent'] = game_data.get_level_attribute_deviations(ip, 'protection end percent')
		profile['insurances'] = game_data.get_level_insurance_deviations(ip)
		return profile

	def create_profiles(self, matches, reflection_data, game_data):
		profiles = []
		count = 0
		matches_count = len(matches)
		for m in matches:
			profiles.append(self.create_profile(m, reflection_data, game_data))
			count += 1
			print str(count) + " of " + str(matches_count)
		return profiles

	def write_profile_to_csv(self, profile, csv_writer):
		row = (
			profile['ip'], 
			profile['games_played'], 
			profile['highest_level'],
			profile['minutes_played']
			)
		research = self.cleanup_research_time(profile['research_time'])
		for r in research:
			row = row + (r,)
		protection = self.cleanup_protection(profile['protection_percent'])
		for p in protection:
			row = row + (p,)
		insurances = self.cleanup_insurances(profile['insurances'])
		for i in insurances:
			row = row + (i,)
		row = row + (self.cleanup_reflection(profile['reflection']),)
		csv_writer.writerow(row)

	def write_profile_to_csv_noclean(self, profile, csv_writer):
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

	def cleanup_research_time(self, research_time):
		clean_research_time = []
		for t in research_time:
			if t == 'n/a':
				clean_research_time.append('n/a')
			else:
				clean_research_time.append(str(round(t)))
		return clean_research_time

	def cleanup_protection(self, protection):
		clean_protection = []
		for t in protection:
			if t == 'n/a':
				clean_protection.append('n/a')
			else:
				clean_protection.append(str(round(t * 100)) + "%")
		return clean_protection

	def cleanup_insurances(self, insurances):
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

	def cleanup_reflection(self, reflection):
		# return reflection
		# r = repr(reflection)
		# r = re.sub('\n', '', r)
		# r = reflection.encode('utf-8')
		return reflection

class QuintileCreator:

	_profiles = []
	_quintiles = {}

	def __init__(self, profiles):
		
		self._profiles = profiles
		self._quintiles = self.create_quintiles()
		"""
		self.write_quintile_to_profile('games_played')
		self.write_quintile_to_profile('highest_level')
		self.write_quintile_to_profile('minutes_played')
		for level in range(6):
			self.write_quintile_to_profile('research_time', level)
			self.write_quintile_to_profile('protection_percent', level)
			# self.write_insurance_quintile_to_profile(level)
		"""

	def get_profiles(self):
		return self._profiles

	def write_quintile_to_profile(self, key, index=-1):
		for p in range(len(self._profiles)):
			if index > -1:
				val = self._profiles[p][key][index]
				if val == 'n/a':
					continue
				self._profiles[p][key][index] = self.group_data_in_quintile(key + str(index), val)
			else:
				val = self._profiles[p][key]
				if val == 'n/a':
					continue
				self._profiles[p][key] = self.group_data_in_quintile(key, val)

	def write_insurance_quintile_to_profile(self, level):
		for p in range(len(self._profiles)):
			for i in range(3):
				val = self._profiles[p]['insurances'][level][i]
				self._profiles[p]['insurances'][level][i] = self.group_data_in_quintile('insurance_level' + str(level), val)
				# print self._profiles[p]['insurances'][level][i]

	def group_data_in_quintile(self, key, data):
		group = ""
		quintile = self._quintiles[key]
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

	def create_quintiles(self):
		
		quints = {}
		quints['games_played'] = self.create_quintile_from_key('games_played')
		quints['highest_level'] = self.create_quintile_from_key('highest_level')
		quints['minutes_played'] = self.create_quintile_from_key('minutes_played')
		
		for level in range(6):
			quints['research_time' + str(level)] = self.create_quintile_from_key('research_time', level)
		
		for level in range(6):
			quints['protection_percent' + str(level)] = self.create_quintile_from_key('protection_percent', level)
		
		for level in range(6):
			arr = []
			for insurance in range(3):
				arr.append(self.create_quintile(self.get_insurance_vals(level)[insurance]))
			quints['insurance_level' + str(level)] = arr
		"""
		print quints['games_played']
		print quints['highest_level']
		print quints['minutes_played']
		print quints['research_time0']
		print quints['research_time1']
		print quints['research_time2']
		print quints['research_time3']
		print quints['research_time4']
		print quints['research_time5']
		print quints['protection_percent0']
		print quints['protection_percent1']
		print quints['protection_percent2']
		print quints['protection_percent3']
		print quints['protection_percent4']
		print quints['protection_percent5']
		"""
		return quints
		
	def create_quintile_from_key(self, key, index=-1):
		if index > -1:
			arr = self.get_key_arr_at_index(key, index)
		else:
			arr = self.get_key_arr(key)
		return self.create_quintile(arr)

	def get_key_arr(self, key):
		arr = []
		for p in self._profiles:
			arr.append(p[key])
		return arr

	def get_key_arr_at_index(self, key, index):
		arr = []
		for p in self._profiles:
			val = p[key][index]
			if val != 'n/a':
				arr.append(val)
		return arr

	def get_insurance_vals(self, level):
		arr = []
		arr.append([])
		arr.append([])
		arr.append([])
		for p in self._profiles:
			level_vals = p['insurances'][level]
			if level_vals == 'n/a':
				continue
			for i in range(3):
				arr[i].append(level_vals[i])
		return arr

	def create_quintile(self, data_arr):
		arr = np.array(data_arr)
		q = []
		for i in range(6):
			q.append(np.percentile(arr, i * 20))
		return q


profile_creator = ProfileCreator(create_profiles=True)
quintile_creator = QuintileCreator(profile_creator.get_profiles())

"""
profiles = quintile_creator.get_profiles()
csv_file = profile_creator.create_csv('rh-reflections-and-data-quintiles.csv')
for p in profiles:
	profile_creator.write_profile_to_csv_noclean(p, csv_file)
"""