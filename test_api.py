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
if checkTableExists(mydb,"legends") == True:
	mycursor.execute("drop table legends")
mycursor.execute("create table legends (legend_id int primary key,legend_name_key varchar(40),bio_name varchar(40),bio_aka varchar(100),weapon_one varchar(20),weapon_two varchar(20), strength varchar(20), dexterity varchar(20), defense varchar(20), speed varchar(20))")

api_key="4S1L2NNFYUEZ6V3RUE4W"
res=requests.get("https://api.brawlhalla.com/legend/all/?api_key="+api_key)
y=json.loads(res.text)

sql = "insert into legends values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
val=[]

for i in y: 
	temp=(i['legend_id'],i['legend_name_key'],i['bio_name'],i['bio_aka'],i['weapon_one'],i['weapon_two'],i['strength'],i['dexterity'],i['defense'],i['speed'])
	val.append(temp)

	# mycursor.execute(sql,val)
	# mydb.commit()
mycursor.executemany(sql, val)
mydb.commit()
