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
import time
from lxml import etree

#driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()))

#column_names = ["Product Name", "Amazon Price"]
ebayHomeURL = "https://www.ebay.com/"

df = pd.read_csv('name_and_price.txt')
df.columns = ["Product Name", "Amazon Price"]
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
    dom = etree.HTML(str(soup))
    #product_list = driver.find_elements(By.XPATH, "//*[@id='srp-river-results']/ul/li")
    listCount = 1
    
    while listCount < 55:
        
            #product_list = soup.find_all(By.XPATH, "//*[@id='srp-river-results']/ul/li[%s]" %(listCount))
            #item_price = driver.find_element(By.XPATH, '/html/body/div[5]/div[4]/div[2]/div[1]/div[2]/ul/li[3]/div/div[2]/div[3]/div[1]/span/span')
            
            print(listCount)
            #print(product_list)
            listCount += 1
            #time.sleep(2)
            #print(element)
    #time.sleep(3)
    
    count += 1