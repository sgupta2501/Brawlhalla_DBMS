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
if checkTableExists(mydb,"players_1v1") == True:
	mycursor.execute("drop table players_1v1 ")
mycursor.execute("create table players_1v1 (rankp int primary key,name varchar(100),brawlhalla_id int,region varchar(20),best_legend int,best_legend_games int,best_legend_wins int,rating int, tier varchar(20), games int, wins int,peak_rating int)")

if checkTableExists(mydb,"players_2v2") == True:
	mycursor.execute("drop table players_2v2 ")
mycursor.execute("create table players_2v2 (rankp int primary key,teamname varchar(100),brawlhalla_id_one int,brawlhalla_id_two int,region varchar(20), rating int, peak_rating int, tier varchar(20), wins int, games int)")

api_key="4S1L2NNFYUEZ6V3RUE4W"
res1v1=requests.get("https://api.brawlhalla.com/rankings/1v1/all/1?api_key="+api_key)
res2v2=requests.get("https://api.brawlhalla.com/rankings/2v2/all/1?api_key="+api_key)

y1=json.loads(res1v1.text)
y2=json.loads(res2v2.text)

sql = "insert into players_1v1  values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
val=[]
for i in y1: 
	temp=(i['rank'] ,i['name'],i['brawlhalla_id'],i['region'],i['best_legend'],i['best_legend_games'] ,i['best_legend_wins'],i['rating'],i['tier'],i['games'],i['wins'],i['peak_rating'])
	#print(temp)
	val.append(temp)

	# mycursor.execute(sql,val)
	# mydb.commit()
mycursor.executemany(sql, val)
mydb.commit()

sql = "insert into players_2v2  values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
val=[]
for i in y2: 
	temp=(i['rank'],i['teamname'],i['brawlhalla_id_one'],i['brawlhalla_id_two'],i['region'], i['rating'], i['peak_rating'], i['tier'], i['wins'], i['games'])
	# print(temp)  
	val.append(temp)

	# mycursor.execute(sql,val)
	# mydb.commit()
mycursor.executemany(sql, val)
mydb.commit()