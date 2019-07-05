# -*- coding: utf-8 -*-
"""
Created on Mon May 27 03:03:26 2019

@author: rohaa
"""

import docx2txt
from pathlib import Path
import requests

def readDocX(DocPath, UserDoc):

    text =  docx2txt.process(DocPath)

    File_object = open(UserDoc,"w+", encoding='utf8', errors='ignore')
    File_object.write(text)
    File_object.close()

    return text

def getDocX(url, UserDoc):
    the_book = requests.get(url, stream=True)
    with open("Pdfs/Temp.docx", 'wb') as f:
      for chunk in the_book.iter_content(1024 * 1024 *2):  # 5 MB chunks
        f.write(chunk)

    print("Download Complete")

    text=readDocX("Pdfs/Temp.docx",UserDoc)

    return text


# getDocX("https://hudoc.echr.coe.int/app/conversion/docx/?library=ECHR&id=001-176931&filename=CASE%20OF%20NDIDI%20v.%20THE%20UNITED%20KINGDOM.docx&logEvent=False","Pdfs/Hi.txt")

# url = "https://drive.google.com/open?id=1H-DN6Tiwn3jROzYdC0zjXZ0ckXgFQqBz"
# UserDoc = "Test_document"
# getDocX(url, UserDoc)
