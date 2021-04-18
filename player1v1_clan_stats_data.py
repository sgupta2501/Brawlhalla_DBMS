import requests
import json
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="tester2",
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

mycursor.execute("select distinct brawlhalla_id from players_1v1")
data=mycursor.fetchall()

#run player1v1 stats collection first, then palyer2v2, then this file

if checkTableExists(mydb,"stats") == True:
  mycursor.execute("alter table stats add column (clan_id int, personal_xp int)")
else:
  print("stats table does not exist")
  return

api_key="4S1L2NNFYUEZ6V3RUE4W"

sql = "insert into stats values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" 

for d in data:
  s= "https://api.brawlhalla.com/player/"+str(d[0])+"/stats?api_key="+api_key
  print(s)
  r = requests.get(s)
  res1v1=requests.get(s)
  i=json.loads(res1v1.text)
  temp=(i['brawlhalla_id'],i['name'],i['xp'],i['level'],i['xp_percentage'],i['games'],i['wins'],i['damagebomb'],i['damagemine'],i['damagespikeball'],i['damagesidekick'],i['hitsnowball'],i['kobomb'],i['komine'],i['kospikeball'],i['kosidekick'],i['kosnowball'])
  mycursor.execute(sql, temp)

  #print(i)
  #print(i['clan'])

mydb.commit()
#mycursor.close()
#mydb.close()
