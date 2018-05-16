import mysql.connector
from mysql.connector import errorcode

user = 'root'
password = 'P@ssw0rd'
host = '192.168.252.136'
database = 'SIEM'

PORTS = {'21' : 'FTP', '22' : 'SSH', '23' : 'TELNET', '25' : 'SMTP' , '67' : 'DHCP' , '53'  : 'DNS' , '80' : 'HTTP', '445'
: 'SMB' ,'443' : 'HTTPS'}





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

def getOrderly(file):
    cnx, cursor = ConnectToDB()
    f = open(file, 'r')
    fileList=f.readlines()
    for i in fileList:
        dictionar = splitDataToDict(i)
        portI =int(dictionar['PORT'])
        query = ("INSERT INTO fwlogsT (DATE, SRCIP, DSTIP, PORT, PROTOCOL, ACTION) VALUES ('%s', '%s', '%s', %s, '%s', '%s')"%( dictionar['DATE'], dictionar['SRC_IP'], dictionar['DST_IP'], portI, dictionar['PROTOCOL'], dictionar['ACTION']))
        
        cursor.execute(query)
       
        
        cnx.commit()
        
    cnx.close()

def splitDataToDict(listItem):
        dictionar = dict()
        
        listp = listItem.split()
        
        srcP =listp[2]

        dictionar.update({'SRC_IP': srcP})
  
        action = listp[-1]
        dictionar.update({'ACTION': action})

        date = listp[0] + " " + listp[1]

        dictionar.update({'DATE': date})
        dstP = listp[3]
        dictionar.update({'DST_IP': dstP})
        port = listp[-2]
        dictionar.update({'PORT': port})
 
        protocol = getPortName(dictionar['PORT'])
        dictionar.update({'PROTOCOL': protocol})
        return dictionar
        

def getPortName(portNum):
    try:
        return PORTS[portNum]
    except:
        return 'unknown'

    
'''def addProtocol(list):
    print(list)
    for i in list:

        a = getPortName(i['PORT'])
        i.update({'PROTOCOL': a})
        print i
'''


print(getOrderly('C:\Python27\Port_Scan.txt'))
