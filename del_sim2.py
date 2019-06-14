# -*- coding: utf-8 -*-
"""
Created on Sat June 14 13:29:42 2019

@author: Rohaan
"""
import argparse
from difflib import SequenceMatcher
import InvertedIndexSearch as iis
import getPdf as gp
import getPPT as gppt
import getHtml as gh
import getDocX as gd
import cosine_sim as cs
import re
import pymongo
import time
import sys
from difflib import SequenceMatcher
import break_sent as bs
from simhash import Simhash
import re
import nltk
from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet as wn

#Start the time
start = time.time()

#Details of the Database
myclient = pymongo.MongoClient("mongodb://localhost/27017")
mydb = myclient["DataA"]
docsCol = mydb["myDocs"]


# Read the document and breaks the document 
def process_file(fileRelevantDocPath):

    Sentences = bs.sentsplit(open(fileRelevantDocPath, "r", encoding='utf8', errors='ignore').read())
    print("Number of Sentences = "+str(len(Sentences)))
    kMers = {}
    Sentences2=[]
    for i in range(0,len(Sentences)):
        line= re.sub("\n|\r", " ", Sentences[i])
        Sentences2.append(line)
        for pos in range(len(line)-k):
            kMers[line[pos:pos+k]] = i

        
    return Sentences2, kMers

if __name__=='__main__':

    # #Arguments for similarity parameter
    UsersDocument = sys.argv[1]
    k=20

    print("User's Document is = "+str(UsersDocument))

    """#Convert the User's Doc to txt file
    if(UsersDocument.endswith('.pdf')):
        gp.convert_pdf_to_txt(UsersDocument,'Test_document.txt')

    if(UsersDocument.endswith('.docx')):
        gd.readDocX(UsersDocument,'Test_document.txt')

    # if(UsersDocument.endswith('.ppt')):
    #     gppt.getPPt(docsCol_url,UsersDocument)

    # else:
    #     gh.start(docsCol_url, 'Test_document.txt')"""

    # # Reading user document and calling the function InvertedIndexSearch
    ListOfRelevantDocs = iis.InvertedIndexSearch('Test_document.txt')
    print(ListOfRelevantDocs)

    noDocsScan=20

    #Checking the User's document for document similarity
    for i in range(0,len(ListOfRelevantDocs)-1):

        if(i>=noDocsScan):
            break

        #Get the Url given the Relevant DocId from the database
        doc=docsCol.find({"_id":ListOfRelevantDocs[i]}).limit(1)
        docsCol_url = doc[0]["url"]
        docsCol_id = doc[0]["_id"]


        RelevantDocPath = "X/"+str(ListOfRelevantDocs[i])+".txt"
        # print(RelevantDocPath)

        """#Store the Document Data into a temp Text File
        if(docsCol_url.endswith('.pdf')):
            gp.save_pdf(docsCol_url,RelevantDocPath)

        if(docsCol_url.endswith('.docx')):
            gd.getDocX(docsCol_url,RelevantDocPath)

        # if(docsCol_url.endswith('.ppt')):
        #     gppt.getPPt(docsCol_url,RelevantDocPath)

        # else:
        #     gh.start(docsCol_url, RelevantDocPath)"""


        #Calculate Cosine Similarity for Document
        if(cs.cosine_sim('Test_document.txt',RelevantDocPath)):
            print("Docs are similar no Need for Sentance Check")  
            #sys.exit()
            break
        else:
            print("Docs are not similar")

    print("Further Sentence Checking Required")

    #Get all the Sentence from User's Document
    SentenceListOfUser, kMersListOfUser = process_file('Test_document.txt')

    #Relevant documents are listed  
    for i in range(0,len(ListOfRelevantDocs)-1):

        if(i>=noDocsScan):
            break

        RelevantDocPath = "X/"+str(ListOfRelevantDocs[i])+".txt"
        print(RelevantDocPath)

        #Get the Sentences from the Relevant Document
        SentenceListOfRelevantDoc, kMersListOfRelevantDoc = process_file(RelevantDocPath)

        # Find common k-mers(possible substrings)
        kMersSubStrings = []
        kMersSentenceId = []    
        UniquekMersSentenceId = []
        UnCommonKmers = []
        UnCommonKmersId = []

        for kMersKeys,kMersVal in kMersListOfRelevantDoc.items():
            if(kMersKeys in kMersListOfUser):
                if(kMersVal not in UniquekMersSentenceId):
                    kMersSentenceId.append([kMersVal,kMersListOfUser[kMersKeys]])
                    UniquekMersSentenceId.append(kMersVal)
                    kMersSubStrings.append(kMersKeys)
            else:
                UnCommonKmers.append(kMersKeys)
                UnCommonKmersId.append(kMersVal)

        # for x in kMersSubStrings.items():
        #     print(x)

        hitScore=0
        for j in range(0,len(kMersSentenceId)):
            
            score = SequenceMatcher(None, SentenceListOfRelevantDoc[kMersSentenceId[j][0]], SentenceListOfUser[kMersSentenceId[j][1]]).ratio()

            if(score >0.8):
                print("Rele Doc: "+str(SentenceListOfRelevantDoc[kMersSentenceId[j][0]])+" "+str(kMersSentenceId[j][0]))
                print("User Doc: "+str(SentenceListOfUser[kMersSentenceId[j][1]])+" "+str(kMersSentenceId[j][1]))
                print(str(score)+"\n ++++++++++++ \n")
                hitScore+=1

    Perc = (hitScore/len(SentenceListOfUser))*100
    print("Plagiarism Percentage = "+str(Perc)+"%")
    # for x in UnCommonKmers:
    #     print(x)

#End Time
end = time.time()
print("time:",end-start)