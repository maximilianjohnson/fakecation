from flask import Flask, g
from flask_session import Session
import os
import sqlite3

app = Flask(__name__)

app.config["SECRET_KEY"] = "hackthenorth2021"

basedir = os.path.abspath(os.path.dirname(__file__))

dbpath = os.path.join(basedir,"image_db.sqlite")

def create_table(conn):

    table = """CREATE TABLE IF NOT EXISTS images (
                        id integer PRIMARY KEY,
                        latitude integer,
                        longitude integer,
                        country integer,
                        number integer,
                        gender text,
                        filepath text
                        );"""
    c = conn.cursor()
    c.execute(table)



def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(dbpath)
    return db

def close_db():
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def insert_row(conn,lat,lon,country,number,gender,fp):

    c = conn.cursor()
    c.execute("INSERT INTO images(latitude,longitude,country,number,gender,filepath) VALUES (?,?,?,?,?,?)",(lat,lon,country,number,gender,fp))
    conn.commit()
