
# semantria login:
# https://semantria.com/users/james_vachon
#
# API Credentials:
# API Key: ad33d748-33e3-41fd-a0cb-73ecc84163dd
# API Secret: ec92e058-d980-49b6-a017-50c13891d274

from __future__ import print_function
import semantria
import uuid
import time
import json

serializer = semantria.JsonSerializer()

semantria_key = 'ad33d748-33e3-41fd-a0cb-73ecc84163dd'
semantria_secret = 'ec92e058-d980-49b6-a017-50c13891d274'

session = semantria.Session(semantria_key, semantria_secret)

def getJSONData(path):
	json_data = open(path)
	d = json.load(json_data)
	return d

def getReflectionResults(index):
	text = submissions_data['submissions'][index]['reflection'].encode('utf-8')
	doc = {"id": str(uuid.uuid4()).replace("-", ""), "text": text}
	status = session.queueDocument(doc)
	if status == 202:
		print("\"", doc["id"], "\" document queued successfully.", "\r\n")

	print(str(index), " of ", submissionsCount, "Retrieving your processed results...", "\r\n")
	time.sleep(2)
	# get processed documents 
	status = session.getProcessedDocuments()
	results.append(status)

def printReflectionData():
	for data in results:
		print(data.encode)
		# print document sentiment score
		print("Document ", data["id"], " Sentiment score: ", data["sentiment_score"], "\r\n")

		# print document themes
		if "themes" in data:
			print("Document themes:", "\r\n")
			for theme in data["themes"]:
				print("     ", theme["title"], " (sentiment: ", theme["sentiment_score"], ")", "\r\n")

		# print document entities
		if "entities" in data:
			print("Entities:", "\r\n")
			for entity in data["entities"]:
				print("\t", entity["title"], " : ", entity["entity_type"]," (sentiment: ", entity["sentiment_score"], ")", "\r\n")

submissions_data = getJSONData('submissions.json')

results = []
submissionsCount = len(submissions_data['submissions'])
for i in range(2):
	getReflectionResults(i)

printReflectionData()

