from fakecation import *
from flask import Flask, render_template, url_for, redirect, session
import pandas as pd



def calculate_distance(lat1, lon1, lat2, lon2):
    r = 6373

    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula for calculating distance between two coordinates
    # accounting for the curvature of the earth
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c

def get_images(conn, lat, lon):

    c = conn.cursor()

    imgs_df = pd.read_sql_query("SELECT * FROM images WHERE latitude BETWEEN ? and ? AND longitude BETWEEN ? and ?", conn, params=(lat-10, lat+10, lon-10,lon+10))


@app.route("/")
def index():
    cur = get_db().cursor()
    return render_template("base.html")

if __name__ == "__main__":

    app.run()

    with app.app_context():
        conn = get_db()

    create_table(conn)
    insert_row(conn,100,125,20,2,"1,0","image123.jpg")

    #get_images(get_db(),100, 100)
    with app.app_context():
        close_db()
