import tkinter as tk
from constants import BUTTON_DEFAULT_COLOUR,TEXT_FONT

class startFrame:
    def __init__(self, window, frame, startFunc):
        #start window displays on program start up
        self.__frame = frame
        self.__window = window
        self.__startFunc = startFunc

        tk.Label(self.__frame,text ="Carcassonne",font=(TEXT_FONT, 70), borderwidth=3, relief="solid",padx=20,pady=20).place(relx=0.5,rely=0.25,anchor = "center")
        tk.Button(self.__frame, text = "Start", command = self.__start, bg = BUTTON_DEFAULT_COLOUR, bd=6,font=(TEXT_FONT, 30),width=15,height=2).place(relx=0.5,rely=0.5,anchor = "center")
        tk.Button(self.__frame, text="Exit", command = self.__window.destroy, bg = BUTTON_DEFAULT_COLOUR,bd=6,font=(TEXT_FONT, 30),width=15,height=2).place(relx=0.5,rely=0.7,anchor = "center")
    
    def __start(self):
        #removes tk children to prepare for next frame
        for widget in self.__frame.winfo_children():
            widget.destroy()
        self.__startFunc()
        