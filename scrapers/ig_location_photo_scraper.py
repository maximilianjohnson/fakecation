from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import urllib.request
import time
import json
import face_recognition
import cv2
import numpy as np
from xlwt import Workbook
from datetime import datetime
import csv

with open('loc_codes.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

print(len(data))
# Workbook is created
wb = Workbook()
now = datetime.now() # current date and time
date_time = now.strftime("%m%d%Y%H%M%S")
wb_name ='img_scraped_{0}.xls'.format(date_time)
# add_sheet is used to create sheet.
sheet1 = wb.add_sheet('URL SCRAPED')

sheet1.write(0, 1, 'LOC_NAME')
sheet1.write(0, 2, 'LAT')
sheet1.write(0, 3, 'LNG')
sheet1.write(0, 4, 'COUNTRY_NAME')
sheet1.write(0, 5, 'COUNTRY_ID')
sheet1.write(0, 6, 'CITY_NAME')
sheet1.write(0, 7, 'CITY_ID')
sheet1.write(0, 8, 'URLS')


driver = webdriver.Chrome(ChromeDriverManager().install())
count=0
for loc_string in data:
    location_code = loc_string[0]
    count+=1
    url = "https://www.instagram.com/explore/locations/{0}/?__a=1".format(location_code)
    time.sleep(2)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    text = soup.get_text()
    data = json.loads(text)

    try:
        lat = data["graphql"]["location"]["lat"]
        lng = data["graphql"]["location"]["lng"]
        name = data["graphql"]["location"]["name"]
        print("Checking " + name)
        country_id = data["graphql"]["location"]["directory"]["country"]["id"]
        country_name = data["graphql"]["location"]["directory"]["country"]["name"]
        city_id = data["graphql"]["location"]["directory"]["city"]["id"]
        city_name = country = data["graphql"]["location"]["directory"]["city"]["name"]
        urls = ""
        ecount = 0
        for i in data["graphql"]["location"]["edge_location_to_media"]["edges"]:
            ecount += 1
            img = (i['node']['display_url'])
            response = urllib.request.urlopen(img)
            image = face_recognition.load_image_file(response)
            faces = face_recognition.face_locations(image)
            if len(faces) > 0:
                urls = urls + img + "\n"
            if len(urls)>len(img)*3 or ecount > 9:
                break
        tcount = 0
        for i in data["graphql"]["location"]["edge_location_to_top_posts"]["edges"]:
            tcount += 1
            img = (i['node']['display_url'])
            response = urllib.request.urlopen(img)
            image = face_recognition.load_image_file(response)
            faces = face_recognition.face_locations(image)
            if len(faces) > 0:
                urls = urls + img + "\n"
            if len(urls)>len(img)*5 or tcount > 7:
                break
        sheet1.write(count, 1, name)
        sheet1.write(count, 2, lat)
        sheet1.write(count, 3, lng)
        sheet1.write(count, 4, country_name)
        sheet1.write(count, 5, country_id)
        sheet1.write(count, 6, city_name)
        sheet1.write(count, 7, city_id)
        sheet1.write(count, 8, urls)

    except:
        pass
    wb.save(wb_name)

driver.quit()
print("DONE")
