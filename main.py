from fakecation import app, get_db, close_db
from flask import Flask, render_template, url_for, redirect, session


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

def calculate_distances(lat, lon):
    return 1

@app.route("/")
def index():
    cur = get_db().cursor()
    return render_template("base.html")

if __name__ == "__main__":

    app.run(debug=True)
