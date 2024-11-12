import tkinter as tk

class pause:
    def __init__(self, window):
        self.__pause_window = tk.Toplevel(window)
        self.__pause_window.grab_set()
        self.__pause_window.title("paused")