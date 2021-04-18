import requests
import json
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="tester2",
  password="test@123",
  database="brawlhalla"
)

mycursor = mydb.cursor()
mycursor.execute("select * from legends")

data=cur.fetchall()
print(data)
