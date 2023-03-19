import os
from flask_mysqldb import MySQL

def connect_ttg_db(app):
    try:
        app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
        app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
        app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
        app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
        mysql = MySQL(app)
        return mysql
    except:
        print("Failure")
