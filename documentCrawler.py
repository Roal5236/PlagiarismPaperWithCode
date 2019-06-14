# -*- coding: utf-8 -*-
"""
Created on Mon May 20 10:42:54 2019

@author: rohaa
"""
from spacy.lemmatizer import Lemmatizer
from spacy.lang.en import LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES
from nltk.corpus import stopwords
import collections
import pymongo
import operator 
import getPdf as gp

myclient = pymongo.MongoClient("mongodb://localhost/27017")

#Database Info(Collection Name)
mydb = myclient["DataA"]
mycol = mydb["keywords"]
myDocs = mydb['myDocs']

LastEleCol = myclient["last_db"]
myLastElements = LastEleCol["LastElements"]

#Get the id of the Last Element Added
last=mycol.find({}).sort([("_id",-1)]).limit(1)


#Get the last value added to the database
if(last.count()>0):
    k = last[0]["_id"]+1
else:
    k=1
    
def start(url): 

    #Get the id of the Last Element Added
    last=mycol.find({}).sort([("_id",-1)]).limit(1)

    #Get the last value added to the database
    if(last.count()>0):
        k = last[0]["_id"]+1
    else:
        k=1

    #Get the words from the website
    #word_list = wc.start(url)
    
    #Calculate the path of the text file that will contain the information about PDF
    name = "X/"+str(k)+".txt"

    #Save the Pdf as a text file
    word_list = gp.save_pdf(url,name)
    

    
    if(len(word_list)>0):

        #Remove stop words and Unnecessary Symbols
        removed_words = remove_unnecessary(word_list)
        
        #lemmatizatoin of the words
        Lemma_list = lemma_wordlist(removed_words)
        
        #Creates a dictionary with word and Word Frequency
        create_dict = create_dictionary(Lemma_list) 
        
        #remove Irrelevant words(words with frequency less than 5)
        RemoveIWords = remove_Irrelevant_Words(create_dict)
        
        #Add the dictionary to the database
        add_database(RemoveIWords, url, k)
        
    
def add_database(word_dict, url, k):
    #Setting the Id
    word_dict["_id"]=k
    print("k="+str(k))

    #insert Into Database
    mycol.insert_one(word_dict)
    TempDocDict = {"_id": k, "url": url}
    myDocs.insert_one(TempDocDict)
    print("Row Added")
    
    #Append the last Value of the keywords 
    myquery = { "keywords": k }
    newvalues = { "$set": { "keywords": k+1 } }
    myLastElements.update_one(myquery, newvalues)
    
    

def remove_unnecessary(word_list):
    
    removed_symbols = []
    
    #List of stopwords from nltk
    stop_words = set(stopwords.words('english'))
    stop_words.add('')
    stop_words.add(' ')
    stop_words.add('/')
    stop_words.add('either')

    
    unnecessary_words = [w for w in word_list if not w in stop_words]

    #Removing Unnecessary Symbols
    for word in unnecessary_words: 
        symbols = '!@#$%^&*()_+={[}]|\;:"<>?/.,¿`ˆ•\'·'
          
        for i in range (0, len(symbols)): 
            word = word.replace('\x00','')
            word = word.replace(symbols[i], '+')
        
        if('+' in word):
            tempWordSplit = word.split('+')
            word = word.strip()
            for tempWords in tempWordSplit:
                tempWords = tempWords.replace('+', '')
                removed_symbols.append(tempWords)  

        else:
            if len(word) > 1: 
                removed_symbols.append(word.strip())

    # for word in removed_symbols:

        
    print('Symbols Removed')
    return removed_symbols



#counts the occurance of each word and creats a dictionary
def create_dictionary(word_list): 
    word_count = {} 
      
    for word in word_list: 
        if word in word_count: 
            word_count[word] += 1
        else: 
            word_count[word] = 1
        
            
    print('Dictionary Created')
    sorted_x = sorted(word_count.items(), key=operator.itemgetter(1),reverse = True)
    sorted_dict = collections.OrderedDict(sorted_x)
    return sorted_dict        


def remove_Irrelevant_Words(word_list):

    #This removes the words that have a frequency less than 5 and the length of the word is less than 2
    final_word_count={}
    for word in word_list:
        temp = word_list[word]
        if(temp>5 and len(word)>2):
            final_word_count[word]=temp

    return final_word_count


def lemma_wordlist(word_list):
    #This Lemmatizes the words 
    lemmatizer = lemmatizer = Lemmatizer(LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES)
    Lemma_list = []
    
    for word in word_list:
        lWord = lemmatizer(word, u"NOUN")
        Lemma_list.append(lWord[0])
        
    print("Words Lemmatized")
    return Lemma_list
    

