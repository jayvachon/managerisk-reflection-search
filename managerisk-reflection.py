import os
import HTMLParser
import json

# These functions navigate the directory to find the submissions and evaluations
def getSubmissions(root):
	listing = os.listdir(root)
	submitters = getSubmitters(root, listing)
	submissions = []
	for s in submitters:
		submissions.append(getSubmission(s))
	return submissions

def getSubmitters(root, listing):
	submitters = []
	for infile in listing:
		path = root + infile
		submitters.append(path)
	return submitters

def getSubmission(path):
	sub = os.listdir(path)
	newPath = path + '/' + sub[0]
	submission = ""
	content = []
	if os.path.exists(newPath):
		submission = os.listdir(newPath)
	for infile in submission:
		content.append(newPath + '/' + infile)
	return content

# Grab the content from the submissions for parsing
def getReflection(submission):
	length = len(submission)
	return submission[length - 1]

def getEvaluations(submission):
	length = len(submission)
	# early exit if no evaluations were submitted
	if length < 2:
		return []
	evals = []
	for f in range(0, length - 1):
		evalFolder = os.listdir(submission[f])
		for infile in evalFolder:
			evals.append(submission[f] + '/' + infile)
	return evals

# Parse the content
class ReflectionParser(HTMLParser.HTMLParser):
	def __init__(self):
		HTMLParser.HTMLParser.__init__(self)
		self.recording = 0
		self.data = []

	def handle_starttag(self, tag, attrs):
		if tag == 'title':
			self.recording = 1
		elif tag == 'div':
			for name, value in attrs:
				if value == 'field-value':
					self.recording = 1

	def handle_endtag(self, tag):
		if tag == 'title':
			self.recording -= 1
		if tag == 'div' and self.recording:
			self.recording -= 1

	def handle_data(self, data):
		if self.recording:
			self.data.append(data)

class EvaluationParser(HTMLParser.HTMLParser):
	def __init__(self):
		HTMLParser.HTMLParser.__init__(self)
		self.recording = 0
		self.data = []

	def handle_starttag(self, tag, attrs):
		if tag != 'div':
			return
		for name, value in attrs:
			self.recording = 1

	def handle_endtag(self, tag):
		if tag == 'div' and self.recording:
			self.recording -= 1

	def handle_data(self, data):
		if self.recording:
			self.data.append(data)

def FormatSubmissionToJSON(submission):
	# reflection
	parser = ReflectionParser()
	f = open(getReflection(submission))
	p = f.read()
	parser.feed(p)
	reflection = parser.data[1]

	# evaluation
	parser = EvaluationParser()
	f = open(getEvaluations(submission)[1])
	p = f.read()
	parser.feed(p)
	evaluation = parser.data

	print(evaluation)

	data = {
		"reflection": reflection,
		"evaluation": {
			"clarity": evaluation[1],
			"comprehension": evaluation[3],
			"reflection": evaluation[5],
			"comments": evaluation[7]
		}
	}
	return data


submissions = getSubmissions('assessment3/')

for s in submissions:
	data = FormatSubmissionToJSON(s)

with open('submissions.json', 'w') as f:
	json.dump(data, f)


