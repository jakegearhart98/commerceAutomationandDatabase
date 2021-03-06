from lib2to3.pgen2 import driver
from webbrowser import Chrome
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import pandas as pd
from bs4 import BeautifulSoup
import time, os, pathlib
import requests
from bs4.dammit import EncodingDetector

def createURLExport(homeURL):
    class_identifier = "zg-grid-general-faceout"
    root_url = 'https://www.amazon.com'

    #Need to have this headers so Amazon thinks its a request from not python(bypass bot prevention)
    HEADERS = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
    response = requests.get(homeURL, headers = HEADERS)

    #here down is used to obtain links of each item in bestselling list
    soup = BeautifulSoup(response.text, 'html.parser')
    doc = soup.find_all(class_ = class_identifier)
    root = os.path.join('C:\\', 'Users', 'flake', 'Desktop', "amazonScraping")
    #print(root + os.path.join('\productNames_export.txt'))


    
    """
        URL from webpage gets parsed and that is the name, splits some and you get the name
        Name, price, and productURL gets written to csv file
    """
    with open((root + os.path.join('\productNames_export.csv')) ,'w') as writeFile:
        for product in doc:
            price = product.find(class_ = 'a-size-base a-color-price')
            
            link = product.find(href = True)
            productURL = root_url + link['href']
            nameParse = str(link['href']).split("/")
            nameParse = str(nameParse[1]).split("-")
            nameParse = " ".join(nameParse)

            #This prints the CSV file
            try:
                writeFile.write("%s, %s, %s\n" %(nameParse, price.text, productURL))
            except:
                price = "Click link for price"
                writeFile.write("%s, %s, %s\n" %(nameParse, price, productURL))

        
#end populate url_export.txt

createURLExport("https://www.amazon.com/Best-Sellers-Nintendo-Switch-Games/zgbs/videogames/16227133011")