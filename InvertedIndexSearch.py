# -*- coding: utf-8 -*-
"""
Created on Fri May 17 11:28:15 2019

@author: rohaa
"""

import pymongo
import documentCrawler as dc
from nltk.tokenize import word_tokenize
from collections import Counter 
import documentCrawler as dc

def InvertedIndexSearch(UsersDocument):
    myclient = pymongo.MongoClient("mongodb://localhost/27017")
    mydb = myclient["DataA"]
    Posting = mydb["Posting"]
    Diction = mydb["Diction"]
    
    raw = open(UsersDocument).read().lower()
    
    #Tokenizing the words
    tokens = word_tokenize(raw)
    words = [w.lower() for w in tokens]
    
    #Remove stop words and Unnecessary Symbols
    removed_words = dc.remove_unnecessary(words)
    
    #lemmatizatoin of the words
    Lemma_list = dc.lemma_wordlist(removed_words)
    
    #Creates a dictionary with word and Word Frequency
    create_dict = dc.create_dictionary(Lemma_list)

    
    #We Get the array of all documents that contain a perticular keyword 
    """Need to do this based on min Doc Frequency"""
    ArrayOfMinDocuments = []
    
    threshold=100
    i=1
    for word,freq in create_dict.items():
        if(i<=threshold):
            diction_words = Diction.find({"Term": word})
            for row in diction_words:
                ArrayOfMinDocuments.extend(row["ARD"])
                break

        else:
            break
        i+=1
        

    CountRelevantDocs = dc.create_dictionary(ArrayOfMinDocuments)


    finalDocArray=[]
    for docId, docFreq in CountRelevantDocs.items():
        finalDocArray.append(docId)
    
    print(finalDocArray)
    return finalDocArray
    
UsersDocument = "Test_document.txt"
InvertedIndexSearch(UsersDocument)