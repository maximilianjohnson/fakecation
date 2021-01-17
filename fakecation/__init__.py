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
    filepath = db.Column(db.String(128))

db.create_all()

def insertDB(lat, lng, c_id, c_name, city, n, g, path):
    new_entry = dbFormat(latitude = lat, longitude = lng, country_id = c_id,
    country_name=c_name, city_name = city, number=n, gender=g, filepath=path)
    db.session.add(new_entry)
    db.session.commit()
    db.session.close()

# app = Flask(__name__)
#
# app.config["SECRET_KEY"] = "hackthenorth2021"
#
# basedir = os.path.abspath(os.path.dirname(__file__))
#
# dbpath = os.path.join(basedir,"image_db.sqlite")
#
# def create_table(conn):
#     """ Creates a table in database with columns:
#         id | latitude | longitude | country_id | country_name | city_name | number | gender | filepath |
#     """
#     table = """CREATE TABLE IF NOT EXISTS images (
#                         id integer PRIMARY KEY,
#                         latitude integer,
#                         longitude integer,
#                         country_id integer,
#                         country_name text,
#                         city_name text,
#                         number integer,
#                         gender text,
#                         filepath text
#                         );"""
#     c = conn.cursor()
#     c.execute(table)
#
#
#
# def get_db():
#     """ Opens connection to database and returns database object
#     """
#     db = getattr(g, '_database', None)
#     if db is None:
#         db = g._database = sqlite3.connect(dbpath)
#     return db
#
# def close_db():
#     """ Closes database connection
#     """
#     db = getattr(g, '_database', None)
#     if db is not None:
#         db.close()
#
# def insert_row(conn,lat,lon,country_id,country_name,city_name,number,gender,fp):
#     """ Inserts row into database
#
#         Parameters:
#             conn: database object (connection assumed to be open)
#             lat: latitude
#             lon: longitude
#             country_id: unique two-character ID for each country
#             country_name: name of country
#             city_name: name of city
#             number: the number of people in the image (currently always 1)
#             gender: comma-separated string of integers:
#                         0 = male-presenting
#                         1 = female-presenting
#                     (not currently used)
#             fp: string containing link to url of image
#
#         Output: none
#     """
#     c = conn.cursor()
#     c.execute("INSERT INTO images(latitude,longitude,country_id,country_name,city_name,number,gender,filepath) VALUES (?,?,?,?,?,?,?,?)",(lat,lon,country_id,country_name,city_name,number,gender,fp))
#     conn.commit()
