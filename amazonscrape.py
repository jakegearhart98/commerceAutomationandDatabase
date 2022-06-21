from lib2to3.pgen2 import driver
from webbrowser import Chrome
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import pandas as pd
from bs4 import BeautifulSoup
import time, os
import requests
from bs4.dammit import EncodingDetector

def createURLExport(homeURL):
    #home_url = "https://www.amazon.com/Best-Sellers-Video-Games-Nintendo-Switch-Games/zgbs/videogames/16227133011/ref=zg_bs_nav_videogames_2_16227128011"
    class_identifier = "zg-grid-general-faceout"
    #driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()))
    root_url = 'https://www.amazon.com'
    #driver.get(home_url)

    #Need to have this headers so Amazon thinks its a request from not python(bypass bot prevention)
    HEADERS = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
    response = requests.get(homeURL, headers = HEADERS)
    #print(response.text)

    #here down is used to obtain links of each item in bestselling list
    soup = BeautifulSoup(response.text, 'html.parser')
    doc = soup.find_all(class_ = class_identifier)
    #titles = soup.find_all(class_ = 'a-link-normal') ##HAVE IT PRINT OUT [1] OF TITLES LIST
    #print(titles)
    #for products in titles:
    #    print(products.text)
    count = 0
    
    for product in doc:
        #with open
        link = product.find(href = True)
        productURL = root_url + link['href']
        nameParse = str(link['href']).split("/")
        count += 1
        print(nameParse[1])
        #print(link['href'])
        #print(productURL)
        #print(full_url)
        

   # f.close()
#end populate url_export.txt

createURLExport("https://www.amazon.com/Best-Sellers-Video-Games-Nintendo-Switch-Games/zgbs/videogames/16227133011/ref=zg_bs_nav_videogames_2_16227128011")