import sqlite3

class dbHandler:
    def __init__(self):
        with sqlite3.connect("database/database.db") as self.__db:
            self.__cur = self.__db.cursor()

        #creates User table
        self.__cur.execute("""       
            CREATE TABLE IF NOT EXISTS User(                    
            UserID INTEGER PRIMARY KEY AUTOINCREMENT,
            Username TEXT UNIQUE NOT NULL,
            PasswordHash TEXT UNIQUE NOT NULL);                                           
        """)

        #creates Game table
        self.__cur.execute("""       
            CREATE TABLE IF NOT EXISTS Game(                    
            GameID INTEGER PRIMARY KEY AUTOINCREMENT,
            Seed INTEGER NOT NULL,
            Playable BOOLEAN NOT NULL,
            UserID INTEGER NOT NULL,
            FOREIGN KEY (UserID) REFERENCES User(UserID));                                           
        """)

        #creates Player table
        self.__cur.execute("""       
            CREATE TABLE IF NOT EXISTS Player(                    
            PlayerID INTEGER PRIMARY KEY AUTOINCREMENT,
            PlayingOrder INTEGER NOT NULL,
            Name TEXT NOT NULL,
            Type TEXT NOT NULL,
            GameID INTEGER NOT NULL,
            FOREIGN KEY (GameID) REFERENCES Game(GameID));                                           
        """)

        #creates Move table
        self.__cur.execute("""       
            CREATE TABLE IF NOT EXISTS Move(                    
            MoveID INTEGER PRIMARY KEY AUTOINCREMENT,
            PlayingOrder INTEGER NOT NULL,
            Rotations INTEGER NOT NULL,
            Meeple TEXT NOT NULL,
            XCoord INTEGER NOT NULL,
            YCoord INTEGER NOT NULL,
            GameID INTEGER NOT NULL,
            FOREIGN KEY (GameID) REFERENCES Game(GameID));                                           
        """)

    def newUser(self,username,passwordHash):
        #try except in case user already in db
        try:
            self.__cur.execute("""
                INSERT INTO User (Username, PasswordHash) 
                VALUES (?, ?);
            """, (username, passwordHash,))
            self.__db.commit()
            return True
        except:
            return False

    def checkPassword(self,username,passwordHash):
        self.__cur.execute("""
            SELECT PasswordHash
            FROM User
            WHERE Username = ?;
        """, (username,))
        passwordDBHash = self.__cur.fetchone()

        if passwordDBHash and passwordDBHash[0] == passwordHash:
            return True
        return False
    
    def getUserID(self,username):
        self.__cur.execute("""
            SELECT UserID
            FROM User WHERE
            Username = ?;
        """, (username,))
        userID = self.__cur.fetchone()

        if userID:
            return userID[0]
        return None
    
    def getUsername(self,userID):
        self.__cur.execute("""
            SELECT Username
            FROM User
            WHERE UserID = ?;
        """, (userID,))
        userID = self.__cur.fetchone()

        if userID:
            return userID[0]
        return None
    
    def newGame(self,seed,userID):
        self.__cur.execute("""
            INSERT INTO Game (Seed, Playable, UserID) 
            VALUES (?, 1, ?);
        """, (seed, userID,))
        #not committed in case user exits program before selecting players

        #gets game id of just added game and returns it
        self.__cur.execute("""
            SELECT MAX(GameID)
            FROM Game;
        """)
        return self.__cur.fetchone()[0]

    def disableGame(self,gameID):
        self.__cur.execute("""
            UPDATE Game
            SET Playable = 0
            WHERE GameID = ?;
        """, (gameID,))
        self.__db.commit()

    def getPlayableGames(self,userID):
        self.__cur.execute("""
            SELECT GameID
            FROM Game
            WHERE UserID = ?
            AND Playable = 1;
        """, (userID,))
        GameIDs = self.__cur.fetchall()

        return [x[0] for x in GameIDs]
    
    def getGamePreviewInfo(self,gameID):
        self.__cur.execute("""
            SELECT COUNT(*)
            FROM Move
            WHERE GameID = ?;
        """, (gameID,))
        numMovesMade = self.__cur.fetchone()[0]

        self.__cur.execute("""
            SELECT COUNT(*)
            FROM Player
            WHERE GameID = ?;
        """, (gameID,))
        numPlayers = self.__cur.fetchone()[0]

        return [numMovesMade,numPlayers]
    
    def newPlayer(self,playingOrder, name, playerType, gameID):
        self.__cur.execute("""
            INSERT INTO Player(PlayingOrder, Name, Type, GameID)
            VALUES (?, ?, ?, ?);
        """, (playingOrder, name, playerType, gameID,))
        self.__db.commit()

    def getPlayerID(self, gameID):
        self.__cur.execute("""
            SELECT PlayerID
            FROM Player
            WHERE GameID = ?
            SORT BY PlayingOrder ASC;
        """, (gameID,))

        PlayerIDs = self.__cur.fetchall()

        return [x[0] for x in PlayerIDs]

    def getPlayerInfo(self, playerID):
        self.__cur.execute("""
            SELECT PlayingOrder, Name, Type
            FROM Player
            WHERE playerID = ?
        """, (playerID,))

        return self.__cur.fetchone()
    
    def getGameSeed(self,gameID):
        self.__cur.execute("""
            SELECT Seed
            FROM Game
            WHERE GameID = ?
        """, (gameID,))

        return self.__cur.fetchone()[0]