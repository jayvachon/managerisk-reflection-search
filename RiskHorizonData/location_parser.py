
import json
import operator

def getJSONData(path):
	json_data = open(path)
	d = json.load(json_data)
	return d

def getCountry(index):
	location = ""
	if 'location' in locations_data['locations'][index]:
		location = locations_data['locations'][index]['location']
		if 'country' in location:
			if isEmersonIP(index):
				return 'null'
			return locations_data['locations'][index]['location']['country']
	return 'null'

def getCountries():
	countries = {}
	length = len(locations_data['locations'])
	for i in range(length):
		country = getCountry(i)
		if country == 'null':
			continue
		if country in countries:
			countries[country] += 1
		else:
			countries[country] = 1
	return countries

def isEmersonIP(index):
	location = locations_data['locations'][index]['location']
	if 'org' in location:
		if location['country'] != 'US':
			return False
		return location['org'].find('Emerson College') > -1
	return False

def sortCountries(countries):
	s = sorted(countries.items(), key=operator.itemgetter(1))
	return s[::-1]

def isoToCountryName(iso):
	for c in countries_data:
		if iso in c.values():
			return c['name']
	return "couldn't find \"" + iso + "\""

# Returns a list of countries organized by number of players
def listCountriesByPlays():
	sortedCountries = sortCountries(getCountries())
	countryCount = len(sortedCountries)
	print str(countryCount) + ' countries'
	for c in sortedCountries:
		name = isoToCountryName(c[0])
		players = c[1]
		print name + ": " + str(players)
	

locations_data = getJSONData('locations.json')
countries_data = getJSONData('countries.json')

listCountriesByPlays()