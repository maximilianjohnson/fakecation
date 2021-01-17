from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import urllib.request
import time
import numpy as np
import pandas as pd
import csv
from datetime import datetime

driver = webdriver.Chrome(ChromeDriverManager().install())
url = "https://www.instagram.com/explore/locations/"
driver.get(url)
time.sleep(15)
driver.get(url)
soup = BeautifulSoup(driver.page_source, 'html.parser')
codes = list()
countries = set()
for i in soup.find_all('li',{'class':'kiTXG'}):
    link = i.find('a',href=True)
    if link is None:
        continue
    countries.add("https://www.instagram.com" + link['href'])
    if len(countries) >= 50:
        break
cities = set()

for country in countries:
    print(country)
    ccount = 0
    time.sleep(5)
    driver.get(country)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    for i in soup.find_all('li',{'class':'kiTXG'}):
        link = i.find('a',href=True)
        if link is None:
            continue
        cities.add("https://www.instagram.com" + link['href'])
        ccount +=1
        if ccount >= 8:
            break

for loc in cities:
    time.sleep(5)
    driver.get(loc)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    lcount = 0
    for i in soup.find_all('li',{'class':'kiTXG'}):
        link = i.find('a',href=True)
        if link is None:
            continue
        clink = link['href']
        clink = clink[1:-1]
        find = clink.split('/', 3)
        codes.append(find[2])
        lcount += 1
        if lcount >= 5:
            break

df = pd.DataFrame(codes)
df.to_csv('loc_codes.csv', index=False)
driver.quit()
print("DONE")
