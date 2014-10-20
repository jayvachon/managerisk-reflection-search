
from __future__ import division
import json
import operator

class CountryDataParser:

	def __init__(self, locations_data):
		self.locations_data = locations_data
		self.countries = self.getCountries()
		# self.listCountriesByPlays()

	def getCountry(self, index):
		location = self.locations_data['locations'][index]['location']
		if self.isEmersonIP(index):
			return 'null'
		return location['country_name']

	def getCountries(self):
		countries = {}
		length = len(locations_data['locations'])
		for i in range(length):
			country = self.getCountry(i)
			if country == 'null':
				continue
			if country in countries:
				countries[country] += 1
			else:
				countries[country] = 1
		return countries

	def getCountryByIP(self, ip):
		locations = locations_data['locations']
		for i in range(len(locations)):
			location = locations[i]
			if location['ipv4'] == ip:
				return location['location']['country_name']
				
	def getCountryPlayerCount(self, country):
		return self.countries[country]

	def isEmersonIP(self, index):
		location = self.locations_data['locations'][index]['location']
		if 'org' in location:
			if location['country'] != 'US':
				return False
			return location['org'].find('Emerson College') > -1
		return False

	def sortCountries(self, countries):
		s = sorted(countries.items(), key=operator.itemgetter(1))
		return s[::-1]

	# Returns a list of countries organized by number of players
	def listCountriesByPlays(self):
		sortedCountries = self.sortCountries(self.getCountries())
		countryCount = len(sortedCountries)
		print str(countryCount) + ' countries'
		for c in sortedCountries:
			name = c[0]
			players = c[1]
			print name + ": " + str(players)

class GameDataParser:

	def __init__(self, game_data, countryDataParser):
		self.game_data = game_data
		self.countryDataParser = countryDataParser
		self.getHighestAverageLevelByCountry()

	def getHighestLevelByIP(self, index):
		sessions = game_data[index]['session']
		highestLevel = {}
		highestLevel['ip'] = game_data[index]['ipv4']
		highestLevel['level'] = 0
		for i in range(len(sessions)):
			levels = sessions[i]['levels']
			for j in range(len(levels)):
				level = levels[j]['level']
				if level > highestLevel['level']:
					highestLevel['level'] = level
		return highestLevel

	def getHighestLevelsByIP(self):
		highestLevels = []
		for i in range(len(game_data)):
			highestLevels.append(self.getHighestLevelByIP(i))
		return highestLevels

	def getHighestAverageLevelByCountry(self):

		# skip countries who had fewer than this many players
		minPlayerCount = 30

		# each player's highest level
		highestLevels = self.getHighestLevelsByIP()

		# an array of all countries with number of players
		countries = self.countryDataParser.getCountries()

		# make a dict with the total of max levels reached by all players in each country
		self.countriesLevels = {}
		for i in range(len(highestLevels)):
			player = highestLevels[i]
			ip = player['ip']
			level = player['level']
			country = self.countryDataParser.getCountryByIP(str(ip))
			if country in self.countriesLevels:
				self.countriesLevels[country] += level
			else:
				self.countriesLevels[country] = level
		
		# average the total^ with the number of players per country
		self.avgLevels = {}
		for c in countries:
			playerCount = self.countryDataParser.getCountryPlayerCount(c)
			if playerCount < minPlayerCount:
				continue
			avgLevel = self.countriesLevels[c] / playerCount
			self.avgLevels[c] = avgLevel

		self.avgLevels = sorted(self.avgLevels.items(), key=operator.itemgetter(1))
		self.avgLevels = self.avgLevels[::-1]
		for a in self.avgLevels:
			print str(a[0]) + ": " + str(a[1])
			

def getJSONData(path):
	print 'loading ' + path + '...'
	json_data = open(path)
	d = json.load(json_data)
	print path + ' loaded'
	return d

def sanitizeLocations():
	d = {}
	d['locations'] = []
	locations = locations_data['locations']
	for location in locations:
		if 'ipv4' in location:
			if 'location' in location:
				if 'city' in location['location']:
					d['locations'].append(location)
	return d

locations_data = getJSONData('locations.json')
locations_data = sanitizeLocations()

game_data = getJSONData('json_parser/data/risk_horizon.json')

cdp = CountryDataParser(locations_data)
gdp = GameDataParser(game_data, cdp)

