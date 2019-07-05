# -*- coding: utf-8 -*-
"""
Created on Sat June 03 13:29:42 2019

@author: Megha
"""
import time


import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import numpy as np
from pymongo import MongoClient
import Codes.documentCrawler as dc


#Tokenizing the whole document into tokens,removing stopwords and storing in dictionary
def process(filez):
	raw = open(filez, "r", encoding='utf8', errors='ignore').read().lower()
    
	#Tokenizing the words
	tokens = word_tokenize(raw)
	words = [w.lower() for w in tokens]

	#Remove stop words and Unnecessary Symbols
	removed_words = dc.remove_unnecessary(words)

	#lemmatizatoin of the words
	Lemma_list = dc.lemma_wordlist(removed_words)

	#Creates a dictionary with word and Word Frequency
	create_dict = dc.create_dictionary(Lemma_list)

	return create_dict


# using cosine similarity to compare the documents and find the cosine similarity,vector normalization
def cos_sim(a,b):
	dot_product = np.dot(a,b)
	norm_a = np.linalg.norm(a)
	norm_b = np.linalg.norm(b)
	return dot_product / (norm_a * norm_b)
 
def getSimilarity(dict1, dict2):
	all_words_list = []
	for key in dict1:
		all_words_list.append(key)
	for key in dict2:
		all_words_list.append(key)
	all_words_list_size = len(all_words_list)
	# print(all_words_list)

	v1 = np.zeros(all_words_list_size, dtype=np.int)
	v2 = np.zeros(all_words_list_size,dtype=np.int)
	i = 0
	for (key) in all_words_list:
		v1[i] = dict1.get(key, 0)
		v2[i] = dict2.get(key, 0)
		i = i + 1
	return cos_sim(v1,v2)

def cosine_sim(UsersDoc,TestDoc):
	print(TestDoc)
	dict1 = process(UsersDoc)
	dict2 = process(TestDoc)
	score = getSimilarity(dict1,dict2)
	if score > 0.7:
		print("score:",score)
		return True

	return False

