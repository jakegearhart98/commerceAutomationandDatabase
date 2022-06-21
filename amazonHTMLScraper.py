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
import pathlib

#This script scans the url_exports.txt file and outputs html data to be scanned
def getProductHTML():
    
    root = os.path.join('C:\\', 'Users', 'flake', 'Desktop', "amazonScraping")    
    url_list = open('url_export.txt').readlines()
    file_count = 0
    driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()))

    driver.get(url_list[0])
    time.sleep(2)

    for item in url_list:

        with open((root + os.path.join('\item_file_export\item%s.txt') %file_count), 'w') as html_file:
            driver.get(item)
            time.sleep(3)
            htmlSource = driver.page_source
            
            htmlSoup = BeautifulSoup(htmlSource, features = 'lxml')
            #returns the section that i want
            try:
                html_file.write(str(htmlSoup.find(id = 'centerCol')))
            except:
                pass
            
            #print(htmlSoup)
            file_count += 1
            #html_file.write(htmlSoup.find(id = 'mediaTabs_tabSetContainer'))

getProductHTML()
        