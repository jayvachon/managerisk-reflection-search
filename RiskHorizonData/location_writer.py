
# grabs the ip addresses from the data and finds the locations of the players, then writes the locations to a json file

import json
from urllib2 import Request, urlopen, URLError

LOCAL = 0
AMAZON = 1

def getJSONData(path):
	print 'loading ' + path + '...'
	json_data = open(path)
	d = json.load(json_data)
	print path + ' loaded'
	return d

def getLocation(index):

	# get the original ip so we can cross-reference the other json file
	full_ip = data[index]['ipv4']

	# grab the local ip of the player
	ip = full_ip.split(',')[LOCAL]
	request = Request ('http://ipinfo.io/' + ip + '/json/?token=bdf69c1ca89ace')
	try:
		response = urlopen(request)
		read = response.read()
		location_data = json.loads(read)

		# these fields need to be encoded as utf-8 because they have characters outside the unicode range
		if 'city' in location_data:
			if location_data['city']:
				location_data['city'] = location_data['city'].encode('utf-8')
		if 'org' in location_data:
			if location_data['org']:
				location_data['org'] = location_data['org'].encode('utf-8')
		if 'country' in location_data:
			iso = location_data['country'].encode('utf-8')
			location_data['country_name'] = isoToCountryName(iso)
		
		# create an object with the full ip and location data
		d = {}
		d['ipv4'] = full_ip
		d['location'] = location_data
		return d
	except URLError, e:
		return [full_ip]

def getLocations():
	locations = []
	length = len(data)
	strlength = str(length)
	for i in range(length):
		print str(i) + ' of ' + strlength
		locations.append(getLocation(i))
	return locations

def writeLocationData(locations):
	location_data = {}
	location_data['locations'] = locations
	with open('locations.json', 'w') as f:
		json.dump(location_data, f, ensure_ascii = False, indent = 4)

def isoToCountryName(iso):
	for c in countries:
		if iso in c.values():
			return c['name']
	return "couldn't find \"" + iso + "\""

data = getJSONData('json_parser/data/risk_horizon.json')
countries = getJSONData('countries.json')

writeLocationData(getLocations())
