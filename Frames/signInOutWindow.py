import tkinter as tk
import re
from constants import SIGN_IN_OUT_SIZE, FRAME_BG_DEFAULT_COLOUR,BUTTON_DEFAULT_COLOUR,TEXT_FONT,FRAME_TOP_BAR_COLOUR

class signInOutWindow:
    def __init__(self,window,currentLogin,loginFunc,dbHandler):
        #new tk window
        self.__signWindow = tk.Toplevel(window,bg=FRAME_BG_DEFAULT_COLOUR,highlightthickness=2)
        self.__signWindow.grab_set()
        self.__signWindow.focus_force()
        self.__signWindow.title("Sign In")
        self.__signWindow.geometry(str(SIGN_IN_OUT_SIZE[0])+"x"+str(SIGN_IN_OUT_SIZE[1]))
        self.__signWindow.wm_overrideredirect(True)

        self.__signWindowTopBar = tk.Frame(self.__signWindow,bg=FRAME_TOP_BAR_COLOUR)
        self.__signWindowMainFrame = tk.Frame(self.__signWindow,bg=FRAME_BG_DEFAULT_COLOUR)

        self.__signWindowTopBar.pack(fill="x",anchor="n")
        self.__signWindowMainFrame.pack(fill="both",expand=True,anchor="n")

        tk.Label(self.__signWindowTopBar,text ="Sign In",font=(TEXT_FONT,16),bg=FRAME_TOP_BAR_COLOUR).pack(side="left")

        pixel = tk.PhotoImage(width=1, height=1)
        button = tk.Button(self.__signWindowTopBar, text="Close",font=(TEXT_FONT,16), width=50,height=30,image=pixel, compound='c', command=self.__signWindow.destroy, bg = BUTTON_DEFAULT_COLOUR)
        button.image = pixel
        button.pack(side="right")

        self.__center_window(self.__signWindow)

        self.__currentLogin = currentLogin
        self.__loginFunc = loginFunc

        self.__dbHander = dbHandler

        self.__displayInitFrame()

    def __displayInitFrame(self):
        self.__clearFrame()
        if self.__currentLogin == "":
            tk.Button(self.__signWindowMainFrame,text = "Log In",bg=BUTTON_DEFAULT_COLOUR,font=(TEXT_FONT,13),command=self.__loadLoginFrame).pack()
            tk.Button(self.__signWindowMainFrame,text = "Sign Up",bg=BUTTON_DEFAULT_COLOUR,font=(TEXT_FONT,13),command=self.__loadSignUpFrame).pack()
        else:
            currentUser = self.__dbHander.getUsername(self.__currentLogin)
            tk.Label(self.__signWindowMainFrame,text="Logged in as: "+currentUser,bg=FRAME_BG_DEFAULT_COLOUR,font=(TEXT_FONT,13)).pack()
            tk.Button(self.__signWindowMainFrame,text = "Log Out",bg=BUTTON_DEFAULT_COLOUR,font=(TEXT_FONT,13),command=self.__logOut).pack()

    def __loadLoginFrame(self):
        self.__clearFrame()

        tk.Label(self.__signWindowMainFrame, text = "Username: ",font=(TEXT_FONT,13),bg=FRAME_BG_DEFAULT_COLOUR).pack()
        self.__usernameEntry = tk.Entry(self.__signWindowMainFrame)
        self.__usernameEntry.pack()

        tk.Label(self.__signWindowMainFrame, text = "Password: ",font=(TEXT_FONT,13),bg=FRAME_BG_DEFAULT_COLOUR).pack()
        self.__passwordEntry = tk.Entry(self.__signWindowMainFrame)
        self.__passwordEntry.pack()

        tk.Button(self.__signWindowMainFrame,text = "Return",font=(TEXT_FONT,13),command=self.__displayInitFrame).pack()
        tk.Button(self.__signWindowMainFrame,text = "Confirm",font=(TEXT_FONT,13),command=self.__confirmSignIn).pack()
        
    def __loadSignUpFrame(self):
        self.__clearFrame()

        tk.Label(self.__signWindowMainFrame, text = "Username: ",font=(TEXT_FONT,13),bg=FRAME_BG_DEFAULT_COLOUR).pack()
        self.__usernameEntry = tk.Entry(self.__signWindowMainFrame)
        self.__usernameEntry.pack()

        tk.Label(self.__signWindowMainFrame, text = "Password: ",font=(TEXT_FONT,13),bg=FRAME_BG_DEFAULT_COLOUR).pack()
        self.__passwordEntry = tk.Entry(self.__signWindowMainFrame)
        self.__passwordEntry.pack()

        tk.Label(self.__signWindowMainFrame, text = "Confirm password: ",font=(TEXT_FONT,13),bg=FRAME_BG_DEFAULT_COLOUR).pack()
        self.__confirmPasswordEntry = tk.Entry(self.__signWindowMainFrame)
        self.__confirmPasswordEntry.pack()

        tk.Button(self.__signWindowMainFrame,text = "Return",font=(TEXT_FONT,13),command=self.__displayInitFrame).pack()
        tk.Button(self.__signWindowMainFrame,text = "Confirm",font=(TEXT_FONT,13),command=self.__confirmSignUp).pack()

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
        for widget in self.__signWindowMainFrame.winfo_children():
            widget.destroy()

    def getSignWindow(self):
        #for game selection frame and achievement window to wait until this window has closed
        return self.__signWindow

    def __center_window(self, window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")