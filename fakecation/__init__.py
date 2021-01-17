from flask import Flask, g
from flask_session import Session
import os
import sqlite3

app = Flask(__name__)

app.config["SECRET_KEY"] = "hackthenorth2021"

basedir = os.path.abspath(os.path.dirname(__file__))

dbpath = os.path.join(basedir,"image_db.sqlite")

def create_table(conn):
    """ Creates a table in database with columns:
        id | latitude | longitude | country_id | country_name | city_name | number | gender | filepath |
    """
    table = """CREATE TABLE IF NOT EXISTS images (
                        id integer PRIMARY KEY,
                        latitude integer,
                        longitude integer,
                        country_id integer,
                        country_name text,
                        city_name text,
                        number integer,
                        gender text,
                        filepath text
                        );"""
    c = conn.cursor()
    c.execute(table)



def get_db():
    """ Opens connection to database and returns database object
    """
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(dbpath)
    return db

def close_db():
    """ Closes database connection
    """
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def insert_row(conn,lat,lon,country_id,country_name,city_name,number,gender,fp):
    """ Inserts row into database

        Parameters:
            conn: database object (connection assumed to be open)
            lat: latitude
            lon: longitude
            country_id: unique two-character ID for each country
            country_name: name of country
            city_name: name of city
            number: the number of people in the image (currently always 1)
            gender: comma-separated string of integers:
                        0 = male-presenting
                        1 = female-presenting
                    (not currently used)
            fp: string containing link to url of image

        Output: none
    """
    c = conn.cursor()
    c.execute("INSERT INTO images(latitude,longitude,country_id,country_name,city_name,number,gender,filepath) VALUES (?,?,?,?,?,?,?,?)",(lat,lon,country_id,country_name,city_name,number,gender,fp))
    conn.commit()
