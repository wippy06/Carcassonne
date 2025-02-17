import sqlite3

with sqlite3.connect("testDatabase.db") as db:
            cur = db.cursor()

#creates User table
cur.execute("""       
CREATE TABLE IF NOT EXISTS User(                    
UserID INTEGER PRIMARY KEY AUTOINCREMENT,
Username TEXT UNIQUE NOT NULL,
PasswordHash TEXT UNIQUE NOT NULL);                                           
""")

#creates Game table
cur.execute("""       
CREATE TABLE IF NOT EXISTS Game(                    
GameID INTEGER PRIMARY KEY AUTOINCREMENT,
Seed INTEGER NOT NULL,
Playable BOOLEAN NOT NULL,
UserID INTEGER UNIQUE NOT NULL,
FOREIGN KEY (UserID) REFERENCES User(UserID));                                           
""")

#creates Player table
cur.execute("""       
CREATE TABLE IF NOT EXISTS Player(                    
PlayerID INTEGER PRIMARY KEY AUTOINCREMENT,
PlayerName TEXT NOT NULL,
Type TEXT NOT NULL,
GameID INTEGER UNIQUE NOT NULL,
FOREIGN KEY (GameID) REFERENCES Game(GameID));                                           
""")

#creates Move table
cur.execute("""       
CREATE TABLE IF NOT EXISTS Move(                    
MoveID INTEGER PRIMARY KEY AUTOINCREMENT,
Rotations INTEGER NOT NULL,
Meeple TEXT NOT NULL,
XCoord INTEGER NOT NULL,
YCoord INTEGER NOT NULL,
GameID INTEGER UNIQUE NOT NULL,
FOREIGN KEY (GameID) REFERENCES Game(GameID));                                           
""")

def newGame(seed,userID):
    #try except in case user already in db
    try:
        cur.execute("""
        INSERT INTO Game (Seed, Playable, UserID) 
        VALUES (?, 1, ?);
        """, (seed, userID))
        db.commit()
        return True
    except:
        return False
    
def getPlayableGames(userID):
    cur.execute("""
        SELECT GameID
        FROM Game
        WHERE UserID = ?
        AND Playable = 1;
    """, (userID))
    GameIDs = cur.fetchall()

    return GameIDs

print(getPlayableGames(str(0)))