"""
[{u'status': u'PROCESSED', 
u'sentiment_polarity': u'negative', 
u'auto_categories': 
	[{u'type': u'node', 
	u'strength_score': 0.8457163, 
	u'categories': 
		[
			{u'type': u'concept', 
			u'strength_score': 0.6421528, 
			u'title': u'Financial_risk'}, 
			
			{u'type': u'concept', 
			u'strength_score': 0.46245885, 
			u'title': u'Economics_of_uncertainty'}
		], 
		u'title': u'Business'},
	{u'type': u'node', 
	u'strength_score': 0.5455496, 
	u'title': u'Finance'}, 

	{u'type': u'node', 
	u'strength_score': 0.45502356, 
	u'title': u'Accounting'}], 
u'language': u'English', 
u'phrases': 
	[{u'sentiment_polarity': u'negative', 
	u'is_intensified': True, 
	u'title': u'stressful', 
	u'sentiment_score': -0.8325, 
	u'is_negated': False, 
	u'type': u'detected', 
	u'intensifying_phrase': u'how'}, 

	{u'sentiment_polarity': u'negative', 
	u'is_intensified': False, 
	u'title': u'disaster', 
	u'sentiment_score': -0.75, 
	u'is_negated': False, 
	u'type': u'detected'}, 

	{u'sentiment_polarity': u'negative', 
	u'is_intensified': False, 
	u'title': u'disasters', 
	u'sentiment_score': -0.75, 
	u'is_negated': False, 
	u'type': u'detected'}, 

	{u'sentiment_polarity': u'negative', 
	u'is_intensified': False, 
	u'title': u'crippling', 
	u'sentiment_score': -0.6, 
	u'is_negated': False, 
	u'type': u'detected'}, 

	{u'sentiment_polarity': u'negative', 
	'is_intensified': True, 
	u'title': u'disrepair', 
	u'sentiment_score': -0.6, 
	u'is_negated': False, 
	u'type': u'detected', 
	u'intensifying_phrase': u'and'}, 

	{u'sentiment_polarity': u'neutral', 
	u'type': u'possible', 
	u'title': u'real dilemna'}, 

	{u'sentiment_polarity': u'neutral', 
	u'type': u'possible', 
	u'title': u'not want'}, 

	{u'sentiment_polarity': u'neutral', 
	u'type': u'possible', 
	u'title': u'more relevant'}], 

u'topics': [{u'sentiment_polarity': u'neutral', 
	u'title': u'Disasters', 
	u'sentiment_score': -0.25988606, 
	u'hitcount': 0, 
	u'type': u'concept', 
	u'strength_score': 0.52147156}, 

	{u'sentiment_polarity': u'neutral', 
	u'title': u'Video Games', 
	u'sentiment_score': -0.051208798, 
	u'hitcount': 0, 
	u'type': u'concept', 
	u'strength_score': 0.4538635}, 

	{u'sentiment_polarity': u'neutral', 
	u'title': u'Education', 
	u'sentiment_score': -0.26267827, 
	u'hitcount': 1, 
	u'type': u'query', 
	u'strength_score': 0.0}], 

u'config_id': u'25425371-3dc0-4109-97c6-942efe9dabc1', 
u'summary': u'However, I realised that the psychology behind my fear and unwillingness to develop was crippling for the community and my ability to advance in the game... I can see that this would be a very real dilemna for communities around the world and contributes to the high levels of destruction and disrepair after natural disaster and other disasters... Risk management for me took the form of reluctance at first and then, after 3 attempts at the game, knowledge enhancement and insurance helped to increase development which in turn enhanced resources and the ability of the community to cope... ', 
u'themes': [{u'sentiment_polarity': u'positive', 
	u'is_about': True, 
	u'title': u'enhanced resources', 
	u'evidence': 7, 
	u'sentiment_score': 6.7599998, 
	u'strength_score': 3.1103878}, 

	{u'sentiment_polarity': u'positive', 
	u'is_about': True, 
	u'title': u'knowledge enhancement', 
	u'evidence': 7, 
	u'sentiment_score': 7.58628, 
	u'strength_score': 3.1103878}, 

	{u'sentiment_polarity': u'positive', 
	u'is_about': False, 
	u'title': u'positive impacts', 
	u'evidence': 7, 
	u'sentiment_score': 2.920083, 
	u'strength_score': 2.8198774}, 

	{u'sentiment_polarity': u'negative', 
	u'is_about': False, 
	u'title': u'common fear', 
	u'evidence': 7, 
	u'sentiment_score': -3.92, 
	u'strength_score': 2.5238097}, 

	{u'sentiment_polarity': u'negative', 
	u'is_about': False, 
	u'title': u'third attempt', 
	u'evidence': 7, 
	u'sentiment_score': -0.6971983, 
	u'strength_score': 2.5238097}], 
	u'sentiment_score': -0.10548397, 
	u'source_text': u'At first, as I will discuss later, I found that I was too afraid to build too many buildings, as the fear of re-building and the costs associated with this were more than I could outlay. \xa0However, I realised that the psychology behind my fear and unwillingness to develop was crippling for the community and my ability to advance in the game. \xa0I can see that this would be a very real dilemna for communities around the world and contributes to the high levels of destruction and disrepair after natural disaster and other disasters. \xa0After some time in the game I realised that building enhanced the community\u2019s resources and was necessary for development. \xa0Risk management for me took the form of reluctance at first and then, after 3 attempts at the game, knowledge enhancement and insurance helped to increase development which in turn enhanced resources and the ability of the community to cope. \xa0This knowledge and insurance increased my risk-taking and provided more confidence in the community\u2019s ability to withstand the impacts of the comets, should they hit. \xa0The power of knowledge and the positive impacts of protection and insurance enabled me to feel confident in developing the community and in their ability to work together and cope. \xa0After playing the game a number of times I realised it was necessary to construct homes in order to increase my points and to gain money in to the account. \xa0At first I was reluctant to develop ad I did not want the comets to destroy the community, however, this is a common fear and a reason why communities do not develop and flourish, and I realised this after my third attempt at the game. \xa0I decided of my community to develop I must put aside fear of destruction and put my resources in to researching the comets, developing the community and taking out insurance. \xa0Very powerful and informative messages came about from this game and I realised just how stressful and complicated development and risk management can truly be.\xa0If I was to add or change one element of this game to make it more relevant for my current location, I would add people in to the mix, as a way of increasing the need for responsible risk management and the urgency of smart decision-making and to increase the impact of the disaster. \xa0', 
	u'id': u'a7b8ba2f645a4c5f884a5622d019a6ed', u'language_score': 343.0}]

"""