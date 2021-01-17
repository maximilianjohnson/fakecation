import pandas as pd
from fakecation import *


if __name__ == "__main__":


    df = pd.read_excel("fakecation/static/image_datasets/image_dataset_final.xls")

    with app.app_context():
        conn = get_db()

    c = conn.cursor()

    create_table(conn)

    count = 0

    for index,row in df.iterrows():

        lat = row["LAT"]
        lon = row["LNG"]
        country_id = row["COUNTRY_ID"]
        country_name = row["COUNTRY_NAME"]
        city_name = row["CITY_NAME"]
        number = 1
        gender = 0

        if type(row["URLS"]) == str:
            urls = row["URLS"].split('\n')

            for url in urls:
                insert_row(conn,lat,lon,country_id,country_name,city_name,number,gender,url)
                print("Inserted row " + str(count) + " to the database.")
                count += 1

    with app.app_context():
        close_db()
