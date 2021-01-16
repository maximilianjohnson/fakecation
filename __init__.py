from flask import flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
import os

app = Flask(__name__)

app.config["SECRET_KEY"] = "hackthenorth2021"

basedir = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATA_URI"] = "sqlite:///" + os.path.join(basedir,"image_db.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
