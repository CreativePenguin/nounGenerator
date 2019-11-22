# nounGenerator -- Derek Leung, Winston Peng, and Ahmed Sultan
# SoftDev1 pd 9
# P01 --
# 2019-11-14

from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
from os import urandom
import urllib
import json
import sqlite3

# -----------------------------------------------------------------
# DATABASE SETUP
DB_FILE = "Info.db"
db = sqlite3.connect(DB_FILE)
c = db.cursor()
c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='userdata' ''')
if c.fetchone()[0] < 1:
    c.execute("CREATE TABLE userdata(username TEXT, password TEXT);")
c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='countrydata' ''')
if c.fetchone()[0] < 1:
    c.execute("CREATE TABLE countrydata(countryname TEXT, population INTEGER, capital TEXT, demonym TEXT, flag_url BLOB, languages BLOB);")
c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='scores' ''')
if c.fetchone()[0] < 1:
    c.execute("CREATE TABLE scores(username TEXT, score1 INTEGER, score2 INTEGER, score3 INTEGER, score4 INTEGER, score5 INTEGER);")

# -----------------------------------------------------------------
# FLASK STUFF

app = Flask(__name__)
app.secret_key = urandom(32)

@app.route("/", methods=['GET', 'POST'])
def checkCreds():
    return redirect("/login")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def reigster():
    return render_template("register.html")

@app.route("/home")
def home():
    return None

@app.route("/leaderboards")
def leaderboards():
    return None

if __name__ == "__main__":
    app.debug = True
    app.run()
