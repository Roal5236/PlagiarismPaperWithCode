# -*- coding: utf-8 -*-
"""
Created on Tue May 21 21:25:38 2019

@author: rohaa
"""

import pymongo
import sys

def InvertedIndex():
    
    print("Building InvertedIndex")

    #Database Details
    myclient = pymongo.MongoClient("mongodb://localhost/27017")
    mydb = myclient["DataA"]
    mycol = mydb["keywords"]
    Diction = mydb["Diction"]
    
    #Create an Index for the "Term" in the Diction Table
    Diction.create_index([("Term", pymongo.ASCENDING)])

    #Get the last Element Indexed
    LastEleCol = myclient["last_db"]
    LastElements = LastEleCol["LastElements"]

    last=LastElements.find({}).limit(1)
    
    if(last.count()>0):
        last_posting_index = last[0]["posting"]
    else:
        last_posting_index=1
            
    #Variables to check if the Program is Running Properly
    CountTotalWords=0
    CountWordPresent=0
    CountWordsNotPresent=0
    CheckWordPresent=0
    CheckWordNotPresent=0

    #Get all the rows in the keyword database after the last entered index
    TotalNumDocumnets = mycol.find({"_id" : { "$gte": last_posting_index }})


    #Creating the InvertedIndex
    for word_dict in TotalNumDocumnets:

        for word, freq in word_dict.items():
            CountTotalWords+=1
            i=0 #Count for the number of doucments the word is present
            j=0 #Count for the Total frequency of the word in all documents
            TempF ={}

            #This is for updating the Array
            WordInDictionList=Diction.find({"Term": word})

            WordPresent = False
            if(WordInDictionList.count()>0):
                CountWordPresent+=1

                for x1 in WordInDictionList:
                    #print("The word Present is "+ x1["Term"])
                    ARD = x1["ARD"]
                    WordPresent = True

            else:
                #print("Nothing Found")
                CountWordsNotPresent+=1
                WordPresent = False
                ARD = []

            for n in mycol.find({},{word : 1}):
                if(len(n)>1):                    
                    i+=1
                    j+=n[word]
                    if(n["_id"] not in ARD):
                        ARD.append(n["_id"])

            if(i>0 and j>0):
                if(WordPresent):
                    #If the keyword is in the database then Update teh "ARD" array with the new document value
                    CheckWordPresent+=1
                    print("Updating Current Array")
                    IdofDocument = { "Term": word }
                    NewValueofDocument = { "$set": { "Docs": i, "Total": j, "ARD": ARD } }
                    Diction.update_one(IdofDocument, NewValueofDocument)
                
                else:
                    #If word not present then add the new keyword into the Diction Table
                    CheckWordNotPresent+=1
                    print("New Document Added")
                    TempF["Term"]=word
                    TempF["Docs"]=i
                    TempF["Total"]=j
                    TempF["ARD"]=ARD
                    Diction.insert_one(TempF)

        last_posting_index+=1

            

    print("Total number of words "+ str(CountTotalWords)+" present = "+str(CountWordPresent)+" not present = "+str(CountWordsNotPresent))
    print("Total number of words "+ str(CountTotalWords)+" CheckWordPresent = "+str(CheckWordPresent)+" CheckWordNotPresent = "+str(CheckWordNotPresent))

    #Update the last element Indexed in the LastElementsTable
    myquery = { "posting": last[0]["posting"] }
    newvalues = { "$set": { "posting": last_posting_index } }

    LastElements.update_one(myquery, newvalues)



InvertedIndex()
