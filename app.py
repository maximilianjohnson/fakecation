from fakecation import *
from flask import Flask, render_template, url_for, redirect, session, Response, request
import pandas as pd
from pandas import DataFrame
import numpy as np
from math import radians
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker
import sys
import PIL.Image as Image
import io
import os
import shutil
from imgurpython import ImgurClient

sys.path.insert(0, "model/detect_face.py")

from model import detect_face

db = SQLAlchemy()

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://aaqbyjinuvxfdz:2f7e0c5ffb8b29b2e339a4b775730277ab29228630a4ad02f0d2303ce8b8167a@ec2-50-19-32-202.compute-1.amazonaws.com:5432/d1v6fidvqjq8nj'
app.config['SECRET_KEY'] = 'thisissecret'
engine = create_engine('postgres://aaqbyjinuvxfdz:2f7e0c5ffb8b29b2e339a4b775730277ab29228630a4ad02f0d2303ce8b8167a@ec2-50-19-32-202.compute-1.amazonaws.com:5432/d1v6fidvqjq8nj')
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

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculates distance between two geographic coordinates using the Haversine formula

     Parameters:
       lat1: float
            target latitude
       lon1: float
            target longitude
       lat2: float
            position latitude
       lon2: float
            position longitude

     Output: distance: the distance between two points in kilometers
     """
    r = 6373 # radius of the earth in km

    lat1 = np.radians(lat1)
    lon1 = np.radians(lon1)
    lat2 = np.radians(lat2)
    lon2 = np.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula for calculating distance between two coordinates
    # accounting for the curvature of the earth
    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arcsin(np.sqrt(a))

    distance = r * c

    return distance

def query_db_by_coords(lat,lon,range=5):
    """ Queries database for entries with latitudes and longitudes both within lat,lon +/- range
        Parameters:
            conn: database object (connection assumed to already be open)
            lat: float
                target latitude
            lon: float
                target longitude
            range: int
                the allowable deviation in latitude and longitude
        Output:
            df: pandas.DataFrame
                dataframe containing the results of query
    """
    query_string = 'select * from "images" WHERE latitude BETWEEN {0} and {1} AND longitude BETWEEN {2} and {3} AND length(filepath) > 0'.format(lat-range, lat+range, lon-range, lon+range)
    imgs_df = pd.read_sql_query(query_string, con=engine)
    df = add_distance_to_df(imgs_df,lat,lon)
    return df

def add_distance_to_df(df, lat, lon):
    """ Returns dataframe object containing queries of 10 images cloest to target
        location
     Parameters:
       df: pandas.DataFrame
            dataframe containing results from SQL query
       lat: float
            target latitude
       lon: float
            target longitude
     Output: dataframe containing 10 nearest images based on Haversine distance
     """

    df["distance"] = calculate_distance(lat,lon,df["latitude"],df["longitude"])

    return df.sort_values("distance").iloc[0:10, 0: ]

def generate_json(df):
    """ Produces JSON representation of dataframe
    Parameters:
        df: pandas.DataFrame
            dataframe to be converted
    Output:
        df_json: string
            string representation of df in JSON format
    """
    return df.to_json(orient='records')

def generate_url_list(df):
    """ Produces list of urls in df
    Parameters:
        df: pandas.DataFrame
            dataframe to be converted
    Output:
        urls: <list> String
            list of urls
    """
    df_list = df["filepath"].tolist()
    df_list = list(filter(None, df_list))
    return df_list

def upload_image(image):
    """Uploads an image file to Imgur"""
    client_id= "a99d1e81fecda64"
    client_secret= "f15cffffa9a4dae824c3044fbb79078582a5d928"
    client = ImgurClient(client_id, client_secret)

    response = client.upload_from_path(image)
    return response['link']

@app.route("/")
def index():
    #new_df = query_db_by_coords(39,-9,range=5)
    #json_db = generate_json(new_df)

    #detect_face.deep_fake("","")
    return render_template("index.html")

@app.route("/results")
def results():
    return render_template("results.html")

@app.route("/results/images", methods=["POST", "GET"])
def images():
    jsonresp = ""
    if session.get("jsonresp") != "" or not session.get("jsonresp") :
        jsonresp = session.get("jsonresp")

    print(jsonresp)
    return jsonresp

@app.route("/latlong", methods=["GET", "POST"])
def latlong() :
    #content=request.json
    jsonresp = ""
    if request.method == "POST":
        location = request.json
        print(location)
        lat = location["lat"]
        lon = location["lng"]
        img_df = query_db_by_coords(lat,lon)
        jsonresp = generate_json(img_df)

    session["jsonresp"] = jsonresp
    return jsonresp

@app.route('/api/', methods=["POST"])
def read_img():
    try:
        path = './tmp/1'
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)

    img = (request.files["filepond"])
    file_name = img.filename
    prefix = file_name.split(".")
    image = Image.open(img)
    img_path = path + "/test_img"
    image.save(img_path, prefix[1])
    resp = Response("1")
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/api/', methods=["DELETE"])
def delete_img():
    folder = './tmp/1'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    os.rmdir(folder)
    return Response()

@app.route('/deepfake', methods=["POST"])
def deep_fake():
    url = request.get_json()
    swap_url = ""
    try:
        path = detect_face.deep_fake(url, './tmp/1/test_img')
        swap_url = upload_image(path)
    except:
        pass
    print(swap_url)
    return Response(swap_url)


if __name__ == "__main__":
    app.run(debug=True)
