from fakecation import app, db
import os
import io
from flask import Flask, render_template, url_for, redirect, session, Response, request 
import PIL.Image as Image


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/results")
def results():
    return render_template("results.html")


@app.route('/api/', methods=["POST"])
def hello():
    data = request.get_data()
    try:
        path = './tmp/1'
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)

    image = Image.open(io.BytesIO(data))
    image.save('./tmp/1/my-file.png', "PNG")

    resp = Response("Foo bar baz")
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

if __name__ == "__main__":
    app.run(debug=True)
