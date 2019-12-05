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
import utl.readapi as readapi

app = Flask(__name__)
app.secret_key = urandom(32)

DB_FILE = "Info.db"
db = sqlite3.connect(DB_FILE)
c = db.cursor()

# -----------------------------------------------------------------
# DATABASE SETUP
c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='userdata' ''')
if c.fetchone()[0] < 1:
    c.execute("CREATE TABLE userdata(username TEXT, password TEXT, countriesOwned INTEGER, countryList BLOB);")
c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='countrydata' ''')
if c.fetchone()[0] < 1:
    c.execute("CREATE TABLE countrydata(countryname TEXT, owner TEXT, hiScore INTEGER);")

# -----------------------------------------------------------------
# FLASK STUFF

# ROOT ------------------------------
@app.route("/", methods=['GET', 'POST'])
def root():
    if 'user' in session:
        return redirect("/home")
    return redirect("/login")

# LOGIN ------------------------------
@app.route("/login", methods=['GET', 'POST'])
def login():
    """Login page -- Redirects if user is logged in. Leads to home page & account creation"""
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
            flash('Please make sure you filled out all the fields with the correct information')

    # rendering template
    return render_template("login.html")

# LOGOUT ------------------------------
@app.route("/logout")
def logout():
    """Removes user session, and leads back to login page"""
    if 'user' in session:
        session.pop("user")
        return redirect(url_for("login"))

    # redirecting to login if not logged in — logout does not have a page!
    return redirect(url_for("root"))

# REGISTER ------------------------------
@app.route("/register")
def register():
    """Register page -- Create a new account. Leads into Login Page"""
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
                    cur.execute("INSERT INTO userdata VALUES (?, ?, ?, ?)",
                                (iUser, iPass, 0, ""))
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
    """Home Page -- Shows 5 random countries"""
    global resultArray
    resultArray = []
    # checking to see if user is logged in
    if 'user' not in session:
        return redirect(url_for("root"))

    u = urllib.request.urlopen("https://restcountries.eu/rest/v2")
    response = u.read()
    data = json.loads(response)

    # Chooses and displays 5 random countries
    count = 0
    while count < 5:
        # picking random country from API response
        rand_num = random.randint(0, 249)

        ctry_name = data[rand_num]['name']
        ctry_capital = data[rand_num]['capital']
        ctry_flag = data[rand_num]['flag']
        ctry_currency = data[rand_num]['currencies'][0]['name']
        ctry_currency_code = data[rand_num]['currencies'][0]['code']
        ctry_population = data[rand_num]['population']
        ctry_languages = []
        for i in data[rand_num]['languages']:
            ctry_languages.append(i['name'])

        countryArray = [ctry_name, ctry_capital, ctry_flag, ctry_currency, ctry_population, ctry_languages, ctry_currency_code]
        if countryArray not in resultArray and ctry_population > 50000000:
            count = count + 1
            resultArray.append(countryArray)
        else:
            count = count

    # rendering template
    return render_template("home.html",
        array=resultArray, username= session['user'])

# COUNTRY ------------------------------
@app.route("/country/<countryName>")
def country(countryName):
    """Each country has a different web page for a different quiz"""
    index = -1
    for i in range(len(resultArray)):
        if (countryName == resultArray[i][0]):
            index = i
            owner = None
            with sqlite3.connect(DB_FILE) as connection:
                cur = connection.cursor()
                foo = cur.execute("SELECT owner FROM countrydata WHERE countryname LIKE ? ;",(countryName,))
                hello = foo.fetchall()
                if(len(hello)>=1):
                    owner = hello[0][0]
            return render_template("country.html", selection=resultArray[index], owner=owner, username=session['user'])

    # if not currently available, return to root
    return redirect(url_for("root"))

