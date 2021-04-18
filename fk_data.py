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

mycursor = mydb.cursor()

mycursor.execute("select distinct clan_id from clan_member")
fkVal=mycursor.fetchall()
mycursor.execute("select distinct clan_id from clans")
pkVal=mycursor.fetchall()
if (fkVal==pkVal):
  mycursor.execute("alter table clan_member add foreign key (clan_id) references clans(clan_id)")
else:
  print("1 clan_member fk clan_id not added")

mycursor.execute("select distinct clan_id from stats")
fkVal=mycursor.fetchall()
if (fkVal==pkVal):
  mycursor.execute("alter table stats add foreign key (clan_id) references clans(clan_id)")
else:
  print("2 stats fk clan_id not added")


mycursor.execute("select distinct brawlhalla_id from clan_member")
fkVal=mycursor.fetchall()
mycursor.execute("select distinct brawlhalla_id from stats")
pkVal=mycursor.fetchall()
if (fkVal==pkVal):
  mycursor.execute("alter table clan_member add foreign key (brawlhalla_id) references stats(brawlhalla_id)")
else:
  print("3 clan_member fk brawlhalla_id not added")

mycursor.execute("select distinct brawlhalla_id from stats_legends")
fkVal=mycursor.fetchall()
if (fkVal==pkVal):
  mycursor.execute("alter table stats_legends add foreign key (brawlhalla_id) references stats(brawlhalla_id)")
else:
  print("4 stats_legends fk brawlhalla_id not added")


mycursor.execute("select distinct brawlhalla_id from players_1v1")
fkVal=mycursor.fetchall()
if (fkVal==pkVal):
  mycursor.execute("alter table players_1v1 add foreign key (brawlhalla_id) references stats(brawlhalla_id)")
else:
  print("5 players_1v1 fk brawlhalla_id not added")


mycursor.execute("select distinct brawlhalla_id_one from players_2v2")
fkVal=mycursor.fetchall()
if (fkVal==pkVal):
  mycursor.execute("alter table players_2v2 add foreign key (brawlhalla_id_one) references stats(brawlhalla_id)")
else:
  print("6 players_2v2 fk brawlhalla_id_one not added")


mycursor.execute("select distinct brawlhalla_id_two from players_2v2")
fkVal=mycursor.fetchall()
if (fkVal==pkVal):
  mycursor.execute("alter table players_2v2 add foreign key (brawlhalla_id_two) references stats(brawlhalla_id)")
else:
  print("7 players_2v2 fk brawlhalla_id_two not added")


mycursor.execute("select distinct legend_id from stats_legends")
fkVal=mycursor.fetchall()
mycursor.execute("select distinct legend_id from legends")
pkVal=mycursor.fetchall()
if (fkVal==pkVal):
  mycursor.execute("alter table stats_legends add foreign key (legend_id) references legends(legend_id)")
else:
  print("8 stats_legends fk legend_id not added")


mycursor.execute("select distinct best_legend from players_1v1")
fkVal=mycursor.fetchall()
if (fkVal==pkVal):
  mycursor.execute("alter table players_1v1 add foreign key (best_legend) references legends(legend_id)")
else:
  print("9 players_1v1 fk legend_id not added")


#mydb.commit()
