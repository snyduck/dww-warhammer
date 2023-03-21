from flask_mysqldb import MySQL
def get_charlist(mysql):
    charlist = []
    cur = mysql.connection.cursor()
    cur.execute('SELECT characterName FROM devttg.war;')
    rv = cur.fetchall()
    for i in rv:
        charlist.append(i[0])
    cur.close()
    return charlist