@app.route("/profile/<username>")
def profile(username):
    user = ""
    with sqlite3.connect(DB_FILE) as connection:
        cur = connection.cursor()
        qry = 'SELECT username, password FROM userdata;'
        foo = cur.execute(qry)
        userList = foo.fetchall()
        for row in userList:
            if (username == row[0]):
                user = username
                break

    with sqlite3.connect(DB_FILE) as connection2:
        cur = connection2.cursor()
        qry = 'SELECT * FROM countrydata WHERE owner="{}";'.format(username)
        foo = cur.execute(qry)
        countryList = foo.fetchall()
        countriesOwnedArray = []
        for row in countryList:
            countriesOwnedArray.append(row)

    return render_template("profile.html", user=user, carray=countriesOwnedArray, lenArr=len(countriesOwnedArray))

questions = []
# CHALLENGE ------------------------------
@app.route("/challenge/<countryName>")
def challenge(countryName):
    """Challenge page where you wait when someone else is trying to log in"""
    index = -1
    for i in range(len(resultArray)):
        # print(resultArray[i][0])
        if (countryName == resultArray[i][0]):
            index = i
            #print("hello")
    #print(index)
    with sqlite3.connect(DB_FILE) as connection:
        doesntExist = True  # if it's in the country database [ONLY CLAIMED COUNTRIES ARE IN THE DATABASE]
        cur = connection.cursor()
        bruh = cur.execute('SELECT * FROM countrydata;')
        for i in bruh:
            if(i[0] == countryName):
                doesntExist = False
        if(doesntExist):
            print(resultArray)
            cur.execute("INSERT INTO countrydata VALUES(?, ?, ?);",(resultArray[index][0], session['user'],0)) #if the claimed country isn't there, auto claim it
        cur.execute('SELECT * FROM countrydata')
    global questions
    questions = readapi.trivia_questions()
    return render_template("challenge.html", selection=resultArray[index], doesntExist = doesntExist, questions = questions)
    #TODO
    #ASSUMING THAT QUESTIONS IS A LIST OF LISTS IN THE FORMAT [[question number,question,answer1,answer2,answer3,answer4,index of right answer],[other question + answers]]
    #example: [1,"what is 9+10?",1,2,3,19,5]

@app.route("/leaderboards")
def leaderboard():
    """Leaderboard page shows who owns what country and so on"""
    # stuff stores what goes into leaderboard
    stuff = []
    with sqlite3.connect(DB_FILE) as connection:
        cur = connection.cursor()
        cur.execute('SELECT username FROM userdata;')
        names = cur.fetchall()
    for i in names:  # loops through all registered usernames
        cur.execute("SELECT * FROM countrydata WHERE OWNER LIKE ? ;",(i[0],)) #cross references username with country owners
        count = len(cur.fetchall())
        stuff.append([i,count])
    sorted(stuff, key =lambda x: x[1], reverse =True)
    print(stuff)
    return render_template("leaderboard.html", stuff = stuff)

@app.route("/answers/<countryName>", methods=['GET', 'POST'])
def check(countryName):
    """Checks answers to see if they're right"""
    numCorrect = 0
    for i in questions:
        #print(request.form[str(i[0])])
        #print(i[6])
        try:
            if(int(request.form[str(i[0])]) == i[6]):
                numCorrect+=1
        except KeyError as e:
            numCorrect+=0
    with sqlite3.connect(DB_FILE) as connection:
        cur = connection.cursor()
        foo = cur.execute('SELECT hiScore FROM countrydata WHERE countryname = ?;',(countryName,))
        hello = foo.fetchall()
        print(hello)
        print(numCorrect)
        if(numCorrect>=hello[0][0]):
            cur.execute('DELETE FROM countrydata WHERE countryname = ?;',(countryName,))
            cur.execute("INSERT INTO countrydata VALUES(?, ?, ?);",(countryName, session['user'] ,numCorrect))
            flash('You got {} question(s) right! That\'s the high score! You now own this country!'.format(numCorrect))
            flash(readapi.get_wikipedia_img_api(countryName))
        else: flash('You didn\'t top the existing score, but you can try again!')
    return redirect("/country/{}".format(countryName))


if __name__ == "__main__":
    app.debug = True
    app.run()
