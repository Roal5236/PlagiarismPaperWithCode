import re
import nltk
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters, PunktLanguageVars

def sentsplit(text):
	punkt_param = PunktParameters()
	abbreviation = ['Mr', 'Mrs', 'Ms', 'Dr', 'Prof', 'Sir', 'Rev', 'Mx', 'M/s', 'pvt', 'ltd', 'llp', 'Jr', 'Sr', 'i.e', 'e.g', 'u.s.a', 'fig', 'Capt', 'Major', 'Lt', 'Col', 'Lady', 'Cpl', 'Gen', 'Gov', 'St', 'Sgt', 'Assoc', 'Corp', 'Dept', 'Dept', 'Inc', 'mr', 'mrs', 'ms', 'dr', 'prof', 'sir', 'rev', 'mx', 'm/s', 'pvt', 'ltd', 'llp', 'jr', 'sr', 'i.e', 'e.g', 'u.s.a', 'fig', 'capt', 'major', 'lt', 'col', 'lady', 'cpl', 'gen', 'gov', 'st', 'sgt', 'assoc', 'corp', 'dept', 'dept', 'inc']
	punkt_param.abbrev_types = set(abbreviation)
	tokenizer = PunktSentenceTokenizer(punkt_param)
	sentence=tokenizer.tokenize(text)

	return sentence
		
