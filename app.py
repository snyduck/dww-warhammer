from flask import Flask, render_template, request
import os
from flask import Flask, render_template
from flask_mysqldb import MySQL
from dotenv import load_dotenv
from connect_ttg_db import *
from get_charinfo import get_charinfo
from characterInfo import *
load_dotenv('.env')
app = Flask(__name__)

db = connect_ttg_db(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/character/<charname>")
def character(charname):
    charDBInfoGrab = get_charinfo(db, charname)
    try:
        dbInfo = charDBInfoGrab[0]
        charInfo = buildCharacter(dbInfo)
        return render_template("character.html",characterObject=charInfo)
    except:
        print("Your shit didn't parse, dumbass")
        return render_template("index.html")



@app.route("/lunchlist")
def lunchlist():
    print("Yes")
    return render_template("lunchlist.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0')
