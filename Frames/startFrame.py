import tkinter as tk
from constants import BUTTON_DEFAULT_COLOUR

class startFrame:
    def __init__(self, window, frame, startFunc):
        #start window displays on program start up
        self.__frame = frame
        self.__window = window
        self.__startFunc = startFunc

        tk.Label(self.__frame,text ="Carcassonne").pack()
        tk.Button(self.__frame, text = "Start", command = self.__start, bg = BUTTON_DEFAULT_COLOUR).pack()
        tk.Button(self.__frame, text="Exit", command = self.__window.destroy, bg = BUTTON_DEFAULT_COLOUR).pack()

    def __start(self):
        #removes tk children to prepare for next window
        for widget in self.__frame.winfo_children():
            widget.destroy()
        self.__startFunc()
        