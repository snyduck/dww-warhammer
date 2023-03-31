import sqlalchemy as db
from sqlalchemy import text
import os
from dotenv import load_dotenv
load_dotenv('.env')


def increment_counter():
    engine = db.create_engine(
        f"mysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}:3306/{os.getenv('MYSQL_DB')}")
    connection = engine.connect()

    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT turnNumber FROM lunch WHERE isWeek = 'True'"))
        currentTurn = result.all()[0][0]
        print(f'Current turn is {currentTurn}')

    if currentTurn == 5:
        nextTurn = 1
    else:
        nextTurn = currentTurn + 1

    print(f'The next turn is {nextTurn}')

    with engine.connect() as conn:
        result = conn.execute(text(
            f"UPDATE `lunch` SET `isWeek` = 'False' WHERE (`turnNumber` = '{currentTurn}');"))
        conn.commit()
        result = conn.execute(text(
            f"UPDATE `lunch` SET `isWeek` = 'True' WHERE (`turnNumber` = '{nextTurn}');"))
        conn.commit()


def decrement_counter():
    engine = db.create_engine(
        f"mysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}:3306/{os.getenv('MYSQL_DB')}")
    connection = engine.connect()

    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT turnNumber FROM lunch WHERE isWeek = 'True'"))
        currentTurn = result.all()[0][0]
        print(f'Current turn is {currentTurn}')

    if currentTurn == 1:
        nextTurn = 5
    else:
        nextTurn = currentTurn - 1

    print(f'The next turn is {nextTurn}')

    with engine.connect() as conn:
        result = conn.execute(text(
            f"UPDATE `lunch` SET `isWeek` = 'False' WHERE (`turnNumber` = '{currentTurn}');"))
        conn.commit()
        result = conn.execute(text(
            f"UPDATE `lunch` SET `isWeek` = 'True' WHERE (`turnNumber` = '{nextTurn}');"))
        conn.commit()