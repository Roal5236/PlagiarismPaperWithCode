import requests
import pymongo
import warnings
import hashlib 

from bs4 import BeautifulSoup

import getLinks as gl
import getLinksSelenium as gls
import remove_reset as rr



warnings.filterwarnings("ignore",category=DeprecationWarning)

#Reset The Database
#rr.remove_dataBases()
#rr.reset_last()

myclient = pymongo.MongoClient("mongodb://localhost/27017")

 #The Details of the Links Database
linkdb = myclient["Links"]
unvisited = linkdb["unvisited"]
visited = linkdb["visited"]

#Details of the Last Elements
LastEleCol = myclient["last_db"]
myLastElements = LastEleCol["LastElements"]


#Create indexs for the encoded links for both visited and unvisited collections
unvisited.create_index([('_id', pymongo.ASCENDING)])
visited.create_index([('_id', pymongo.ASCENDING)])

#Check if the unvisited Collection is empty
if(unvisited.find({}).count()<=0):
    startz = "https://paperswithcode.com/sota"
    
    #Get the links from the base Link
    Links = gl.GetLinks(startz)
    
    #Add each Link to the Unvisited Collection
    for link in Links:
        result = str(hashlib.md5(link.encode()).hexdigest())
        if(visited.find({"_id": result}).count()<=0 and unvisited.find({"_id": result}).count()<=0):
            LinkDict  = {"Link": link, "_id": result}
            unvisited.insert_one(LinkDict)
    
#Get the last thing added to the database
GetLastElements = myLastElements.find({})
i= GetLastElements[0]["keywords"]


#Get all the links in the unvisited collection
print("Enter into the Unvisited Loop")

while(unvisited.find({}).count()>0):
    tempUnvisited = unvisited.find({})

    for LinkDict2 in tempUnvisited:

        #Check if the link is there in the visited table
        if(visited.find({"_id": LinkDict2["_id"]}).count()<=0):
            print("\n\n")
            print("Current Link Number = "+str(i))

            #Add the keywords to database
            if(LinkDict2["Link"].startswith('https://paperswithcode.com/task/')):
                gls.StartWorkFromTasks(LinkDict2["Link"])
            
            #Add the new Links to the unvisited List
            Links = gl.GetLinks(LinkDict2["Link"])

            for link in Links:
                result = str(hashlib.md5(link.encode()).hexdigest())

                if(visited.find({"_id": result}).count()<=0 and unvisited.find({"_id": result}).count()<=0):
                    NewLinkDict  = {"Link": link, "_id": result}
                    unvisited.insert_one(NewLinkDict)
                    
            print("Sucessfully Inserted "+str(len(Links))+" New Links")

            #Add to Visited Links
            print(LinkDict2["Link"])
            visited.insert_one(LinkDict2)
                
            #Remove from Unvisited Links
            result2 = str(hashlib.md5(LinkDict2["Link"].encode()).hexdigest())
            myquery = {"Link": LinkDict2["Link"], "_id": result2}
            unvisited.delete_one(myquery) 
            
            
        else:
            print("Already Present In Visited Links")
        
        i+=1
            
        print(tempUnvisited.count())
            # if(i>1):
            #     break