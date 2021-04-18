import mysql.connector

cnx = mysql.connector.connect(user='root', password='hello0hello',
                              host='127.0.0.1',
                              database='dbms2021')
mycursor = cnx.cursor()

mycursor.execute("SELECT * FROM employee")

myresult = mycursor.fetchall()

for x in myresult:
  print(x)

cnx.close()