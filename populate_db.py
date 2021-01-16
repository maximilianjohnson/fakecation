import pandas as pd
from fakecation import *


if __name__ == "__main__":

    df = pd.read_excel("fakecation/static/image_datasets/img_scraped_01162021100023.xls")

    with app.app_context():
        conn = get_db()

    c = conn.cursor()

    for index,row in df.iterrows():

        lat = row["LAT"]
        lon = row["LNG"]
        country = row["COUNTRY_ID"]
        number = 1
        gender = 1

        if type(row["URLS"]) == str:
            urls = row["URLS"].split('\n')

            for url in urls:
                insert_row(conn,lat,lon,country,number,gender,url)
