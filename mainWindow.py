import tkinter as tk
from start import start
from pause import pause

class main_window:
    def __init__(self):
        self.__window = tk.Tk()
        self.__window.attributes("-fullscreen", True)

        self.__window.title("Carcassonne")

        self.__top_bar_frame = tk.Frame(self.__window)
        self.__top_bar_frame.pack(side="top", fill ="x")

        self.__top_bar_frame_l = tk.Frame(self.__top_bar_frame)
        self.__top_bar_frame_l.pack(side="left")

        self.__top_bar_frame_r = tk.Frame(self.__top_bar_frame)
        self.__top_bar_frame_r.pack(side="right")

        self.__bottom_frame = tk.Frame(self.__window)
        self.__bottom_frame.pack(side="top")

        tk.Label(self.__top_bar_frame_l,text ="Carcassonne").pack()
        tk.Button(self.__top_bar_frame_r, text = "Pause", command = self.__pause).pack()
        tk.Button(self.__top_bar_frame_r, text="Exit", command=self.__window.destroy).pack()

        self.__window.bind("<Escape>", self.__end_fullscreen)
        self.__window.bind("<F11>", self.__begin_fullscreen)

        self.__start_screen()

    def __pause(self):
        pause(self.__window)

    def __end_fullscreen(self, event):
        self.__window.attributes("-fullscreen", False)

    def __begin_fullscreen(self, event):
        self.__window.attributes("-fullscreen", True)

    def __start_screen(self):
        start(self.__window, self.__bottom_frame, self.__new_game)

    def __new_game(self):
        print("start")

    def run(self):
        self.__window.mainloop()