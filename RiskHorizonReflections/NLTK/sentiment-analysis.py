
# take 2

import json
import random
import string

# spell-check
# TODO: use aspell instead of pyenchant
import enchant

# nltk
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import PunktSentenceTokenizer
from nltk.corpus import stopwords
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.collocations import TrigramCollocationFinder
from nltk.metrics import TrigramAssocMeasures

class SubmissionsHandler:

	_data = {}
	_submissions = []

	def __init__(self):
		json_data = open('../submissions.json')
		self._data = json.load(json_data)
		self._submissions = self._data['submissions']
	
	def get_submissions_count(self):
		return len(self._submissions)

	def get_reflection(self, index):
		return self._submissions[index]['reflection'].encode('ascii', 'ignore')

	def get_random_reflection(self):
		return self.get_random_reflections(1)[0]

	def get_random_reflections(self, count):
		submissions_count = self.get_submissions_count()
		random_ints = []
		reflections = []
		
		for i in range(count):

			# get a unique random number
			r = random.randint(0, submissions_count-1)
			while r in random_ints:
				r = random.randint(0, submissions_count-1)
			
			# get the reflection at this index
			random_ints.append(r)
			reflections.append(self.get_reflection(r))

		return reflections

	def get_full_corpora(self):
		reflections = ""
		for i in range(self.get_submissions_count()-1):
			reflections += self.get_reflection(i)
		return reflections

class NoiseReducer:

	_english_stops = []
	_enchant_dict = enchant.Dict

	def __init__(self, text):
		self.set_stopwords()
		self._enchant_dict = enchant.Dict("en_US")
		# print self.correct_spelling(self.tokenize_words(self.normalize_text(text)))
		# self.get_bigrams(text)
		self.get_trigrams(text)

	def set_stopwords(self):
		self._english_stops = set(stopwords.words('english'))

	def get_bigrams(self, full_text):
		"""
		cached the top 10 because this function takes several minutes to run
		"""
		# words = self.tokenize_words(self.normalize_text(full_text))
		# bcf = BigramCollocationFinder.from_words(words)
		# print bcf.nbest(BigramAssocMeasures.likelihood_ratio, 10)
		return [('risk', 'management'), ('played', 'game'), ('real', 'life'), ('role', 'risk'), ('new', 'version'), ('protection', 'insurance'), ('first', 'time'), ('risk', 'horizon'), ('main', 'things'), ('long', 'term')]

	def get_trigrams(self, full_text):
		"""
		cached the top 10 because this function takes several minutes to run
		"""
		# words = self.tokenize_words(self.normalize_text(full_text))
		# tcf = TrigramCollocationFinder.from_words(words)
		# print tcf.nbest(TrigramAssocMeasures.likelihood_ratio, 10)
		return [('role', 'risk', 'management'), ('preparation', 'risk', 'management'), ('risk', 'management', 'game'), ('represent', 'risk', 'management'), ('manage', 'risk', 'management'), ('risk', 'management', 'choices'), ('aspects', 'risk', 'management'), ('effective', 'risk', 'management'), ('risk', 'management', 'imagine'), ('preparing', 'risk', 'management')]

	def normalize_text(self, text, to_lowercase=True, remove_digits=True, remove_punction=True):
		if to_lowercase:
			text = text.lower()
		if remove_digits:
			text = text.translate(None, string.digits)
		# TODO: this does nothing! the word tokenizer already removes punctuation, but it would be good to have it as an option
		if remove_punction:
			text = text.translate(string.maketrans("",""), string.punctuation)
		return text

	def tokenize_words(self, text, ignore_stopwords=True):
		# considers contractions and words joined by a dash ("-") to be single words
		word_tokenizer = RegexpTokenizer("[\w']+[\w-]+")
		words = word_tokenizer.tokenize(text)
		if ignore_stopwords:
			words = [word for word in words if word not in self._english_stops]
		return words
	
	def tokenize_sentences(self, text):
		sent_tokenizer = PunktSentenceTokenizer(text)
		return sent_tokenizer.tokenize(text)

	def correct_spelling(self, words):
		correct_words = []
		for word in words:
			if self._enchant_dict.check(word):
				correct_words.append(word)
			else:
				suggestions = self._enchant_dict.suggest(word)
				if (len(suggestions) > 0):
					correct_words.append(suggestions[0])
				else:
					correct_words.append(word)
		return correct_words

submissions = SubmissionsHandler()
# noise_reducer = NoiseReducer(submissions.get_random_reflection())
# noise_reducer = NoiseReducer(submissions.get_reflection(0))
noise_reducer = NoiseReducer(submissions.get_full_corpora())


