
import json
import random
import string

# spell-check
import enchant
from subprocess import Popen, PIPE, STDOUT

# nltk
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import PunktSentenceTokenizer
from nltk.corpus import stopwords

#ngrams
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.collocations import TrigramCollocationFinder
from nltk.metrics import TrigramAssocMeasures

# stemming and lemmatizing
from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer

from nltk.corpus.reader import CategorizedPlaintextCorpusReader
from nltk.tag import DefaultTagger
from nltk.corpus import treebank


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

class TextHandler:

	_english_stops = []
	_enchant_dict = enchant.Dict

	def __init__(self, text=""):
		self.set_stopwords()
		self._enchant_dict = enchant.Dict("en_US")
		# print self.correct_spelling_aspell(self.tokenize_words(self.normalize_text(text)))
		# self.get_bigrams(text)
		# self.get_trigrams(text)
		# print self.stem_words(self.tokenize_words(self.normalize_text(text)))

	def set_stopwords(self):
		self._english_stops = set(stopwords.words('english'))

	def get_stopwords(self):
		return self._english_stops

	def normalize_text(self, text, to_lowercase=True, remove_digits=True, remove_punction=True):
		if to_lowercase:
			text = text.lower()
		if remove_digits:
			text = text.translate(None, string.digits)
		# TODO: this does nothing! the word tokenizer already removes punctuation, but it would be good to have it as an option
		if remove_punction:
			text = text.translate(string.maketrans("",""), string.punctuation)
		return text

	""" tokenizing """
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

	""" spell correction """
	# uses enchant
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

	# uses aspell (more accurate than enchant, but slower)
	def correct_spelling_aspell(self, words):
		correct_words = []
		count = 0
		word_count = len(words)
		for word in words:
			correct_words.append(self.apply_external(word))
			count += 1
			print str(count) + " of " + str(word_count)
		return correct_words

	def apply_external(self, msg):
		proc = Popen(
			['ruby', 'spell-correct.rb'],
			stdout=PIPE,
			stdin=PIPE,
			stderr=STDOUT)
		proc.stdin.write(msg)
		proc.stdin.close()
		result = proc.stdout.read()
		return(result)

	""" ngrams """
	def get_bigrams(self, full_text):
		# words = self.tokenize_words(self.normalize_text(full_text))
		# bcf = BigramCollocationFinder.from_words(words)
		# print bcf.nbest(BigramAssocMeasures.likelihood_ratio, 10)
		""" cached the top 10 because this function takes several minutes to run """
		return [('risk', 'management'), ('played', 'game'), ('real', 'life'), ('role', 'risk'), ('new', 'version'), ('protection', 'insurance'), ('first', 'time'), ('risk', 'horizon'), ('main', 'things'), ('long', 'term')]

	def get_trigrams(self, full_text):
		# words = self.tokenize_words(self.normalize_text(full_text))
		# tcf = TrigramCollocationFinder.from_words(words)
		# print tcf.nbest(TrigramAssocMeasures.likelihood_ratio, 10)
		""" cached the top 10 because this function takes several minutes to run """
		return [('role', 'risk', 'management'), ('preparation', 'risk', 'management'), ('risk', 'management', 'game'), ('represent', 'risk', 'management'), ('manage', 'risk', 'management'), ('risk', 'management', 'choices'), ('aspects', 'risk', 'management'), ('effective', 'risk', 'management'), ('risk', 'management', 'imagine'), ('preparing', 'risk', 'management')]

	""" stemming """
	def stem_words(self, words):
		porter = PorterStemmer()
		snowball = SnowballStemmer('english')
		wordnet = WordNetLemmatizer()
		stemmed_text = []
		for word in words:
			stemmed_text.append(porter.stem(word))
			# uncomment to try a different stemmer (snowball) or lemmatizer (wordnet)
			# stemmed_text.append(snowball.stem(word))
			# stemmed_text.append(wordnet.lemmatize(word))
		return stemmed_text

	def get_words(self, text, normalize=True, spell_correct=False, stem=False):
		if normalize:
			text = self.normalize_text(text)
		words = self.tokenize_words(text)
		if spell_correct:
			words = self.correct_spelling_aspell(words)
		if stem:
			words = self.stem_words(words)
		return words

	def get_sentences(self, text):
		return self.tokenize_sentences(text)

class Chunker:

	_tagger = DefaultTagger
	
	def __init__(self, words):
		self._tagger = DefaultTagger('NN')
		self.tag_words(words)

	def tag_words(self, words):
		print self._tagger.tag(words)

	def get_accuracy(self, sentences=[]):

		if sentences == []:
			test_sents = treebank.tagged_sents()[3000:]
		else:
			test_sents = sentences
		print self._tagger.evaluate(test_sents)

class CorporaHandler:

	_reader = CategorizedPlaintextCorpusReader

	def __init__(self):
		self.create_reader()

	def create_reader(self):
		self._reader = CategorizedPlaintextCorpusReader('.', r'corpora/effective_.*\.txt', cat_pattern=r'corpora/effective_(\w+)\.txt')

	def create_classifier(self):
		# TODO: Get bag of nonstop words
		lfeats = label_feats_from_corpus(self._reader, bag_of_non_stopwords)
		train_feats, test_feats = split_label_feats(lfeats, split=1.0)
		nb_classifier = NaiveBayesClassifier.train(train_feats)
		return nb_classifier

	def categorizeText(words, classifier):
      return classifier.classify(bag_of_non_stopwords(words))

submissions = SubmissionsHandler()
text_handler = TextHandler()
corpora_handler = CorporaHandler()


# text_handler = TextHandler(submissions.get_random_reflection())
# text_handler = TextHandler(submissions.get_reflection(0))
# text_handler = TextHandler(submissions.get_full_corpora())

# print text_handler.get_sentences(submissions.get_reflection(0))
# chunker = Chunker(text_handler.get_words(submissions.get_reflection(0), spell_correct=False, stem=False))
# chunker.get_accuracy(text_handler.get_sentences(submissions.get_reflection(0)))

