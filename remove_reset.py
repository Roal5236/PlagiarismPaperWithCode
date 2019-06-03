import pymongo




def reset_last():
    
    myclient = pymongo.MongoClient("mongodb://localhost/27017")

    LastEleCol = myclient["last_db"]
    myLastElements = LastEleCol["LastElements"]

    mydb = myclient["DataA"]
    mycol = mydb["keywords"]
    
    if(mycol.find({}).count()<=0):
  
        #Get the last value added to the database
        GetLastElements = myLastElements.find({})
        keywordsValue = GetLastElements[0]["keywords"]
        postingValue = GetLastElements[0]["posting"]

        #Reset the last Value of the keywords 
        myquery = { "keywords": keywordsValue, "posting": postingValue }
        newvalues = { "$set": { "keywords": 1, "posting": 1 } }
        myLastElements.update_one(myquery, newvalues)

        print("LastElemnets Reseted")
        
#Drop the databases    
def remove_dataBases():

    myclient = pymongo.MongoClient("mongodb://localhost/27017")

    myclient.drop_database('Links')  
    myclient.drop_database('DataA')    

    print("Databases Removed")