import tkinter as tk

class start:
    def __init__(self, window, frame, start_func):
        self.__frame = frame
        self.__window = window
        self.__start_func = start_func

        tk.Label(self.__frame,text ="Carcassonne").pack()
        tk.Button(self.__frame, text = "Start", command = self.__start).pack()
        tk.Button(self.__frame, text="Exit", command = self.__window.destroy).pack()

    def __start(self):
        for widget in self.__frame.winfo_children():
            widget.destroy()
        self.__start_func()
        