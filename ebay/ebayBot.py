from itertools import count
from lib2to3.pgen2 import driver
from webbrowser import Chrome
from numpy import product
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
import pandas as pd
from bs4 import BeautifulSoup
import time, os
from lxml import etree
from selenium.webdriver.chrome.options import Options

#driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()))
options = Options()
options.headless = True
#column_names = ["Product Name", "Amazon Price"]
ebayHomeURL = "https://www.ebay.com/"

df = pd.read_csv('productNames_export.csv')
df.columns = ["Product Name", "Amazon Price", "Product URL"]

#obtain length of columns of dataframe
dataFrameHeight = df.shape[0]


productDataColumnNames = ["Product Name", "Amazon Price", "eBay Average", "Percentage Sold", "Total Amount of Listings"]
productDataFrame = pd.DataFrame(columns = productDataColumnNames)

item_prices = []
#print(df.iloc[0][0])


driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()))
count = 1
driver.get(ebayHomeURL)

driver.find_element(By.ID, "gh-ac").send_keys(df.iloc[count][0], Keys.ENTER)
#time.sleep(2)
#clicks completed listing, only needs to be activated once at the beginning then ebay doesn't switch you out of that setting
completedItemsBar = driver.find_element(By.XPATH, "/html/body/div[5]/div[3]")
completedItemsBar.find_element(By.NAME, 'LH_Complete').click()

time.sleep(1)

######NEED TO START LOOP, COMPLETED LISTING IS CLICKED, HAVE LOOP BE BASED ON LENGTH OF PRODUCTdATAFRAME

def scanEbayPage(htmlPage):
    ##WORK ON THIS METHOD NEXT, SCAN EBAY PAGE AND GET ALL THE DATA, CALL THIS METHOD WITHIN WHILE LOOP
    pass


while count < dataFrameHeight:
    
    #this finds the search bar
    driver.find_element(By.ID, 'gh-ac').clear()
    driver.find_element(By.ID, 'gh-ac').send_keys(df.iloc[count][0], Keys.ENTER)
    time.sleep(0.5)
    ###################

    print('completed listing loading, starting your code')

    soup_level1 = BeautifulSoup(driver.page_source, 'html.parser')
    middleSection = soup_level1.find(id ='srp-river-results')
    itemList = middleSection.find_all("li", class_ = "s-item s-item__pl-on-bottom")
    
    for eachItem in itemList:
        dateSold = eachItem.find("span", class_='POSITIVE')
        try:
            print(dateSold.text)
        except:
            dateSold = False
            print(dateSold)
    #soup_level2 = BeautifulSoup(, 'html.parser')

    """
    for eachProduct in productCells:
        #print(eachProduct)
        soup = BeautifulSoup(eachProduct, '')
        print(soup)
    
    """

    """
    for eachProduct in productCells:
        #print(eachProduct.text + '\n\n')
        itemSold = eachProduct.find_element(By.CLASS_NAME, 's-item__title--tagblock ')
        dateSoldSection = itemSold.find_element(By.CLASS_NAME, 'POSITIVE')
        dateList = (dateSoldSection.text).split()
        del(dateList[0])
        dateSold = " ".join(dateList)
        print(dateSold)
        boolIemSold = True
    """

        #soldItemString.splitlines()
        #print(soldItemString[0])
    #print(productCell)
    #print(driver.find_element(By.ID, 'srp-river-main'))
    count += 1

    print(count)