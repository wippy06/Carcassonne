import tkinter as tk
import json

class selectGame:
    def __init__(self, frame, playerFunc, loadGameFunc):
        self.__mainFrame = frame
        self.__frame = tk.Frame(frame)
        self.__frame.pack(side="top")
        self.__playerFunc = playerFunc
        self.__loadGameFunc = loadGameFunc

        #set tk frames for game slot options
        tk.Label(self.__frame,text ="Choose save slot").grid(column=1,row=0)

        self.__slot1Frame = tk.Frame(self.__frame)
        self.__slot1Frame.grid(column=0,row=1)

        self.__slot2Frame = tk.Frame(self.__frame)
        self.__slot2Frame.grid(column=1,row=1)

        self.__slot3Frame = tk.Frame(self.__frame)
        self.__slot3Frame.grid(column=2,row=1)

        #create button options for slots not done as for loop to specify tk frames
        self.__createSlotDisplay(1, self.__slot1Frame)
        self.__createSlotDisplay(2, self.__slot2Frame)
        self.__createSlotDisplay(3, self.__slot3Frame)

    def __createSlotDisplay(self, slot, frame):
        #check if slot filled then display data associated to game slot
        slotFile = open("gameSlots/slot"+str(slot)+".json", "r")
        fileString = slotFile.read()

        tk.Label(frame,text="Save Slot " + str(slot)).pack()

        if fileString == "":
            tk.Button(frame, text = "New Game"+ str(slot), command = lambda: self.__slotChoice(slot)).pack()
        else:
            fileData = json.loads(fileString)
            tk.Label(frame,text="Players : " + str(len(fileData["players"]))).pack()
            tk.Label(frame,text="Turn : " + str(len(fileData["moves"])+1)).pack()
            tk.Label(frame,text="Tiles Remaining : " + str(int(fileData["tileNum"]-len(fileData["moves"])))).pack()
            tk.Button(frame, text = "Continue Game"+ str(slot), command = lambda: self.__slotChoice(slot)).pack()
            tk.Button(frame, text = "Delete Game"+ str(slot), command = lambda: self.__clearSlot(slotFile, slot, frame)).pack()

        slotFile.close()

    def __clearSlot(self, slotFile, slot, frame):
        #delete data from game slots by accessing file
        slotFile.close()
        slotFile = open("gameSlots/slot"+str(slot)+".json", "w")
        slotFile.close()

        for widget in frame.winfo_children():
            widget.destroy()
        self.__createSlotDisplay(slot, frame)
        
    def __slotChoice(self, slot):
        #removes tk children to prepare for next window
        for widget in self.__mainFrame.winfo_children():
            widget.destroy()

        slotFile = open("gameSlots/slot"+str(slot)+".json", "r")
       
        if slotFile.read() == "":
            self.__playerFunc(slot)
        else:
            self.__loadGameFunc("gameSlots/slot"+str(slot)+".json")