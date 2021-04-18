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
if checkTableExists(mydb,"brawlhallaID") == True:
  mycursor.execute("drop table brawlhallaID")

mycursor.execute("create table brawlhallaID as ((select distinct brawlhalla_id from players_1v1) union (select distinct brawlhalla_id_one as brawlhalla_id from players_2v2) union (select distinct brawlhalla_id_two as brawlhalla_id from players_2v2))")

mydb.commit()
mycursor.close()
mydb.close()
