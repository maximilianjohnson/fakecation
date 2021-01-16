from flask import Flask, g
from flask_session import Session
import os
import sqlite3

app = Flask(__name__)

app.config["SECRET_KEY"] = "hackthenorth2021"

basedir = os.path.abspath(os.path.dirname(__file__))

dbpath = os.path.join(basedir,"image_db.sqlite")

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(dbpath)
    return db

@app.teardown_appcontext
def close_db(error):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
