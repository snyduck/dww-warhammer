from flask import Flask, render_template
import os
from sqlalchemy import create_engine, text, select
from sqlalchemy.orm import Session
from flask import Flask, render_template
from dotenv import load_dotenv
from connect_ttg_db import *
from characterInfo import *
load_dotenv('.env')
app = Flask(__name__)

engine = create_engine(
    f"mysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}:3306/{os.getenv('MYSQL_DB')}", echo=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/character/<charname>")
def character(charname):
    stmt = text(f"SELECT * FROM war WHERE charname LIKE '{charname}%'")
    with Session(engine) as session:
        result = session.execute(stmt)
        for row in result:
            charDBInfoGrab = row
    try:
        dbInfo = charDBInfoGrab
        charInfo = buildCharacter(dbInfo)
        return render_template("character.html", characterObject=charInfo, charname=charname)
    except Exception as e:
        print(f"The query didn't parse for: {charname}")
        print(f"Error: {e}")
        return render_template("index.html")


@app.route("/lunchlist")
def lunchlist():
    return render_template("lunchlist.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# if __name__ == "__main__":
#     app.run()