import requests
import json
import yaml
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="hello0hello",
  database="brawlhalla"
)

def checkTableExists(dbcon, tablename):
    dbcur = dbcon.cursor()
    dbcur.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = '{0}'
        """.format(tablename.replace('\'', '\'\'')))
    if dbcur.fetchone()[0] == 1:
        dbcur.close()
        return True

    dbcur.close()
    return False

mycursor = mydb.cursor()

mycursor.execute("select distinct clan_id from stats")
data=mycursor.fetchall()

if checkTableExists(mydb,"clans") == True:
  mycursor.execute("drop table clans")
mycursor.execute("create table clans (clan_id int primary key,clan_name varchar(100),clan_create_date varchar(20),clan_xp varchar(20))")  

api_key="4S1L2NNFYUEZ6V3RUE4W"

sql = "insert into clans values (%s,%s,%s,%s)" 
val=[] 

for d in data:
  s= "https://api.brawlhalla.com/clan/"+str(d[0])+"/?api_key="+api_key
  res1v1=requests.get(s)
  i=json.loads(res1v1.text)

  temp=(i['clan_id'],i['clan_name'],i['xp'],i['clan_create_date'],i['clan_xp'])
  val.append(temp)
 
mycursor.executemany(sql, val)
mydb.commit()
