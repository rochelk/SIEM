import mysql.connector
from mysql.connector import errorcode
user = 'root'
password = 'P@ssw0rd'
host = '192.168.252.136'
database = 'SIEM'

def ConnectToDB():
    try:
        cnx = mysql.connector.connect(user=user, password=password,
                                      host=host, database=database)
        return cnx, cnx.cursor(buffered=True)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        return None

def selectDodgePorts():
    cnx, cursor = ConnectToDB()
    query = "SELECT * FROM fwlogsT WHERE PORT =445 OR PORT = 4445"
    cursor.execute(query)
    a = cursor.fetchall()
    for i in a:
        print(i)


def countAttemptPort():
    cnx, cursor = ConnectToDB()
    query = ("""SELECT SRCIP, COUNT(SRCIP) FROM( SELECT DISTINCT SRCIP, PORT FROM fwlogsT AS D) AS C GROUP BY SRCIP""")
    cursor.execute(query)
    a = cursor.fetchall()
    for i in a:
        if int(i[1]) > 10:
            print(i)

def moreThanTen():
    cnx, cursor = ConnectToDB()
    query = ("""SELECT SRCIP, COUNT(DSTIP) FROM( SELECT DISTINCT SRCIP, DSTIP FROM fwlogsT AS D) AS C GROUP BY DSTIP""")
    cursor.execute(query)
    a = cursor.fetchall()
    for i in a:
        print(i)
#selectDodgePorts()
#countAttemptPort()
moreThanTen()
