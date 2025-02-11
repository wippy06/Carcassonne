import tkinter as tk
from constants import PAUSE_SIZE, BUTTON_DEFAULT_COLOUR

class pauseWindow:
    def __init__(self, window, isPlaying, saveFunc):
        #opens new window and sets to root to prevent user from accessing main window

        self.__window = window
        self.__pauseWindow = tk.Toplevel(self.__window)
        self.__pauseWindow.grab_set()
        self.__pauseWindow.focus_force()
        self.__pauseWindow.title("paused")

        self.__pauseWindow.geometry(str(PAUSE_SIZE[0])+"x"+str(PAUSE_SIZE[1]))

        tk.Label(self.__pauseWindow,text ="Paused").pack()
        tk.Button(self.__pauseWindow, text="Resume", command = self.__pauseWindow.destroy, bg = BUTTON_DEFAULT_COLOUR).pack()

        if isPlaying:
            #displays if there is a current game being played
            tk.Button(self.__pauseWindow, text="Save", command= saveFunc).pack()

        tk.Button(self.__pauseWindow, text = "Exit", command = self.__window.destroy, bg = BUTTON_DEFAULT_COLOUR).pack()