import pandas as pd
from fakecation import *
from flask import Flask, g
from flask_session import Session
import os
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, update, or_
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
db = SQLAlchemy()

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/fakecation'
app.config['SECRET_KEY'] = 'thisissecret'

db = SQLAlchemy(app)

class dbFormat(db.Model):
    __tablename__="images"
    id = db.Column(db.Integer, primary_key = True)
    latitude = db.Column(db.Integer)
    longitude  = db.Column(db.Integer)
    country_id = db.Column(db.String(64))
    country_name = db.Column(db.String(64))
    city_name = db.Column(db.String(64))
    number = db.Column(db.Integer)
    gender = db.Column(db.String(64))
    filepath = db.Column(db.String(512))

db.create_all()

def insertDB(lat, lng, c_id, c_name, city, n, g, path):
    new_entry = dbFormat(latitude = lat, longitude = lng, country_id = c_id,
    country_name=c_name, city_name = city, number=n, gender=g, filepath=path)
    db.session.add(new_entry)
    db.session.commit()
    db.session.close()

if __name__ == "__main__":


    df = pd.read_excel("fakecation/static/image_datasets/final_locations_for_db.xls")

    count = 0

    for index,row in df.iterrows():

        lat = row["LAT"]
        lon = row["LNG"]
        country_id = row["COUNTRY_ID"]
        country_name = row["COUNTRY_NAME"]
        city_name = row["CITY_NAME"]
        number = 1
        gender = 0

        if type(row["URLS"]) == str:
            urls = row["URLS"].split('\n')

            for url in urls:
                insertDB(lat,lon,country_id,country_name,city_name,number,gender,url)
                print("Inserted row " + str(count) + " to the database.")
                count += 1
