from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from characterInfo import *
load_dotenv('.env')

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}:3306/{os.getenv('MYSQL_DB')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


class players(db.Model):
    playerID = db.Column(db.Integer, primary_key=True)
    playerFirstName = db.Column(db.String, nullable=False)
    playerLastName = db.Column(db.String, nullable=False)


class lunch(db.Model):
    turnNumber = db.Column(db.Integer, primary_key=True)
    playerID = db.Column(db.Integer)
    isWeek = db.Column(db.String)
    lastWeek = db.Column(db.String)


class war(db.Model):
    charID = db.Column(db.Integer, primary_key=True)
    playerID = db.Column(db.Integer)
    charName = db.Column(db.String)
    charBio = db.Column(db.String)
    charBlurb = db.Column(db.String)
    charEpitaph = db.Column(db.String)
    charImg = db.Column(db.String)
    charDead = db.Column(db.Integer)
    charClass = db.Column(db.String)
    charCareer = db.Column(db.String)
    charDistMark = db.Column(db.String)
    charStar = db.Column(db.String)
    charStatus = db.Column(db.String)
    charCareerGroup = db.Column(db.String)


with app.app_context():
    db.create_all()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/story")
def story():
    return render_template("story.html")


@app.route("/character/<charname>")
def character(charname):
    charDBInfo = db.session.execute(db.select(war).where(
        war.charName.like(f'{charname}%'))).scalar()
    try:
        charInfo = buildCharacter(charDBInfo)
        return render_template("character.html", characterObject=charInfo, charname=charname)
    except Exception as e:
        print(f"The query didn't parse for: {charname}")
        print(f"Error: {e}")
        return render_template("index.html")
    

@app.route("/graveyard/<charname>")
def graveyard(charname):
    charDBInfo = db.session.execute(db.select(war).where(
        war.charName.like(f'{charname}%'))).scalar()
    try:
        charInfo = buildCharacter(charDBInfo)
        return render_template("deadcharacter.html", characterObject=charInfo, charname=charname)
    except Exception as e:
        print(f"The query didn't parse for: {charname}")
        print(f"Error: {e}")
        return render_template("index.html")

@app.route("/lunchlist")
def lunchlist():
    try:
        buyerID = db.session.execute(
            db.select(lunch.playerID).where(lunch.isWeek == "True")).scalar()
        buyingPlayer = db.session.execute(db.select(players.playerFirstName).where(
            players.playerID == f"{buyerID}")).scalar()
        print(f"Getting playername: {buyingPlayer}")
        return render_template("lunchlist.html", buyingPlayer=buyingPlayer)
    except Exception as e:
        print(f"An issue occured fetching info for lunch:")
        print(f"Error: {e}")
        return render_template("index.html")
    
@app.route("/foo")
def foo():
    return "Foo and Bar!"


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
