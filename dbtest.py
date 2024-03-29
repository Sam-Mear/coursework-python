import sqlite3

mydb = sqlite3.connect("CSGO-Results.db")
cursor = mydb.cursor()
print("All table names:")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())
print("table Team")
cursor.execute("PRAGMA table_info(Team)")
print(cursor.fetchall())
print("table Player")
cursor.execute("PRAGMA table_info(Player)")
print(cursor.fetchall())
print("table Event")
cursor.execute("PRAGMA table_info(Event)")
print(cursor.fetchall())
print("table Game")
cursor.execute("PRAGMA table_info(Game)")
print(cursor.fetchall())
print("table GameMap")
cursor.execute("PRAGMA table_info(GameMap)")
print(cursor.fetchall())
print("table PlayerMap")
cursor.execute("PRAGMA table_info(PlayerMap)")
print(cursor.fetchall())
print("table TeamMap")
cursor.execute("PRAGMA table_info(TeamMap)")
print(cursor.fetchall())
cursor.close()
mydb.close()