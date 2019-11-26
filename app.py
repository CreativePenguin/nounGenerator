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
import random

app = Flask(__name__)
app.secret_key = urandom(32)

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

# ROOT ------------------------------
@app.route("/", methods=['GET', 'POST'])
def root():
    if 'user' in session:
        return redirect("/home")
    return redirect("/login")

# LOGIN ------------------------------
@app.route("/login")
def login():
    # if user is already logged in, redirect back to discover to be handled
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
                            flash('Wrong password! Please try again.')
                    else:
                        flash('Unrecognized username! Please try again.')
        else:
            flash('Not all fields filled! Please try again.')

    # rendering template
    return render_template("login.html")

# LOGOUT ------------------------------
@app.route("/logout")
def logout():
    if 'user' in session:
        session.pop("user")
        return redirect(url_for("login"))

    # redirecting to login if not logged in — logout does not have a page!
    return redirect(url_for("root"))

# REGISTER ------------------------------
@app.route("/register")
def register():
    # if user is already logged in, redirect back to root to be handled
    if 'user' in session:
        return redirect(url_for('root'))

    # checking to see if something was input
    if (request.args):
        # checking to see if all args present
        if (bool(request.args["username"]) and bool(request.args["password"]) and bool(request.args["confpassword"])):
            iUser = request.args["username"]
            iPass = request.args["password"]
            iConf = request.args["confpassword"]

            # confirming passwords match
            if (iPass == iConf):
                # next, checking to see if user in user list
                with sqlite3.connect(DB_FILE) as connection:
                    cur = connection.cursor()
                    qry = 'SELECT username, password FROM userdata;'
                    foo = cur.execute(qry)
                    userList = foo.fetchall()
                    for row in userList:
                        if (iUser == row[0]):
                            flash('Username already taken! Please try again.')
                            return redirect(url_for("register"))
                    qry = "INSERT INTO userdata VALUES('{}', '{}', 0, '');".format(iUser, iPass)
                    cur.execute(qry)
                    connection.commit()
                    flash('Successfully registered! Please log in.')
                    return redirect("/login")
            else:
                flash('Passwords do not match! Please try again.')
        else:
            flash('Not all fields filled! Please try again.')

    # rendering template
    return render_template("register.html")

# HOME ------------------------------
resultArray = []
@app.route("/home")
def home():
    global resultArray
    resultArray = []
    # checking to see if user is logged in
    if 'user' not in session:
        return redirect(url_for("root"))

    for i in range(5):
        u = urllib.request.urlopen("https://restcountries.eu/rest/v2")
        response = u.read()
        data = json.loads(response)

        # picking random country from API response
        rand_num = random.randint(0, 249)

        ctry_name = data[rand_num]['name']
        ctry_capital = data[rand_num]['capital']
        ctry_flag = data[rand_num]['flag']
        ctry_currency = data[rand_num]['currencies'][0]['name']
        ctry_population = data[rand_num]['population']
        ctry_languages = []
        for i in data[rand_num]['languages']:
            ctry_languages.append(i['name'])

        countryArray = [ctry_name, ctry_capital, ctry_flag, ctry_currency, ctry_population, ctry_languages]
        if countryArray not in resultArray:
            resultArray.append(countryArray)
        else:
            return redirect(url_for("home"))

    # rendering template
    return render_template("home.html",
        array=resultArray, username= session['user'])

@app.route("/country/<countryName>")
def country(countryName):
    index = -1
    for i in range(len(resultArray)):
        if(countryName == resultArray[i][0]):
            index = i
    return render_template("country.html",array=resultArray,index = index)


if __name__ == "__main__":
    app.debug = True
    app.run()
