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

def addFK(dbcon, fkTab, pkTab, fkattr, pkattr):
  mycursor = dbcon.cursor()
  
  fksql="select distinct "+fkattr+ " from "+ fkTab
  #print(fksql)
  mycursor.execute(fksql)
  fkVal=mycursor.fetchall()

  for d in fkVal:
    if d[0]==None:
      continue
    pksql="select "+pkattr+ " from "+ pkTab+ " where "+ pkattr + " = "+ str(d[0])
    #print(pksql)
    mycursor.execute(pksql)
    pkVal=mycursor.fetchall()
    if len(pkVal) == 0:
     fksql="delete from "+fkTab+ " where "+ fkattr+ " = "+ str(d[0])
     mycursor.execute(fksql)
  
  s= "alter table "+ fkTab + " add foreign key ("+fkattr+ ") references "+ pkTab+ "("+ pkattr+ ")"
  print(s)
  mycursor.execute(s)
  



addFK(mydb, "clan_member", "clans", "clan_id", "clan_id")
addFK(mydb, "clan_member", "stats", "brawlhalla_id", "brawlhalla_id")
addFK(mydb, "stats_legends", "stats", "brawlhalla_id", "brawlhalla_id")
addFK(mydb, "stats_legends", "stats", "brawlhalla_id", "brawlhalla_id")
addFK(mydb, "players_1v1", "stats", "brawlhalla_id", "brawlhalla_id")
addFK(mydb, "players_2v2", "stats", "brawlhalla_id_one", "brawlhalla_id")
addFK(mydb, "players_2v2", "stats", "brawlhalla_id_two", "brawlhalla_id")
addFK(mydb, "stats_legends", "legends", "legend_id", "legend_id")
addFK(mydb, "players_1v1", "legends", "best_legend", "legend_id")
addFK(mydb, "stats", "clans", "clan_id", "clan_id") 


mydb.commit()
