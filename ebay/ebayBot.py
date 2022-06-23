from itertools import count
from lib2to3.pgen2 import driver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
from pandas import concat
from bs4 import BeautifulSoup
import time, os
from selenium.webdriver.chrome.options import Options

options = Options()
options.headless = True
#column_names = ["Product Name", "Amazon Price"]
ebayHomeURL = "https://www.ebay.com/"

df = pd.read_csv('productNames_export.csv')
df.columns = ["Product Name", "Amazon Price", "Product URL"]

#obtain length of columns of dataframe
dataFrameHeight = df.shape[0]

singleProductColumns = ["Listing Title", "eBay Item URL", "Price Sold For", "Shipping Price", "Date Sold"]

productDataColumnNames = ["Product Name", "Amazon Price", "eBay Average", "Percentage Sold", "Total Amount of Listings", "Date Sold"]
productDataFrame = pd.DataFrame(columns = productDataColumnNames)
masterProductFrame = pd.DataFrame(columns = singleProductColumns)
item_prices = []
#print(df.iloc[0][0])

#driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()))
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
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
    time.sleep(0.5)
    totalAmount = 0 #Only past 60 items, add feature to select 240 feature
    percentageSold = 0.0
    amountNotSold = 0
    amountSold = 0
    productTitle = ""
    priceSold = 0.0
    #this finds the search bar
    #driver.find_element(By.ID, 'gh-ac-box2').clear()
    time.sleep(0.5)
    driver.find_element(By.CSS_SELECTOR, "#gh-ac").clear()
    driver.find_element(By.CSS_SELECTOR, "#gh-ac").send_keys(df.iloc[count][0], Keys.ENTER)
    time.sleep(0.2)
    ###################
    #with open('file%s.txt' %(count), 'w') as writeFile:
    #    writeFile.write(driver.page_source)
    soup_level1 = BeautifulSoup(driver.page_source, 'html.parser')
    middleSection = soup_level1.find(id ='srp-river-results')
    itemList = middleSection.find_all("li", class_ = "s-item s-item__pl-on-bottom")
    
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
        #itemID = pricingSoup.find("span", class_ = 's-item__detail s-item__detail--secondary')
        
        #print(itemID)
        listingTitle = eachItem.find("h3", class_ = "s-item__title s-item__title--has-tags")
        titleURL = eachItem.find("a", class_ = "s-item__link")

        titleURL = titleURL['href']
        
        
        #print(listingTitle.text)
        #print(productTitle.text)
        totalAmount += 1
        if dateSold == "False":
            price = "Not Sold"

        listingTitle = listingTitle.text
        singleProductDataFrame = pd.DataFrame({"Date Sold": [dateSold], "Listing Title": [listingTitle],
                                            "Price Sold For" : [price], "eBay Item URL": [titleURL], "Shipping Price": shippingPrice}, columns = singleProductColumns)
        #print(singleProductDataFrame)
        masterProductFrame = pd.merge(singleProductDataFrame, masterProductFrame, how = 'outer')
        print(masterProductFrame)
        
    """
    print("%i items sold" %(amountSold))
    print("%i NOT sold" %(amountNotSold))
    percentageSold = amountSold / totalAmount
    print("Percentage of items sold %f" %(percentageSold))
    """


    #singleProductDataFrame = pd.DataFrame({"Date Sold": [dateSold]}, columns = productDataColumnNames)
    #print(productDataFrame)
    print('NEW ITEM STARTING')
    count += 1
