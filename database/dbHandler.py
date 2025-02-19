import sqlite3, json

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

        #creates Achievement table
        self.__cur.execute("""
            CREATE TABLE IF NOT EXISTS Achievement(
            AchievementID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT UNIQUE NOT NULL,
            Description TEXT UNIQUE NOT NULL);
        """)

        #creates GameAchievement table, linking table for many to many relationship with game and achievement tables
        self.__cur.execute("""
            CREATE TABLE IF NOT EXISTS GameAchievement(
            GameID INTEGER NOT NULL,
            AchievementID INTEGER NOT NULL,
            PRIMARY KEY (GameID, AchievementID),        
            FOREIGN KEY (GameID) REFERENCES Game(GameID)
            FOREIGN KEY (AchievementID) REFERENCES Achievement(AchievementID));
        """)

        #inserting achievement data into database
        achievementData = open("jsonFiles/achievements.json", "r")
        achievementDataDict = json.loads(achievementData.read())
        achievementData.close()

        for i in achievementDataDict.keys():
            #try except in case achievement already in db
            try:
                self.__cur.execute("""
                    INSERT INTO Achievement (Name, Description)
                    VALUES (?,?);
                """, (achievementDataDict[i][0], achievementDataDict[i][1],))
                self.__db.commit()
            except:
                pass

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

        #returns ID of new game
        return self.__cur.lastrowid

    def disableGame(self,gameID):
        self.__cur.execute("""
            UPDATE Game
            SET Playable = 0
            WHERE GameID = ?;
        """, (gameID,))
        self.__db.commit()

    def deleteGame(self,gameID):
        self.__cur.execute("""
            DELETE FROM Game WHERE GameID = ?;
        """, (gameID,))
        self.__cur.execute("""
            DELETE FROM Player WHERE GameID = ?;
        """, (gameID,))
        self.__cur.execute("""
            DELETE FROM Move WHERE GameID = ?;
        """, (gameID,))
        self.__cur.execute("""
            DELETE FROM GameAchievement WHERE GameID = ?;
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

    def getGamePlayerInfo(self, gameID):
        self.__cur.execute("""
            SELECT Name, Type
            FROM Player
            WHERE gameID = ?
            ORDER BY PlayingOrder ASC;         
        """, (gameID,))

        return self.__cur.fetchall()
    
    def getGameSeed(self,gameID):
        self.__cur.execute("""
            SELECT Seed
            FROM Game
            WHERE GameID = ?
        """, (gameID,))

        return self.__cur.fetchone()[0]
    
    def getMoveList(self,gameID):
        self.__cur.execute("""
            SELECT Rotations, Meeple, XCoord, YCoord
            FROM Move
            WHERE GameID = ?
            ORDER BY PlayingOrder ASC;
        """, (gameID,))

        return self.__cur.fetchall()
    
    def newMove(self, order, rotations, meeple, xCoord, yCoord, gameID):
        self.__cur.execute("""
            INSERT INTO Move(PlayingOrder, Rotations, Meeple, XCoord, YCoord, GameID)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (order, rotations, meeple, xCoord, yCoord, gameID,))
        self.__db.commit()

    def newGameAchievement(self, gameID, achievementName):
        self.__cur.execute("""
            SELECT AchievementID
            FROM Achievement
            WHERE Name = ?;
        """, (achievementName,))

        achievementID = self.__cur.fetchone()[0]

        try:
            self.__cur.execute("""
                INSERT INTO GameAchievement(GameID, AchievementID)
                VALUES (?, ?);
            """, (gameID,achievementID))
            self.__db.commit()
        except:
            pass