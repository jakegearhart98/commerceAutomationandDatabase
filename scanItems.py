import pandas as pd
from bs4 import BeautifulSoup
import time, os
import requests
import numpy as np
import pandas as pd
import productClass

def scanItemFiles():
    fileCount = 0

    #product = productClass.ProductObject("")
    column_names = ["Product Name"]

    """
    Opens files (name: item#.txt), scans the raw html and stores data into pandas dataframe
    """
    with open("name_and_price.txt", "w")  as writeFile:

        while (os.path.exists('item%s.txt' %fileCount)):
            with open('item%s.txt' %fileCount, 'r') as openFile:
                #print(html_Doc)
                soup = BeautifulSoup(openFile.read(), features = 'lxml')
                title = soup.find(id = "productTitle")
                price = soup.find(id = "priceblock_ourprice")

                """Output gets skipped if title or price is blank: Fix this issue later"""
                try:
                    writeFile.write("%s, %s\n" %((title.text).strip(), price.text))
                except:
                    pass
                
                fileCount += 1