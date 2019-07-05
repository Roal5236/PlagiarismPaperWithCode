# -*- coding: utf-8 -*-
"""
Created on Sat June 14 13:29:42 2019

@author: Rohaan
"""
import argparse
import re
import pymongo
import time
import sys

import Codes.InvertedIndexSearch as iis
import Codes.getPdf as gp
import Codes.getHtml as gh
import Codes.getDocX as gd
import Codes.getPpt as gppt
import Codes.cosine_sim as cs
import Codes.break_sent as bs

from difflib import SequenceMatcher
from simhash import Simhash


#Start the time
start = time.time()

#Details of the Database
myclient = pymongo.MongoClient("mongodb://localhost/27017")
mydb = myclient["DataA"]
docsCol = mydb["myDocs"]

#Converts the User Document to a text file
def ConvertUserDoc(UsersDocument):
    #Convert the User's Doc to txt file
    if(UsersDocument.endswith('.pdf')):
        gp.convert_pdf_to_txt(UsersDocument,'Test_document.txt')

    elif(UsersDocument.endswith('.docx')):
        gd.readDocX(UsersDocument,'Test_document.txt')

    elif(UsersDocument.endswith('.pptx')):
        gppt.convert_ppt2txt(UsersDocument, 'Test_document.txt')

    elif(UsersDocument.endswith('.txt')):
        pass

    else:
        gh.start(UsersDocument, 'Test_document.txt')

# Downloads all the relevent Documents
def downloadAllDocs(CurrentReleventDoc, docsCol_url):

  #Relevant Documnet Path
  RelevantDocPath = "X/"+str(CurrentReleventDoc)+".txt"

  #Store the Document Data into a temp Text File
  if(docsCol_url.endswith('.pdf')):
      gp.save_pdf(docsCol_url,RelevantDocPath)

  if(docsCol_url.endswith('.docx')):
      gd.getDocX(docsCol_url,RelevantDocPath)

  else:
      gh.start(docsCol_url, RelevantDocPath)

# Read the document and breaks the document
def process_file(fileRelevantDocPath):

    #Number of Characters of the Substring
    CharacterSubStringNo=20

    #Using Anish/Ananya's Code to Get Sentences
    Sentences = bs.sentsplit(open(fileRelevantDocPath, "r", encoding='utf8', errors='ignore').read())

    kMers = {}
    Sentences2=[]
    for i in range(0,len(Sentences)):
        #Seperate into sentences for every \n\n
        if('\n\n' in Sentences[i]):
            temp = Sentences[i].split('\n\n')
            for x in temp:
                #Remove all new lines
                line2= re.sub("\n|\r", " ", x)
                Sentences2.append(line2)

        #Remove all new lines
        else:
            line= re.sub("\n|\r", " ", Sentences[i])
            Sentences2.append(line)

        if('•\t' in Sentences[i]):
            temp = Sentences[i].split('•\t')
            for x in temp:
                #Remove all new lines
                line2= re.sub("•\t", " ", x)
                Sentences2.append(line2)

    for j in range(0,len(Sentences2)):
        #Take parts of a sentence as keys with the sentence id as values
        for pos in range(len(Sentences2[j])-CharacterSubStringNo):
            kMers[Sentences2[j][pos:pos+CharacterSubStringNo]] = j


    return Sentences2, kMers

# Main Function that returns the plagiarised sentences
def sent_sim_main(UserDocumentPath):

    plagSentences = []
    DocPerc={}
    plaginfo={}


    # Reading user document and calling the function InvertedIndexSearch
    ListOfRelevantDocs = iis.InvertedIndexSearch('Test_document.txt')

    #Get all the Sentence from User's Document
    SentenceListOfUser, kMersListOfUser = process_file('Test_document.txt')


    #Count Number of plagiarized Sentences
    hitScore=0

    #Relevant documents are listed
    for i in range(0,len(ListOfRelevantDocs)-1):

        #Get the Url given the Relevant DocId from the database
        doc=docsCol.find({"_id":ListOfRelevantDocs[i]}).limit(1)
        docsCol_url = doc[0]["url"]
        docsCol_id = doc[0]["_id"]

        #Download the Current Relevent Document
        """downloadAllDocs(ListOfRelevantDocs[i], docsCol_url)"""

        #Path of relevant Doc
        RelevantDocPath = "X/"+str(ListOfRelevantDocs[i])+".txt"

        #Get the Sentences from the Relevant Document
        SentenceListOfRelevantDoc, kMersListOfRelevantDoc = process_file(RelevantDocPath)

        # Find common CharacterSubStringNo-mers(possible substrings)
        kMersSentenceId = []
        UniquekMersSentenceId = []
        """UnCommonKmers = []
        UnCommonKmersId = []"""

        #Compares the Keys(Parts of the sentence) of Relevant with User
        for kMersKeys,kMersVal in kMersListOfRelevantDoc.items():
            if(kMersKeys in kMersListOfUser):
                if(kMersVal not in UniquekMersSentenceId):
                    kMersSentenceId.append([kMersVal,kMersListOfUser[kMersKeys]])
                    UniquekMersSentenceId.append(kMersVal)
            """else:
                UnCommonKmers.append(kMersKeys)
                UnCommonKmersId.append(kMersVal)"""

        BoolUrl = True
        DocumentPlag=0

        #All the Common Sentence's Respective Id is Compared
        for j in range(0,len(kMersSentenceId)):

            #Similarity Between the Relevent and user's Sentence
            score = SequenceMatcher(None, SentenceListOfRelevantDoc[kMersSentenceId[j][0]], SentenceListOfUser[kMersSentenceId[j][1]]).ratio()

            #Threshold for Sentence similarity
            if(score >0.8):

                plagSentences.append(kMersSentenceId[j][1])
                plaginfo[kMersSentenceId[j][1]]=[docsCol_url,SentenceListOfRelevantDoc[kMersSentenceId[j][0]]]

                hitScore+=1
                DocumentPlag+=1


        if(DocumentPlag > 0):
          DocPerc[docsCol_url]=DocumentPlag


    FinalUserSentence={}
    for hm in range(0, len(SentenceListOfUser)):
        if(hm in plagSentences):
            FinalUserSentence[hm]=[SentenceListOfUser[hm],"plag",plaginfo[hm][0],plaginfo[hm][1]]
        else:
            FinalUserSentence[hm]=[SentenceListOfUser[hm],"notplag","none", "none"]


    #Percentage of Plagiarism
    Perc = (hitScore/len(SentenceListOfUser))*100
    print("Total Plagiarism Percentage = "+str((int)(Perc))+"%")

    #End Time
    end = time.time()
    print("Execution time:",end-start)

    return Perc, FinalUserSentence, DocPerc
