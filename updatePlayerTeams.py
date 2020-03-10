import sqlite3
def update(date):
    mydb = sqlite3.connect("CSGO-Results.db")
    cursor = mydb.cursor()
    cursor.execute("SELECT PlayerID FROM Player")
    for each in cursor.fetchall():
        playerID = each[0]
        cursor.execute("SELECT TeamID,MAX(CountedTeam) FROM (SELECT TeamMap.TeamID TeamID,count(TeamMap.TeamID) CountedTeam FROM (SELECT PlayerMap.GameMapID PlayerMapGameID,PlayerID FROM PlayerMap,GameMap,Game WHERE PlayerID = ? AND PlayerMap.GameMapID = GameMap.GameMapID AND GameMap.GameID = Game.GameID AND Game.Date > ?),TeamMap WHERE TeamMap.GameMapID = PlayerMapGameID GROUP BY TeamMap.TeamID)",(playerID,date))
        teamID = cursor.fetchall()[0][0]
        if teamID == None:
            teamID=0
        cursor.execute("UPDATE Player SET TeamID = (?) WHERE PlayerID = (?)",(teamID,playerID))
    cursor.execute("COMMIT")