
import json
import string
import csv

def getJSONData():
	json_data = open('submissions.json')
	data = json.load(json_data)
	return data

def getTitles():
	submissions = data['submissions']
	titles = []
	for submission in submissions:
		titles.append(submission['title'])
	return titles

def getUserIDs():
	ids = []
	for title in titles:
		# user_id_pos = string.find(title, 'coursera_user_id') + len('coursera_user_id: ')
		# user_id = str(title[user_id_pos:user_id_pos + 7])
		# if user_id.endswith(','):
		# 	user_id = user_id[:-1]
		# 	print user_id
		# TODO: Use this next line instead of all the shit above it
		# re.search('id: (.*), session', title).group(1)
		ids.append(user_id)
	ids_out = []
	ids_out.append(ids)
	return ids

data = getJSONData()
titles = getTitles()
ids = getUserIDs()

csv_file = open('user_ids.csv', 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["user_id"])
for i in range(len(ids)):
	csv_writer.writerow([ids[i]])
csv_file.close()