import tkinter as tk
import re
from constants import SIGN_IN_OUT_SIZE,FRAME_BG_DEFAULT_COLOUR,BUTTON_DEFAULT_COLOUR,TEXT_FONT
from .subwindowBase import subwindowBase

class signInOutWindow(subwindowBase):
    def __init__(self,window,currentLogin,loginFunc,dbHandler):
        self.__currentLogin = currentLogin
        self.__loginFunc = loginFunc
        self.__dbHander = dbHandler

        super().__init__(window,"Sign In")
        
    def _displayMainFrame(self):
        self._window.geometry(str(SIGN_IN_OUT_SIZE[0])+"x"+str(SIGN_IN_OUT_SIZE[1]))
        self.__displayInitFrame()

    def __displayInitFrame(self):
        self.__clearFrame()
        if self.__currentLogin == "":
            tk.Button(self._mainFrame,text = "Log In",bg=BUTTON_DEFAULT_COLOUR,font=(TEXT_FONT,13),command=self.__loadLoginFrame).place(relx=0.5,rely=0.33,anchor="center")
            tk.Button(self._mainFrame,text = "Sign Up",bg=BUTTON_DEFAULT_COLOUR,font=(TEXT_FONT,13),command=self.__loadSignUpFrame).place(relx=0.5,rely=0.66,anchor="center")
        else:
            currentUser = self.__dbHander.getUsername(self.__currentLogin)
            tk.Label(self._mainFrame,text="Logged in as: "+currentUser,bg=FRAME_BG_DEFAULT_COLOUR,font=(TEXT_FONT,13)).place(relx=0.5,rely=0.33,anchor="center")
            tk.Button(self._mainFrame,text = "Log Out",bg=BUTTON_DEFAULT_COLOUR,font=(TEXT_FONT,13),command=self.__logOut).place(relx=0.5,rely=0.66,anchor="center")

    def __loadLoginFrame(self):
        self.__clearFrame()

        tk.Label(self._mainFrame, text = "Username: ",font=(TEXT_FONT,13),bg=FRAME_BG_DEFAULT_COLOUR).pack()
        self.__usernameEntry = tk.Entry(self._mainFrame)
        self.__usernameEntry.pack()

        tk.Label(self._mainFrame, text = "Password: ",font=(TEXT_FONT,13),bg=FRAME_BG_DEFAULT_COLOUR).pack()
        self.__passwordEntry = tk.Entry(self._mainFrame)
        self.__passwordEntry.pack()

        tk.Button(self._mainFrame,text = "Return",font=(TEXT_FONT,13),command=self.__displayInitFrame).pack()
        tk.Button(self._mainFrame,text = "Confirm",font=(TEXT_FONT,13),command=self.__confirmSignIn).pack()
        
    def __loadSignUpFrame(self):
        self.__clearFrame()

        tk.Label(self._mainFrame, text = "Username: ",font=(TEXT_FONT,13),bg=FRAME_BG_DEFAULT_COLOUR).pack()
        self.__usernameEntry = tk.Entry(self._mainFrame)
        self.__usernameEntry.pack()

        tk.Label(self._mainFrame, text = "Password: ",font=(TEXT_FONT,13),bg=FRAME_BG_DEFAULT_COLOUR).pack()
        self.__passwordEntry = tk.Entry(self._mainFrame)
        self.__passwordEntry.pack()

        tk.Label(self._mainFrame, text = "Confirm password: ",font=(TEXT_FONT,13),bg=FRAME_BG_DEFAULT_COLOUR).pack()
        self.__confirmPasswordEntry = tk.Entry(self._mainFrame)
        self.__confirmPasswordEntry.pack()

        tk.Button(self._mainFrame,text = "Return",font=(TEXT_FONT,13),command=self.__displayInitFrame).pack()
        tk.Button(self._mainFrame,text = "Confirm",font=(TEXT_FONT,13),command=self.__confirmSignUp).pack()

    def __confirmSignIn(self):
        #takes username and password then looks up in database
        username = self.__usernameEntry.get()
        password = self.__passwordEntry.get()

        hashedPassword = self.__hashPassword(password)
        userID = self.__dbHander.getUserID(username)

        if userID and self.__dbHander.checkPassword(username,hashedPassword):
            self.__loginFunc(userID)
            self._window.destroy()

    def __confirmSignUp(self):
        username = self.__usernameEntry.get()
        password = self.__passwordEntry.get()
        confirmPassword = self.__confirmPasswordEntry.get()

        #username has to be alphanumeric with space and - as possible special characters
        #password has to be alphanumeric with ! % _ + - = < > ? $ & @ as possible special characters
        #password has to be longer than 8 chars
        if password == confirmPassword and re.search("^([a-z]|[A-Z]|[0-9])([a-z]|[A-Z]|[0-9]|( |-)([a-z]|[A-Z]|[0-9]))*$",username) and re.search("^([a-z]|[A-Z]|[0-9]|!|%|_|\+|-|=|<|>|\?|\$|&|@)+$",password) and len(password)>=8:
            hashedPassword = self.__hashPassword(password)

            if self.__dbHander.newUser(username,hashedPassword):
                userID = self.__dbHander.getUserID(username)
                self.__loginFunc(userID)
                self._window.destroy()                 

    def __hashPassword(self,password):
        #to do make hash function
        return password

    def __logOut(self):
        self.__clearFrame()
        self.__loginFunc("")
        self.__currentLogin = ""
        self.__displayInitFrame()

    def __clearFrame(self):
        #removes tk children
        for widget in self._mainFrame.winfo_children():
            widget.destroy()