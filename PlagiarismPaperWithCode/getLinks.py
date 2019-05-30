# -*- coding: utf-8 -*-
"""
Created on Fri May 17 17:47:42 2019

@author: rohaa
"""
import requests 
import os
from bs4 import BeautifulSoup 

def GetLinks(url): 
    unvisitedLinks = []
  
    # the website fetched from our web-crawler 
    source_code = requests.get(url).text 
  
    # BeautifulSoup object which will 
    soup = BeautifulSoup(source_code, 'html.parser') 
    
    #Get Links from an a tag
    for link in soup.findAll('a'):
        tempLink = str(link.get('href'))
        #Check if the link is of proper format
        if(tempLink.startswith('https://') or tempLink.startswith('/') or tempLink.startswith('http://')):
            
            if(tempLink.startswith('https://paperswithcode.com') or tempLink.startswith('http://paperswithcode.com')):
                    unvisitedLinks.append(tempLink)
                
            elif(tempLink.startswith('//')):
                pass
                
            else:
                #if the url has / then we need to append it to the base url
                urlSplit = url.split('/')
                linkSplit = tempLink.split('/')
                base_url= urlSplit[0]+'//'+urlSplit[2]
                if('paperswithcode.com' in base_url):
                    tempLink = base_url+'/'+linkSplit[len(linkSplit)-2]+'/'+linkSplit[len(linkSplit)-1]
                    unvisitedLinks.append(tempLink)
                
    print("Links fetched")
    #print(unvisitedLinks)
    
    return unvisitedLinks
