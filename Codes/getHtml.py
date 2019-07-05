# -*- coding: utf-8 -*-
"""
Created on Fri May 10 13:39:26 2019

@author: rohaa
"""

import requests 
from bs4 import BeautifulSoup 
from collections import Counter 
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pymongo
import re


def start(url, UserRelevantDoc): 
    
  
    source_code = requests.get(url).text 
    soup = BeautifulSoup(source_code, 'html.parser') 
    print("html fetched")
    
    
    File_object = open(UserRelevantDoc,"w+", encoding='utf8', errors='ignore')

    AllWords=[]
    Sentances = []

    text_returned=soup.findAll('p')
    if(len(text_returned) > 0):
        for each_text in text_returned:
            notag = re.sub("<.*?>", " ", str(each_text))
            content = notag.lower()
            Sentances.append(content)
            temp = content.split(' ')
            for each_word in temp:
                AllWords.append(each_word.strip())            
                   
    text_returned=soup.findAll('a')
    if(len(text_returned) > 0):
        for each_text in text_returned:
            notag = re.sub("<.*?>", " ", str(each_text))
            content = notag.lower()
            Sentances.append(content)
            temp = content.split(' ')
            for each_word in temp:
                AllWords.append(each_word.strip()) 
            
    text_returned=soup.findAll('h1')
    if(len(text_returned) > 0):
        for each_text in text_returned:
            notag = re.sub("<.*?>", " ", str(each_text))
            content = notag.lower()
            Sentances.append(content)
            temp = content.split(' ')
            for each_word in temp:
                AllWords.append(each_word.strip()) 
            
    text_returned=soup.findAll('h2')
    if(len(text_returned) > 0):
        for each_text in text_returned:
            notag = re.sub("<.*?>", " ", str(each_text))
            content = notag.lower()
            Sentances.append(content)
            temp = content.split(' ')
            for each_word in temp:
                AllWords.append(each_word.strip()) 
            
    text_returned=soup.findAll('h3')
    if(len(text_returned) > 0):
        for each_text in text_returned:
            notag = re.sub("<.*?>", " ", str(each_text))
            content = notag.lower()
            Sentances.append(content)
            temp = content.split(' ')
            for each_word in temp:
                AllWords.append(each_word.strip()) 
            
    text_returned=soup.findAll('h4')
    if(len(text_returned) > 0):
        for each_text in text_returned:
            notag = re.sub("<.*?>", " ", str(each_text))
            content = notag.lower()
            Sentances.append(content)
            temp = content.split(' ')
            for each_word in temp:
                AllWords.append(each_word.strip()) 
            
    text_returned=soup.findAll('h5')
    if(len(text_returned) > 0):
        for each_text in text_returned:
            notag = re.sub("<.*?>", " ", str(each_text))
            content = notag.lower()
            Sentances.append(content)
            temp = content.split(' ')
            for each_word in temp:
                AllWords.append(each_word.strip()) 
            
    text_returned=soup.findAll('h6')
    if(len(text_returned) > 0):
        for each_text in text_returned:
            notag = re.sub("<.*?>", " ", str(each_text))
            content = notag.lower()
            Sentances.append(content)
            temp = content.split(' ')
            for each_word in temp:
                AllWords.append(each_word.strip())  
                
    text_returned=soup.findAll('li')
    if(len(text_returned) > 0):
        for each_text in text_returned:
            notag = re.sub("<.*?>", " ", str(each_text))
            content = notag.lower()
            Sentances.append(content)
            temp = content.split(' ')
            for each_word in temp:
                AllWords.append(each_word.strip())  
                
    text_returned=soup.findAll('span')
    if(len(text_returned) > 0):
        for each_text in text_returned:
            notag = re.sub("<.*?>", " ", str(each_text))
            content = notag.lower()
            Sentances.append(content)
            temp = content.split(' ')
            for each_word in temp:
                AllWords.append(each_word.strip())  
       
    final_sent=''         
    for sent in Sentances:
        final_sent = final_sent+sent
        
    File_object.write(final_sent)
    
    File_object.close()
           
    return AllWords

