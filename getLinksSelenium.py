import time
import pymongo
import hashlib

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import getThePdfLink as gpdf
import documentCrawler as dc

myclient = pymongo.MongoClient("mongodb://localhost/27017")

#Details of the DataA Database
mydb = myclient["DataA"]
myDocs = mydb["myDocs"]

#Details of the LastElements Database
LastEleCol = myclient["last_db"]
myLastElements = LastEleCol["LastElements"]

#The Details of the Links Database
linkdb = myclient["Links"]
unvisited = linkdb["unvisited"]
visited = linkdb["visited"]

myDocs.create_index([('url', pymongo.ASCENDING)])

#This opens the Selenium driver and Opens Firefox for webscraping
def StartWorkFromTasks(url):
    browser = webdriver.Firefox(executable_path=r'C:/Users/HP/Documents/Python Scripts/geckodriver.exe')
    browser.get(url)
    time.sleep(1)

    #This scrolls the webpage down
    elem = browser.find_element_by_tag_name("body")
    no_of_pagedowns = 200
    while no_of_pagedowns:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.2)
        no_of_pagedowns-=1

    # post_elems = browser.find_elements_by_class_name("badge-light")

    #The arrays to store the different type of links
    papers =[]
    tasks = []
    sotas = []
    otherLinks = []

    #Get all the links
    elems = browser.find_elements_by_xpath("//a[@href]")
    for elem in elems:
        
        href = elem.get_attribute("href")
        if(href.startswith('https://paperswithcode.com/paper/')):
            papers.append(href)

        elif(href.startswith('https://paperswithcode.com/task/') or href.startswith('https://paperswithcode.com/area/')):
            tasks.append(href)

        elif(href.startswith('https://paperswithcode.com/sota/')):
            sotas.append(href)

        else:
            otherLinks.append(href)

    papers = list(set(papers))
    tasks = list(set(tasks))

    #If the link contains "task" then we add it to the unvisited list to be parsed
    for task in tasks:
        result = str(hashlib.md5(task.encode()).hexdigest())
        if(visited.find({"_id": result}).count()<=0 and unvisited.find({"_id": result}).count()<=0):
            LinkDict  = {"Link": task, "_id": result}
            unvisited.insert_one(LinkDict)

    #If the link contains PDF link then we fetch the pdf Links and Add the Links to the Database
    for paper_url in papers:

        if(paper_url.endswith('.pdf')):
            pdfLink = gpdf.GetPdfLink(paper_url)
            if(len(pdfLink)>5 and myDocs.find({"url": pdfLink}).count()<=0):
                print('\n\n')
                print(pdfLink)
                dc.start(pdfLink)

        if(paper_url.endswith('.docx')):
            pass

        if(paper_url.endswith('.ppt')):
            pass


    browser.quit()

