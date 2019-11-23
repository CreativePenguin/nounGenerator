# nounGenerator -- Derek Leung, Winston Peng, and Ahmed Sultan
# SoftDev1 pd 9
# P01 --
# 2019-11-14

from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from flask import flash
from flask import session
from os import urandom
import urllib
import json
import sqlite3

app = Flask(__name__)
app.secret_key = urandom(32)

# -----------------------------------------------------------------
# DATABASE SETUP
DB_FILE = "info.db"
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

@app.route("/", methods=['GET', 'POST'])
def root():
    if 'user' in session:
        return redirect("/home")
    return redirect("/login")

@app.route("/login")
def login():
    # if user is already logged in, redirect back to discover
    if 'user' in session:
        return redirect(url_for('root'))
    
    # checking to see if something was input
    if (request.args):
        if (bool(request.args["username"]) and bool(request.args["password"])):
            iUser = request.args["username"]
            iPass = request.args["password"]

            with sqlite3.connect(DB_FILE) as connection:
                cur = connection.cursor()
                qry = 'SELECT username, password FROM userdata;'
                foo = cur.execute(qry)
                userList = foo.fetchall()
                for row in userList:
                    if iUser == row[0]:
                        if iPass == row[1]:
                            session['user'] = iUser
                            return redirect(url_for("root"))
                        else:
                            flash('Wrong password. Please try again.')
                    else:
                        flash('Unrecognized username. Please try again.')
    
    return render_template("login.html")


@app.route("/home")
def home():
    return "Hello!"

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/registerHelp")
def registerHelp():
    return None

@app.route("/leaderboards")
def leaderboards():
    return None

if __name__ == "__main__":
    app.debug = True
    app.run()
