import tkinter as tk

class selectGame:
    def __init__(self, frame, playerFunc, loadGameFunc):
        self.__frame = frame
        self.__playerFunc = playerFunc
        self.__loadGameFunc = loadGameFunc

        #set tk vars
        tk.Label(self.__frame,text ="Choose save slot").pack()

        self.__slot1Frame = tk.Frame(self.__frame)
        self.__slot1Frame.pack(side="top")

        self.__slot2Frame = tk.Frame(self.__frame)
        self.__slot2Frame.pack(side="top")

        self.__slot3Frame = tk.Frame(self.__frame)
        self.__slot3Frame.pack(side="top")

        #create button options
        self.__createSlotDisplay(1, self.__slot1Frame)
        self.__createSlotDisplay(2, self.__slot2Frame)
        self.__createSlotDisplay(3, self.__slot3Frame)

    def __createSlotDisplay(self, slot, frame):
        #check if slot filled
        slotFile = open("gameSlots/slot"+str(slot)+".json", "r")

        if slotFile.read() == "":
            tk.Button(frame, text = "New Game"+ str(slot), command = lambda: self.__slotChoice(slot)).pack()
        else:
            tk.Button(frame, text = "Continue Game"+ str(slot), command = lambda: self.__slotChoice(slot)).pack()
            tk.Button(frame, text = "Delete Game"+ str(slot), command = lambda: self.__clearSlot(slotFile, slot, frame)).pack()

        slotFile.close()

    def __clearSlot(self, slotFile, slot, frame):
        slotFile.close()
        slotFile = open("gameSlots/slot"+str(slot)+".json", "w")
        slotFile.close()
        for widget in frame.winfo_children():
            widget.destroy()
        self.__createSlotDisplay(slot, frame)
        
    def __slotChoice(self, slot):
        for widget in self.__frame.winfo_children():
            widget.destroy()

        slotFile = open("gameSlots/slot"+str(slot)+".json", "r")
       
        if slotFile.read() == "":
            self.__playerFunc(slot)
        else:
            self.__loadGameFunc("gameSlots/slot"+str(slot)+".json")