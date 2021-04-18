import requests
import json
import yaml
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="tester",
  password="test@123",
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

mycursor.execute("((select distinct brawlhalla_id_one from players_2v2) union (select distinct brawlhalla_id_two from players_2v2))")
data=mycursor.fetchall()

#run player1v1 stats collection first, then palyer2v2

if checkTableExists(mydb,"stats") == True:
  pass
else:
  mycursor.execute("create table stats (brawlhalla_id int primary key,name varchar(100), xp int,level int, xp_percentage decimal(14,13), games int, wins int, damagebomb varchar(20), damagemine varchar(20), damagespikeball varchar(20), damagesidekick varchar(20), hitsnowball int, kobomb int, komine int, kospikeball int, kosidekick int, kosnowball int, clan_id int, pesonal_xp int)")  

if checkTableExists(mydb,"stats_legends") == True:
  pass
else:
  mycursor.execute("create table stats_legends (brawlhalla_id int, legend_id int, damagedealt varchar(20), damagetaken varchar(20), kos int, falls int, suicides int, teamkos int, matchtime int, games int, wins int, xp int, level int, xp_percentage decimal(14,13), primary key(brawlhalla_id, legend_id))")  

api_key="4S1L2NNFYUEZ6V3RUE4W"

sql = "insert into stats (brawlhalla_id,name, xp, level, xp_percentage, games,wins,damagebomb,damagemine,damagespikeball,damagesidekick,hitsnowball,kobomb,komine,kospikeball,kosidekick,kosnowball)  values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" 
#sql = "insert into stats values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" 
sql1 = "insert into stats_legends values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" 

for d in data:
  s1="select brawlhalla_id from stats where brawlhalla_id = "+ str(d[0])
  mycursor.execute(s1)
  v = mycursor.fetchall()
  #print("brawlhalla id= "+ str(d[0]))
  if len(v) > 0:
    #print("cont")
    continue;

  s= "https://api.brawlhalla.com/player/"+str(d[0])+"/stats?api_key="+api_key
  print(s)
  res1v1=requests.get(s)
  i=json.loads(res1v1.text)
  #print(i['clan'])

  temp=(i['brawlhalla_id'],i['name'],i['xp'],i['level'],i['xp_percentage'],i['games'],i['wins'],i['damagebomb'],i['damagemine'],i['damagespikeball'],i['damagesidekick'],i['hitsnowball'],i['kobomb'],i['komine'],i['kospikeball'],i['kosidekick'],i['kosnowball'])
  #temp=(i['brawlhalla_id'],i['name'],i['xp'],i['level'],i['xp_percentage'],i['games'],i['wins'],i['damagebomb'],i['damagemine'],i['damagespikeball'],i['damagesidekick'],i['hitsnowball'],i['kobomb'],i['komine'],i['kospikeball'],i['kosidekick'],i['kosnowball'],i['clan']['clan_id'],i['clan']['personal_xp'])
  
  mycursor.execute(sql, temp)
  for j in i['legends']:
    temp1 = (i['brawlhalla_id'],j['legend_id'],j['damagedealt'], j['damagetaken'], j['kos'], j['falls'], j['suicides'], j['teamkos'], j['matchtime'], j['games'], j['wins'], j['xp'], j['level'], j['xp_percentage'])
    mycursor.execute(sql1, temp1)

  #print(i)
  #print(i['clan'])
  
mydb.commit()
#mycursor.close()
#mydb.close()
