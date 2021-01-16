from fakecation import app, db
from flask import Flask, render_template, url_for, redirect, session

@app.route("/")
def index():
    return render_template("base.html")

if __name__ == "__main__":
    app.run(debug=True)
