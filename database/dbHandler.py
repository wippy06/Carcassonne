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

    def newUser(self,username,passwordHash):
        #try except in case user already in db
        try:
            self.__cur.execute("""
            INSERT INTO User (Username, PasswordHash) 
            VALUES (?, ?);
            """, (username, passwordHash))
            self.__db.commit()
            return True
        except:
            return False

    def checkPassword(self,username,passwordHash):
        self.__cur.execute("""
        SELECT PasswordHash FROM User WHERE Username = ?;
        """, (username,))
        passwordDBHash = self.__cur.fetchone()

        if passwordDBHash and passwordDBHash[0] == passwordHash:
            return True
        return False
    
    def getUserID(self,username):
        self.__cur.execute("""
        SELECT UserID FROM User WHERE Username = ?;
        """, (username,))
        userID = self.__cur.fetchone()

        if userID:
            return userID[0]
        return None
    
    def getUsername(self,userID):
        self.__cur.execute("""
        SELECT Username FROM User WHERE UserID = ?;
        """, (userID,))
        userID = self.__cur.fetchone()

        if userID:
            return userID[0]
        return None