from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from characterInfo import *
load_dotenv('.env')
import logging

db = SQLAlchemy()
app = Flask(__name__)

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    

app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}:3306/{os.getenv('MYSQL_DB')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers


class players(db.Model):
    playerID = db.Column(db.Integer, primary_key=True)
    playerFirstName = db.Column(db.String, nullable=False)
    playerLastName = db.Column(db.String, nullable=False)


class lunch(db.Model):
    turnNumber = db.Column(db.Integer, primary_key=True)
    playerID = db.Column(db.Integer, db.ForeignKey('players.playerID'))
    isWeek = db.Column(db.String)
    lastWeek = db.Column(db.String)


class war(db.Model):
    charID = db.Column(db.Integer, primary_key=True)
    playerID = db.Column(db.Integer, db.ForeignKey('players.playerID'))
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


class war_journal_entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    entry = db.Column(db.String)
    date = db.Column(db.String)


class LunchEntry():
    def __init__(self, name, turn_number):
        self.name = name
        self.turn_number = turn_number


with app.app_context():
    db.create_all()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/story")
def story():
    entryResult = db.session.execute(db.select(war_journal_entry)).scalars()
    entries = entryResult.all()
    if len(entries) == 0:
        app.logger.info("No entries in journal table!")
        return render_template("comingsoon.html")
    else:
        return render_template("story.html", entries=entries)


@app.route("/character/<charname>")
def character(charname):
    app.logger.info(f"Retrieving DB entries for ${charname}")
    charDBInfo = db.session.execute(db.select(war).where(
        war.charName.like(f'{charname}%'))).scalar()
    try:
        charInfo = buildCharacter(charDBInfo)
        return render_template("character.html", characterObject=charInfo, charname=charname)
    except Exception as e:
        app.logger.error(f"The query didn't parse for: {charname}")
        app.logger.error(f"Error: {e}")
        return render_template("index.html")


@app.route("/graveyard/<charname>")
def graveyard(charname):
    charDBInfo = db.session.execute(db.select(war).where(
        war.charName.like(f'{charname}%'))).scalar()
    try:
        charInfo = buildCharacter(charDBInfo)
        return render_template("deadcharacter.html", characterObject=charInfo, charname=charname)
    except Exception as e:
        app.logger.error(f"The query didn't parse for: {charname}")
        app.logger.error(f"Error: {e}")
        return render_template("index.html")


@app.route("/lunchlist")
def lunchlist():
    try:
        buyerQuery = db.session.execute(
            db.text(
                'SELECT * FROM players INNER JOIN lunch ON lunch.playerID = players.playerID WHERE isWeek = "True"')
        )
        buyerInfo = buyerQuery.all()[0]

        allPlayerLunchInfo = buyerQuery = db.session.execute(
            db.text(
                'SELECT * FROM players INNER JOIN lunch ON lunch.playerID = players.playerID ORDER BY turnNumber')
        )
        allPlayerLunchInfo = buyerQuery.all()

        return render_template("lunchlist.html", buyingPlayer=buyerInfo, allPlayerLunchInfo=allPlayerLunchInfo)
    except Exception as e:
        app.logger.error(f"An issue occured fetching info for lunch:")
        app.logger.error(f"Error: {e}")
        return render_template("index.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
