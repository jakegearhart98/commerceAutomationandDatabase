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

#driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()))

#column_names = ["Product Name", "Amazon Price"]
ebayHomeURL = "https://www.ebay.com/"

df = pd.read_csv('name_and_price.txt')
df.columns = ["Product Name", "Amazon Price"]
productDataColumnNames = ["Product Name", "Amazon Price", "eBay Average", "Percentage Sold", "Total Amount of Listings"]
productDataFrame = pd.DataFrame(columns = productDataColumnNames)
print(productDataFrame)
item_prices = []
#print(df.iloc[0][0])

driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()))


 #obtain ebay home page

#time.sleep(1)
count = 0
driver.get(ebayHomeURL)

while count < 14:
    print("Value of count %i" %count)
    if count == 0:
        #search item into search bar and press enter
        element = driver.find_element(By.ID, "gh-ac").send_keys(df.iloc[count][0], Keys.ENTER)
    if count != 0:
        driver.find_element(By.XPATH, '//*[@id="gh-ac"]').clear()
        element = driver.find_element(By.XPATH, '//*[@id="gh-ac"]').send_keys(df.iloc[count][0], Keys.ENTER)
    time.sleep(2)

    if count == 0:
        #clicks completed items
        driver.find_element(By.XPATH, '//*[@id="x-refine__group__8"]/ul/li[4]/div/a').click()

    time.sleep(1)

    pageSource = driver.page_source
    soup = BeautifulSoup(pageSource, features = 'lxml')

    #I got this bit from geeksforgeeks https://www.geeksforgeeks.org/how-to-use-xpath-with-beautifulsoup/
    #dom = etree.HTML(str(soup))
    #product_list = driver.find_elements(By.XPATH, "//*[@id='srp-river-results']/ul/li")
    listCount = 2
    
    while listCount < 70:
        #try:
            #product = driver.find_element(By.XPATH, '//*[@id="srp-river-results"]/ul/li[%s]' %(listCount))
            #itemSold = driver.find_element(By.XPATH, '//*[@id="srp-river-results"]/ul/li[%s]/div/div[2]/div[1]/div/span[l]' %(listCount))
            productSoup = BeautifulSoup(driver.find_element(By.XPATH, '//*[@id="srp-river-results"]/ul/li[%s]' %(listCount)), 'html.parser')
            
            print(productSoup)
            #print(itemSold)
            print(listCount)
            listCount += 1

        #except:
        #    listCount = 71
            pass

            
    #time.sleep(3)
    
    count += 1