import json
from urllib2 import Request, urlopen, URLError

"""

data to get:
-winning strategies?
-where people played
-how well people did depending on where they played
-how people played depending on where they played
-average sessions count
-how long people played for (time)

break data up into thirds
1. bottom 3rd
2. middle 3rd
3. upper 3rd
look at: geography, strategy

"""

LOCAL = 0
AMAZON = 1

def getJSONData():
	json_data = open('json_parser/data/risk_horizon.json')
	data = json.load(json_data)
	return data

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
		
		# create an object with the full ip and location data
		d = {}
		d['ipv4'] = full_ip
		d['location'] = location_data
		return d
	except URLError, e:
		return [full_ip]

def getLocations():
	locations = []
	# for i in range(len(data)):
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

print 'loading json data...'
data = getJSONData()
print 'data loaded'
writeLocationData(getLocations())
