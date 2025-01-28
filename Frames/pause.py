import tkinter as tk
from constants import PAUSE_SIZE

class pause:
    def __init__(self, window, isPlaying, saveFunc):
        self.__window = window
        self.__pauseWindow = tk.Toplevel(self.__window)
        self.__pauseWindow.grab_set()
        self.__pauseWindow.title("paused")

        self.__pauseWindow.geometry(PAUSE_SIZE)

        tk.Label(self.__pauseWindow,text ="Paused").pack()
        tk.Button(self.__pauseWindow, text="Resume", command = self.__pauseWindow.destroy).pack()

        if isPlaying:
            tk.Button(self.__pauseWindow, text="Save", command= saveFunc).pack()

        tk.Button(self.__pauseWindow, text = "Exit", command = self.__window.destroy).pack()