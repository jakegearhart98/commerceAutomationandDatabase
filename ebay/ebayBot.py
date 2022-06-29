from doctest import master
from itertools import count
from lib2to3.pgen2 import driver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
from pandas import concat
from bs4 import BeautifulSoup
import time, os
from selenium.webdriver.chrome.options import Options

options = Options()
options.headless = True

root = os.path.join('C:\\', 'Users', 'flake', 'Desktop', "amazonScraping")
#column_names = ["Product Name", "Amazon Price"]
ebayHomeURL = "https://www.ebay.com"

df = pd.read_csv('productNames_export.csv')
df.columns = ["Product Name", "Amazon Price", "Product URL"]

#obtain length of columns of dataframe
dataFrameHeight = df.shape[0]


singleProductColumns = ["Listing Title", "eBay Item URL", "Price Sold For", "Shipping Price", "Date Sold"]
aggColumns = ["Product Name", "Amount Sold", "Amount Not Sold", "Percentage Sold"]
productDataColumnNames = ["Product Name", "Amazon Price", "eBay Average", "Percentage Sold", "Total Amount of Listings", "Date Sold"]


productDataFrame = pd.DataFrame(columns = productDataColumnNames)
masterProductFrame = pd.DataFrame(columns = singleProductColumns)
dataAggFrame = pd.DataFrame(columns = aggColumns)
masterDataAggFrame = pd.DataFrame(columns = aggColumns)
item_prices = []

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driverWait = WebDriverWait(driver, 5)
count = 1

driver.get(ebayHomeURL)

try:
    driverWait.until(EC.presence_of_element_located((By.ID, "gh-ac")))
except:
    driver.quit()


driver.find_element(By.ID, "gh-ac").send_keys(df.iloc[count][0], Keys.ENTER)

#time.sleep(2)

"""
clicks completed listing, only needs to be activated once at the beginning then ebay doesn't switch you out of that setting
"""

try:
    driverWait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="x-refine__group__8"]/ul/li[4]/div/a/div/span')))
except:
    driver.quit()


driver.find_element(By.XPATH, '//*[@id="x-refine__group__8"]/ul/li[4]/div/a/div/span').click()


while count < dataFrameHeight:
    time.sleep(0.5)
    totalAmount = 0 #Only past 60 items, add feature to select 240 feature
    percentageSold = 0.0
    amountNotSold = 0
    amountSold = 0
    productTitle = ""
    priceSold = 0.0
    
    """
    This bit of code finds the searchbar and enters in the name of item from pandas.csv export
    """
    productName = df.iloc[count][0]

    searchBarElement = driver.find_element(By.XPATH, '//*[@id="gh-ac"]')
    searchBarElement.clear()

    #time.sleep(0.1)
    driverWait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="gh-ac"]')))
    driverWait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="gh-ac"]')))
    searchBarElement.send_keys(productName)

    #time.sleep(0.2)
    driverWait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="gh-btn"]')))
    driverWait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="gh-btn"]')))
    driver.find_element(By.XPATH, '//*[@id="gh-btn"]').click()
    time.sleep(1)
    driverWait.until(EC.url_changes)
    
    """
    parses down to the results list
    
        NEED TO DO
        have "No more results" check done somewhere around here and calculate length possibly
    """
    soup_level1 = BeautifulSoup(driver.page_source, 'html.parser')

    middleSection = soup_level1.find(id ='srp-river-results')

    #itemList = middleSection.find_all("li", class_ = "s-item s-item__pl-on-bottom")
    itemListUL = middleSection.find("ul", class_ = "srp-results srp-list clearfix")
    itemList = itemListUL.find_all("li")
    print(itemList)
    #singleProductFrame = 
    for eachItem in itemList:

        dateSold = eachItem.find("span", class_='POSITIVE')
        price = eachItem.find("span", class_ = 's-item__price')
        shippingPrice = eachItem.find("span", class_ = 's-item__shipping s-item__logisticsCost')
        shippingPrice = shippingPrice.text

        try:
            dateList = str((dateSold.text)).split()
            del(dateList[0])
            dateList = " ".join(dateList)
            amountSold += 1
            dateSold = dateList
            
        except:
            dateSold = "False"
            amountNotSold += 1
            #print("%i NOT sold" %(amountNotSold))
            #print(dateSold)

        pricingSoup = BeautifulSoup(str(eachItem.contents), 'html.parser')
        listingTitle = eachItem.find("h3", class_ = "s-item__title s-item__title--has-tags")
        titleURL = eachItem.find("a", class_ = "s-item__link")
        titleURL = titleURL['href']

        totalAmount += 1
        if dateSold == "False":
            price = "Not Sold"

        listingTitle = listingTitle.text

        """
        All single product data frames are being added to the master product data frame, only master product data frame gets exported
        """
        singleProductDataFrame = pd.DataFrame({"Date Sold": [dateSold], "Listing Title": [listingTitle],
                                            "Price Sold For" : [price], "eBay Item URL": [titleURL], "Shipping Price": shippingPrice}, columns = singleProductColumns)
        #print(singleProductDataFrame)
        masterProductFrame = pd.merge(singleProductDataFrame, masterProductFrame, how = 'outer')
        #print(masterProductFrame)
        percentageSold = amountSold / totalAmount
        dataAggFrame = pd.DataFrame({"Product Name": [productName], "Amount Sold": [amountSold], "Amount Not Sold": [amountNotSold], "Percentage Sold": [percentageSold]}, columns = aggColumns)
    #END OF WHILE LOOP
    
    """
    masterProductFrame holds the data of each completed ebay item, and writes to a file with the name of the search term(item)
    """
    masterProductFrame.to_csv("%s.csv" %(df.iloc[count][0]))
    print('NEW ITEM STARTING')
    count += 1

