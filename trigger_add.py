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
if checkTableExists(mydb, "player_log") == True:
  pass
else:
  mycursor.execute("create table player_log (brawlhalla_id int primary key)")

mycursor.execute("""CREATE TRIGGER fill_log after INSERT ON stats FOR EACH ROW BEGIN insert into player_log (brawlhalla_id) values (new.brawlhalla_id); end""") 

mydb.commit()
