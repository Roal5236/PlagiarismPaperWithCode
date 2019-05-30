import requests 
from bs4 import BeautifulSoup 

def GetPdfLink(url):
    source_code = requests.get(url).text 

    # BeautifulSoup object which will 
    soup = BeautifulSoup(source_code, 'html.parser') 
    
    #Get Links from an a tag
    for link in soup.findAll('a'):
        tempLink = str(link.get('href'))
        #Check if the link isof proper format
        if(tempLink.endswith('.pdf')):
            print("Pdf Link Fetched")
            return tempLink

    else:
        return "None"






