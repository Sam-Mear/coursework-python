import sqlite3

mydb = sqlite3.connect("CSGO-Results1.db")

#creating an instance of 'cursor' class which is used to execute the 'SQL' statements in 'Python'
cursor = mydb.cursor()

def database(db,cursor):
    print("Connecting to database")
    cursor = mydb.cursor()
    cursor.execute("CREATE TABLE Team (TeamID INTEGER PRIMARY KEY,TeamName TEXT NOT NULL)")
    print(cursor)
    cursor.execute("CREATE TABLE Player (PlayerID INTEGER PRIMARY KEY,Nickname TEXT NOT NULL,Nationality TEXT NOT NULL,TeamID INTEGER NOT NULL,FOREIGN KEY (TeamID) REFERENCES Team (TeamID))")
    print(cursor)
    cursor.execute("CREATE TABLE Event (EventID INTEGER PRIMARY KEY,EventName TEXT NOT NULL)")
    print(cursor)
    cursor.execute("CREATE TABLE Game (GameID INTEGER PRIMARY KEY,Format TEXT NOT NULL,NumberOfMaps INTEGER NOT NULL,Date TEXT NOT NULL,EventID INTEGER NOT NULL,FOREIGN KEY (EventID) REFERENCES Event(EventID))")
    print(cursor)
    cursor.execute("CREATE TABLE GameMap (GameMapID INTEGER PRIMARY KEY,RoundsPlayed INTEGER NOT NULL,MapName TEXT NOT NULL,GameID INTEGER NOT NULL,FOREIGN KEY(GameID) REFERENCES Game(GameID))")
    print(cursor)
    cursor.execute("CREATE TABLE PlayerMap (GameMapID INTEGER NOT NULL,PlayerID INTEGER NOT NULL,Kills INTEGER NOT NULL,Deaths INTEGER NOT NULL,adr REAL NOT NULL,kast REAL NOT NULL,Rating REAL NOT NULL,FOREIGN KEY(GameMapID) REFERENCES GameMap(GameMapID),FOREIGN KEY (PlayerID) REFERENCES Player(PlayerID),PRIMARY KEY (GameMapID, PlayerID))")
    print(cursor)
    cursor.execute("CREATE TABLE TeamMap (GameMapID INTEGER NOT NULL,TeamID INTEGER NOT NULL,Won INTEGER NOT NULL,RoundsWon INTEGER NOT NULL,RoundsLost INTEGER NOT NULL,FOREIGN KEY(GameMapID) REFERENCES GameMap(GameMapID),FOREIGN KEY (TeamID) REFERENCES Team(TeamID),PRIMARY KEY (GameMapID, TeamID))")
    print(cursor)
    print("Created tables.... Onto basic data entry....")
    cursor.execute("INSERT INTO Team VALUES(0,'No Team')")
    print(cursor)
    print("Checking tbl Team..")
    cursor.execute("COMMIT")
    cursor.execute("SELECT * FROM Team")
    print(cursor.fetchall())
    cursor.execute("INSERT INTO Team (TeamName) VALUES('Test Team')")
    cursor.execute("COMMIT")
    cursor.execute("SELECT * FROM Team")
    print(cursor.fetchall())
    cursor.execute("DELETE FROM Team WHERE TeamID = 1")
    cursor.execute("COMMIT")
    cursor.execute("SELECT * FROM Team")
    print(cursor.fetchall())
    cursor.close()
    db.close()


database(mydb,cursor)