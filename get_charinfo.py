from flask_mysqldb import MySQL
def get_charinfo(mysql,charName):
    cur = mysql.connection.cursor()
    cur.execute(f'SELECT * FROM devttg.war_characters WHERE characterName LIKE "{charName}%";')
    charinfo = cur.fetchall()
    return charinfo