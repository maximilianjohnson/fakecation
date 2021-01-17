from fakecation import *
from flask import Flask, render_template, url_for, redirect, session
import pandas as pd
import numpy as np
from math import radians



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


def query_db_by_coords(conn,lat,lon,range):
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
    c = conn.cursor()

    imgs_df = pd.read_sql_query("SELECT * FROM images WHERE latitude BETWEEN ? and ? AND longitude BETWEEN ? and ?", conn, params=(lat-range, lat+range, lon-range,lon+range))
    #imgs_df = pd.read_sql_query("SELECT * from images",conn)
    df = add_distance_to_df(imgs_df,lat, lon)

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
    return df.to_json("data.json",'records')

@app.route("/")
def index():
    cur = get_db().cursor()
    return render_template("base.html")

if __name__ == "__main__":

    app.run()

    with app.app_context():
        conn = get_db()

    #create_table(conn)
    #insert_row(conn,100,125,20,2,"1,0","image123.jpg")

    #get_images(get_db(),100, 100

    img_df = query_db_by_coords(conn,50,20,20)
    print(img_df)
    print(calculate_distance(10,20,45,22))
    generate_json(img_df)
    with app.app_context():
        close_db()
