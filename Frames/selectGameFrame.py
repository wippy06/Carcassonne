import tkinter as tk
import json
from constants import BUTTON_DEFAULT_COLOUR,TEXT_FONT,FRAME_BG_DEFAULT_COLOUR

class selectGameFrame:
    def __init__(self, frame, playerFunc, loadGameFunc):
        self.__mainFrame = frame
        self.__frame = tk.Frame(frame,bg=FRAME_BG_DEFAULT_COLOUR)
        self.__frame.pack(side="top",expand=True,fill="both")
        self.__playerFunc = playerFunc
        self.__loadGameFunc = loadGameFunc

        #set tk frames for game slot options
        tk.Label(self.__frame,text ="Choose save slot",font=(TEXT_FONT,40),bg=FRAME_BG_DEFAULT_COLOUR).place(relx=0.5,rely=0.2,anchor="center")

        self.__slot1Frame = tk.Frame(self.__frame,borderwidth=1,relief="solid")
        self.__slot1Frame.place(relx=0.25,rely=0.5,anchor="center",width=300,height=300)

        self.__slot2Frame = tk.Frame(self.__frame,borderwidth=1,relief="solid")
        self.__slot2Frame.place(relx=0.5,rely=0.5,anchor="center",width=300,height=300)

        self.__slot3Frame = tk.Frame(self.__frame,borderwidth=1,relief="solid")
        self.__slot3Frame.place(relx=0.75,rely=0.5,anchor="center",width=300,height=300)

        #create button options for slots not done as for loop to specify tk frames
        self.__createSlotDisplay(1, self.__slot1Frame)
        self.__createSlotDisplay(2, self.__slot2Frame)
        self.__createSlotDisplay(3, self.__slot3Frame)

    def __createSlotDisplay(self, slot, frame):
        #check if slot filled then display data associated to game slot
        slotFile = open("gameSlots/slot"+str(slot)+".json", "r")
        fileString = slotFile.read()

        tk.Label(frame,text="Save Slot " + str(slot),font=(TEXT_FONT,20)).pack()

        if fileString == "":
            tk.Button(frame, text = "New Game", command = lambda: self.__slotChoice(slot), bg = BUTTON_DEFAULT_COLOUR,font=(TEXT_FONT,13)).place(relx=0.5,rely=0.5,anchor="center")
        else:
            fileData = json.loads(fileString)
            centreFrame = tk.Frame(frame)
            centreFrame.place(relx=0.5,rely=0.5,anchor="center")
            tk.Label(centreFrame,text="Players : " + str(len(fileData["players"])),font=(TEXT_FONT,13)).pack()
            tk.Label(centreFrame,text="Turn : " + str(len(fileData["moves"])+1),font=(TEXT_FONT,13)).pack()
            tk.Label(centreFrame,text="Tiles Remaining : " + str(int(fileData["tileNum"]-len(fileData["moves"]))),font=(TEXT_FONT,13)).pack()
            tk.Button(centreFrame, text = "Continue Game", command = lambda: self.__slotChoice(slot), bg = BUTTON_DEFAULT_COLOUR,font=(TEXT_FONT,13)).pack()
            tk.Button(centreFrame, text = "Delete Game", command = lambda: self.__clearSlot(slotFile, slot, frame), bg = BUTTON_DEFAULT_COLOUR,font=(TEXT_FONT,13)).pack()

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