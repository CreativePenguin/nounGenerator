# nounGenerator -- Derek Leung, Winston Peng, and Ahmed Sultan
# SoftDev1 pd 9
# P01 --
# 2019-11-14

from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
import urllib
import json

app = Flask(__name__)

#-----------------------------------------------------------------
#DATABASE SETUP
DB_FILE = "Info.db"
db = sqlite3.connect(DB_FILE)
c = db.cursor()
c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='userdata' ''')
if c.fetchone()[0] < 1:
    c.execute("CREATE TABLE userdata();")
c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='countrydata' ''')
if c.fetchone()[0] < 1:
    c.execute("CREATE TABLE countrydata();")
c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='scores' ''')
if c.fetchone()[0] < 1:
    c.execute("CREATE TABLE scores();")

#-----------------------------------------------------------------

@app.route("/")
def main():
    return render_template("base.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def reigster():
    return render_template("register.html")

if __name__ == "__main__":
    app.debug = True
    app.run()
