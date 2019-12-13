import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="class7"
)

#creating an instance of 'cursor' class which is used to execute the 'SQL' statements in 'Python'
mycursor = mydb.cursor()

def database():
    print("Connecting to database")
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="class7",
        database = "CSGOResults"
        )
    mycursor = mydb.cursor()
    user = input("Do the tables already exist?(y/n)")
    if user == "y":
        mycursor.execute("DROP TABLE PlayerMap")
        print(mycursor)
        mycursor.execute("DROP TABLE TeamMap")
        print(mycursor)
        mycursor.execute("DROP TABLE Player")
        print(mycursor)
        mycursor.execute("DROP TABLE Team")
        print(mycursor)
        mycursor.execute("DROP TABLE Map")
        print(mycursor)
        mycursor.execute("DROP TABLE Game")
        print(mycursor)
        mycursor.execute("DROP TABLE Event")
        print(mycursor)
    mycursor.execute("CREATE TABLE Team (TeamID SMALLINT AUTO_INCREMENT NOT NULL PRIMARY KEY, TeamName TINYTEXT NOT NULL)")
    print(mycursor)
    mycursor.execute("CREATE TABLE Player (PlayerID SMALLINT AUTO_INCREMENT NOT NULL PRIMARY KEY, Nickname TINYTEXT NOT NULL, FirstName TINYTEXT NOT NULL, LastName TINYTEXT NOT NULL, TeamID SMALLINT, FOREIGN KEY (TeamID) REFERENCES Team (TeamID))")
    print(mycursor)
    mycursor.execute("CREATE TABLE Event (EventID SMALLINT AUTO_INCREMENT NOT NULL PRIMARY KEY, EventName TINYTEXT NOT NULL)")
    print(mycursor)
    mycursor.execute("CREATE TABLE Game (GameID SMALLINT AUTO_INCREMENT NOT NULL PRIMARY KEY, Format TINYTEXT NOT NULL, NumberOfMaps TINYINT NOT NULL, Date DATE NOT NULL, EventID SMALLINT, FOREIGN KEY (EventID) REFERENCES Event(EventID))")
    print(mycursor)
    mycursor.execute("CREATE TABLE Map (MapID SMALLINT AUTO_INCREMENT NOT NULL PRIMARY KEY, RoundsPlayed TINYINT NOT NULL, Map TINYTEXT NOT NULL, GameID SMALLINT, FOREIGN KEY(GameID) REFERENCES Game(GameID))")
    print(mycursor)
    mycursor.execute("CREATE TABLE PlayerMap (MapID SMALLINT, PlayerID SMALLINT, Kills SMALLINT NOT NULL, Deaths SMALLINT NOT NULL, adr FLOAT NOT NULL, kast FLOAT NOT NULL, Rating FLOAT NOT NULL, FOREIGN KEY(MapID) REFERENCES Map(MapID), FOREIGN KEY (PlayerID) REFERENCES Player(PlayerID), PRIMARY KEY (MapID, PlayerID))")
    print(mycursor)
    mycursor.execute("CREATE TABLE TeamMap (MapID SMALLINT NOT NULL, TeamID SMALLINT NOT NULL, Won TINYINT NOT NULL, RoundsWon TINYINT NOT NULL, RoundsLost TINYINT NOT NULL, FOREIGN KEY(MapID) REFERENCES Map(MapID), FOREIGN KEY (TeamID) REFERENCES Team(TeamID), PRIMARY KEY (MapID, TeamID))")
    print(mycursor)
    print("done")


user = input("This constructs the database, Does the database already exist?(y/n)")
if user == "n":
    mycursor.execute("CREATE DATABASE CSGOResults")
    print(mycursor)
    database()
else:
    database()
