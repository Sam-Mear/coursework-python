import sqlite3
mydb = sqlite3.connect("CSGO-Results.db")
cursor = mydb.cursor()
#cursor.execute("SELECT avg(Rating) FROM PlayerMap")
#print(cursor.fetchall())
#cursor.execute("UPDATE Game SET Date = REPLACE(Date,'-1st','-01');")
#cursor.execute("UPDATE Game SET Date = REPLACE(Date,'-2nd','-02');")
#cursor.execute("UPDATE Game SET Date = REPLACE(Date,'-3rd','-03');")
#cursor.execute("UPDATE Game SET Date = REPLACE(Date,'st','');")
#cursor.execute("UPDATE Game SET Date = REPLACE(Date,'nd','');")
#cursor.execute("UPDATE Game SET Date = REPLACE(Date,'rd','');")
#cursor.execute("COMMIT")
#cursor.execute("UPDATE Game SET Date = REPLACE(Date,'-4','-04')")
#cursor.execute("UPDATE Game SET Date = REPLACE(Date,'-5','-05')")
#cursor.execute("UPDATE Game SET Date = REPLACE(Date,'-6','-06')")
#cursor.execute("UPDATE Game SET Date = REPLACE(Date,'-7','-07')")
#cursor.execute("UPDATE Game SET Date = REPLACE(Date,'-8','-08')")
#cursor.execute("UPDATE Game SET Date = REPLACE(Date,'-9','-09')")
#cursor.execute("UPDATE Game SET Date = REPLACE(Date,'19-','2019-')")
#cursor.execute("UPDATE Game SET Date = REPLACE(Date,'20-','2020-')")
#cursor.execute("UPDATE Game SET Date = REPLACE(Date,'2-1-','20-01-')")
#cursor.execute("SELECT MapName,COUNT(*) FROM GameMap GROUP BY MapName")
#print(cursor.fetchall())
#cursor.execute("SELECT subqry.PlayerID, round(subqry.AVERAGERATING,2), subqry.MAPCOUNT FROM (SELECT PlayerID, avg(adr), avg(kast), avg(Rating) AVERAGERATING,COUNT(Rating) MAPCOUNT FROM PlayerMap GROUP BY PlayerID) AS subqry WHERE subqry.AVERAGERATING>1.3 AND subqry.MAPCOUNT > 4")
#print(cursor.fetchall())
#cursor.execute("SELECT Game.Date,PlayerMap.PlayerID FROM Game,GameMap,PlayerMap WHERE Date >'20-01-01'")
#print(cursor.fetchall())
#cursor.execute("COMMIT")

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())