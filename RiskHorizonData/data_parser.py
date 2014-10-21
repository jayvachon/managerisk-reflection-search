
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
		self.playersHighestLevels = self.getPlayersHighestLevel()
		self.tierCounts = self.getTierCounts()
		# self.getHighestAverageLevelByCountry()
		# print self.getTimePlayedByIP(0)
		# print self.getPlayersHighestLevel()
		# self.getTimesPlayedByTier()
		self.getGameCountByTier()

	def getIPAtIndex(self, index):
		return game_data[index]['ipv4']

	def getSessionsAtIndex(self, index):
		return game_data[index]['session']

	def getFinalLevels(self):
		# returns an array of players' last levels
		levelCounts = [0, 0, 0, 0, 0, 0]
		for h in self.playersHighestLevels:
			levelCounts[h['level'] - 1] += 1
		return levelCounts

	def getTierCounts(self):
		finalLevels = self.getFinalLevels()
		return [finalLevels[0] + finalLevels[1], finalLevels[2] + finalLevels[3], finalLevels[4] + finalLevels[5]]

	def getTier(self, highestLevel):
		"""
		use this to divide players into 3 groups based on success in the game
		1 is bottom 3rd,
		2 is middle 3rd,
		3 is top 3rd
		"""
		if highestLevel < 3:
			return 1
		elif highestLevel < 5:
			return 2
		else:
			return 3

	def getPlayerHighestLevel(self, index):
		sessions = self.getSessionsAtIndex(index)
		highestLevel = {}
		highestLevel['ip'] = self.getIPAtIndex(index)
		highestLevel['level'] = 0
		for i in range(len(sessions)):
			levels = sessions[i]['levels']
			for j in range(len(levels)):
				level = levels[j]['level']
				if level > highestLevel['level']:
					highestLevel['level'] = level
		return highestLevel

	def getPlayersHighestLevel(self):
		# returns an array of players with the highest level they reached
		highestLevels = []
		for i in range(len(game_data)):
			highestLevels.append(self.getPlayerHighestLevel(i))
		return highestLevels

	def findPlayerHighestLevel(self, ip):
		for hl in self.playersHighestLevels:
			if hl['ip'] == ip:
				return hl['level']
		return 'ip ' + ip + ' not found'

	def getHighestAverageLevelByCountry(self):

		# skip countries who had fewer than this many players
		minPlayerCount = 30

		# an array of all countries with number of players
		countries = self.countryDataParser.getCountries()

		# make a dict with the total of max levels reached by all players in each country
		self.countriesLevels = {}
		for i in range(len(self.playersHighestLevels)):
			player = self.playersHighestLevels[i]
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

	def getTimePlayedByIP(self, index):
		# gets the total amount of time, in minutes, that a player played the game
		sessions = self.getSessionsAtIndex(index)
		timePlayed = {}
		timePlayed['ip'] = self.getIPAtIndex(index)
		time = 0
		levelDuration = 3 # minutes
		for i in range(len(sessions)):
			levels = sessions[i]['levels']
			for l in levels:
				time += levelDuration
 		
		timePlayed['time'] = time
		return timePlayed

	def getTimesPlayedByTier(self):
		plays = []

		# make an array with entries containing ip, tier, and total time played
		for i in range(len(game_data)):
			play = self.getTimePlayedByIP(i)
			level = self.findPlayerHighestLevel(play['ip'])
			play['tier'] = self.getTier(level)
			plays.append(play)

		# get the total time played by all players, per tier
		totalTierTime = [0, 0, 0]
		for p in plays:
			tier = p['tier']
			totalTierTime[tier - 1] += p['time']
			if p['time'] < 3:
				print p['time']

		# average out the total time over all players
		# tierCounts = self.tierCounts
		avgTimePlayedPerTier = []
		for i in range(3):
			avgTimePlayedPerTier.append(totalTierTime[i] / self.tierCounts[i])

		print avgTimePlayedPerTier

	def getGameCountByIP(self, index):
		sessions = self.getSessionsAtIndex(index)
		gamesPlayed = {}
		gamesPlayed['ip'] = self.getIPAtIndex(index)
		gameCount = 0
		for i in range(len(sessions)):
			levels = sessions[i]['levels']
			for l in levels:
				if l['level'] == 1:
					gameCount += 1

		# in case data from level 1s wasn't collected, count level 2s played
		if gameCount == 0:
			for i in range(len(sessions)):
				levels = sessions[i]['levels']
				for l in levels:
					if l['level'] == 2:
						gameCount += 1
		
		gamesPlayed['games'] = gameCount
		return gamesPlayed


	def getGameCountByTier(self):
		gameCounts = []

		for i in range(len(game_data)):
			gameCount = self.getGameCountByIP(i)
			level = self.findPlayerHighestLevel(gameCount['ip'])
			gameCount['tier'] = self.getTier(level)
			gameCounts.append(gameCount)

		totalGameCounts = [0, 0, 0]
		for gc in gameCounts:
			tier = gc['tier']
			totalGameCounts[tier - 1] += gc['games']
			if gc['games'] == 0:
				print gc['ip'] + " " + str(gc['games'])

		avgGameCountPerTier = []
		for i in range(3):
			avgGameCountPerTier.append(totalGameCounts[i] / self.tierCounts[i])

		print avgGameCountPerTier



def getJSONData(path):
	print 'loading ' + path + '...'
	json_data = open(path)
	d = json.load(json_data)
	print path + ' loaded'
	return d

def sanitizeLocationData():
	d = {}
	d['locations'] = []
	locations = locations_data['locations']
	for location in locations:
		if 'ipv4' in location:
			if 'location' in location:
				if 'city' in location['location']:
					d['locations'].append(location)
	return d

def sanitizeGameData():
	g = []
	emptySessionCount = 0
	for i in range(len(game_data)):
		session = game_data[i]['session']
		
		# removes players who were not able to play the game
		# or where data was not collected
		sessionCount = len(session)
		for s in range(sessionCount):
			levels = session[s]['levels']
			if len(levels) > 0:
				hasLevel1 = False
				for l in levels:
					if l['level'] == 1:
						g.append(game_data[i])
						hasLevel1 = True
						break
				if hasLevel1 == False:
					emptySessionCount += 1	
				break
			elif s == sessionCount - 1:
				emptySessionCount += 1
		
	print str(emptySessionCount) + " empty sessions"
	return g

locations_data = getJSONData('locations.json')
locations_data = sanitizeLocationData()

game_data = getJSONData('json_parser/data/risk_horizon.json')
game_data = sanitizeGameData()

cdp = CountryDataParser(locations_data)
gdp = GameDataParser(game_data, cdp)

