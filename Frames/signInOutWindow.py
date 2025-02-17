import tkinter as tk
import re
from constants import SIGN_IN_OUT_SIZE, FRAME_BG_DEFAULT_COLOUR,WINDOW_CENTER_OFFSET,BUTTON_DEFAULT_COLOUR,TEXT_FONT

class signInOutWindow:
    def __init__(self,window,currentLogin,loginFunc,dbHandler):
        #new tk window
        self.__signWindow = tk.Toplevel(window,bg=FRAME_BG_DEFAULT_COLOUR)
        self.__signWindow.grab_set()
        self.__signWindow.focus_force()
        self.__signWindow.title("Sign In/Out")
        self.__signWindow.geometry(str(SIGN_IN_OUT_SIZE[0])+"x"+str(SIGN_IN_OUT_SIZE[1]))

        self.__center_window(self.__signWindow)

        self.__currentLogin = currentLogin
        self.__loginFunc = loginFunc

        self.__dbHander = dbHandler

        self.__displayInitFrame()

    def __displayInitFrame(self):
        self.__clearFrame()
        if self.__currentLogin == "":
            tk.Button(self.__signWindow,text = "Log In",bg=BUTTON_DEFAULT_COLOUR,font=(TEXT_FONT,13),command=self.__loadLoginFrame).pack()
            tk.Button(self.__signWindow,text = "Sign Up",bg=BUTTON_DEFAULT_COLOUR,font=(TEXT_FONT,13),command=self.__loadSignUpFrame).pack()
        else:
            currentUser = self.__dbHander.getUsername(self.__currentLogin)
            tk.Label(self.__signWindow,text="Logged in as: "+currentUser,bg=FRAME_BG_DEFAULT_COLOUR,font=(TEXT_FONT,13)).pack()
            tk.Button(self.__signWindow,text = "Log Out",bg=BUTTON_DEFAULT_COLOUR,font=(TEXT_FONT,13),command=self.__logOut).pack()

    def __loadLoginFrame(self):
        self.__clearFrame()

        tk.Label(self.__signWindow, text = "Username: ",font=(TEXT_FONT,13),bg=FRAME_BG_DEFAULT_COLOUR).pack()
        self.__usernameEntry = tk.Entry(self.__signWindow)
        self.__usernameEntry.pack()

        tk.Label(self.__signWindow, text = "Password: ",font=(TEXT_FONT,13),bg=FRAME_BG_DEFAULT_COLOUR).pack()
        self.__passwordEntry = tk.Entry(self.__signWindow)
        self.__passwordEntry.pack()

        tk.Button(self.__signWindow,text = "Return",font=(TEXT_FONT,13),command=self.__displayInitFrame).pack()
        tk.Button(self.__signWindow,text = "Confirm",font=(TEXT_FONT,13),command=self.__confirmSignIn).pack()
        
    def __loadSignUpFrame(self):
        self.__clearFrame()

        tk.Label(self.__signWindow, text = "Username: ",font=(TEXT_FONT,13),bg=FRAME_BG_DEFAULT_COLOUR).pack()
        self.__usernameEntry = tk.Entry(self.__signWindow)
        self.__usernameEntry.pack()

        tk.Label(self.__signWindow, text = "Password: ",font=(TEXT_FONT,13),bg=FRAME_BG_DEFAULT_COLOUR).pack()
        self.__passwordEntry = tk.Entry(self.__signWindow)
        self.__passwordEntry.pack()

        tk.Label(self.__signWindow, text = "Confirm password: ",font=(TEXT_FONT,13),bg=FRAME_BG_DEFAULT_COLOUR).pack()
        self.__confirmPasswordEntry = tk.Entry(self.__signWindow)
        self.__confirmPasswordEntry.pack()

        tk.Button(self.__signWindow,text = "Return",font=(TEXT_FONT,13),command=self.__displayInitFrame).pack()
        tk.Button(self.__signWindow,text = "Confirm",font=(TEXT_FONT,13),command=self.__confirmSignUp).pack()

    def __confirmSignIn(self):
        #takes username and password then looks up in database
        username = self.__usernameEntry.get()
        password = self.__passwordEntry.get()

        hashedPassword = self.__hashPassword(password)
        userID = self.__dbHander.getUserID(username)

        if userID and self.__dbHander.checkPassword(username,hashedPassword):
            self.__loginFunc(userID)
            self.__signWindow.destroy()

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
                self.__signWindow.destroy()                 

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
        for widget in self.__signWindow.winfo_children():
            widget.destroy()

    def getSignWindow(self):
        #for game selection frame to wait until this window has closed
        return self.__signWindow

    def __center_window(self, window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2-WINDOW_CENTER_OFFSET
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")