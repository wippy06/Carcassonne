import tkinter as tk

class selectGame:
    def __init__(self, frame, playerFunc):
        self.__frame = frame
        self.__playerFunc = playerFunc

        tk.Label(self.__frame,text ="Choose save slot").pack()
        tk.Button(self.__frame, text = "Slot 1", command = lambda: self.__slotChoice(1)).pack()
        tk.Button(self.__frame, text = "Slot 2", command = lambda: self.__slotChoice(2)).pack()
        tk.Button(self.__frame, text = "Slot 2", command = lambda: self.__slotChoice(3)).pack()

    def __slotChoice(self, slot):
        print(slot)
        for widget in self.__frame.winfo_children():
            widget.destroy()
        self.__playerFunc(slot)