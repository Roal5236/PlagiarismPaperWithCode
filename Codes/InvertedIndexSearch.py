# -*- coding: utf-8 -*-
"""
Created on Fri May 17 11:28:15 2019

@author: rohaa
"""
import time
import pymongo
from nltk.tokenize import word_tokenize
from collections import Counter
import Codes.documentCrawler as dc

def InvertedIndexSearch(UsersDocument):
    #Details of the database
    myclient = pymongo.MongoClient("mongodb://localhost/27017")
    mydb = myclient["DataA"]
    Diction = mydb["Diction"]

    #Reading the user's document
    raw = open(UsersDocument, "r", encoding='utf8', errors='ignore').read().lower()

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

    threshold=90
    i=1
    #Get an List of all documents relevant to a perticular keyword and Add to to ArrayOfMinDocuments
    for word in create_dict.keys():
        if(i<=threshold):
            diction_words = Diction.find({"Term": word})
            for row in diction_words:
                ArrayOfMinDocuments.extend(row["ARD"])
                break

        else:
            break
        i+=1

    #Calculate the number of documents with the most hits
    CountRelevantDocs = dc.create_dictionary(ArrayOfMinDocuments)

    #Convert the above Dictionary into a list
    finalDocArray=[]
    for docId in CountRelevantDocs.keys():
        finalDocArray.append(docId)

    return finalDocArray[0:50]

# #Start the time
# start = time.time()

# UsersDocument="Test_document.txt"
# print(InvertedIndexSearch(UsersDocument))

# #End Time
# end = time.time()
# print("Execution time:",end-start)
