
import json

def write_reflection_to_text(submission):
	user_id = submission['user_id']
	filename = directory + user_id + ".txt"
	reflection = submission['reflection'].encode('utf-8')
	with open(filename, 'w') as f:
		f.write(user_id + '\n\n')
		f.write(reflection)

def write_reflections_to_text(submissions):
	for s in submissions:
		write_reflection_to_text(s)

reflections = json.load(open('submissions.json'))
directory = "reflections/"

write_reflections_to_text(reflections['submissions'])