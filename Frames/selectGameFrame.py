import tkinter as tk
import json
import random
from constants import BUTTON_DEFAULT_COLOUR,TEXT_FONT,FRAME_BG_DEFAULT_COLOUR

class selectGameFrame:
    def __init__(self, frame, playerFunc, loadGameFunc, getLoginIDFunc, dbHandler, signInOutFunc, signInOutButton):
        self.__frame = tk.Frame(frame,bg=FRAME_BG_DEFAULT_COLOUR)
        self.__frame.pack(side="top",expand=True,fill="both")
        self.__playerFunc = playerFunc
        self.__loadGameFunc = loadGameFunc
        self.__getLoginIDFunc = getLoginIDFunc
        self.__signInOutFunc = signInOutFunc
        self.__dbHandler = dbHandler
        signInOutButton.config(command = self.__openLoginWindow)

        self.__initateDisplayFrame()      

    def __initateDisplayFrame(self):
        #removes tk children
        for widget in self.__frame.winfo_children():
            widget.destroy()

        tk.Label(self.__frame,text ="Choose save slot",font=(TEXT_FONT,40),bg=FRAME_BG_DEFAULT_COLOUR).place(relx=0.5,rely=0.2,anchor="center")

        if self.__getLoginIDFunc() != "":
            #set tk frames for game slot options      
            self.__slot1Frame = tk.Frame(self.__frame,borderwidth=1,relief="solid")
            self.__slot1Frame.place(relx=0.25,rely=0.5,anchor="center",width=300,height=300)

            self.__slot2Frame = tk.Frame(self.__frame,borderwidth=1,relief="solid")
            self.__slot2Frame.place(relx=0.5,rely=0.5,anchor="center",width=300,height=300)

            self.__slot3Frame = tk.Frame(self.__frame,borderwidth=1,relief="solid")
            self.__slot3Frame.place(relx=0.75,rely=0.5,anchor="center",width=300,height=300)

            self.__gameIDs = self.__dbHandler.getPlayableGames(self.__getLoginIDFunc())

            while len(self.__gameIDs) != 3:
                self.__gameIDs.append("")

            #create button options for slots not done as for loop to specify tk frames
            self.__createSlotDisplay(self.__gameIDs[0], self.__slot1Frame)
            self.__createSlotDisplay(self.__gameIDs[1], self.__slot2Frame)
            self.__createSlotDisplay(self.__gameIDs[2], self.__slot3Frame)

        else:
            self.__loginButton = tk.Button(self.__frame,text = "Login", font = (TEXT_FONT,13), command= self.__openLoginWindow)
            self.__loginButton.place(relx=0.5,rely=0.5,anchor="center")

    def __openLoginWindow(self):
        self.__frame.winfo_toplevel().wait_window(self.__signInOutFunc().getSignWindow())
        self.__initateDisplayFrame()

    def __createSlotDisplay(self, gameID, frame):
        if gameID == "":
            tk.Button(frame, text = "New Game", command = lambda: self.__slotChoice(""), bg = BUTTON_DEFAULT_COLOUR,font=(TEXT_FONT,13)).place(relx=0.5,rely=0.5,anchor="center")
        else:
            #check if slot filled then display data associated to game slot
            gameInfo = self.__dbHandler.getGamePreviewInfo(gameID)

            centreFrame = tk.Frame(frame)
            centreFrame.place(relx=0.5,rely=0.5,anchor="center")

            tk.Label(frame,text="Game ID " + str(gameID),font=(TEXT_FONT,20)).pack()
            tk.Label(centreFrame,text="Players : " + str(gameInfo[1]),font=(TEXT_FONT,13)).pack()
            tk.Label(centreFrame,text="Turn : " + str(gameInfo[0]+1),font=(TEXT_FONT,13)).pack()
            tk.Label(centreFrame,text="Tiles Remaining : " + str(int(self.__maxTiles()-gameInfo[0])),font=(TEXT_FONT,13)).pack()
            tk.Button(centreFrame, text = "Continue Game", command = lambda: self.__slotChoice(gameID), bg = BUTTON_DEFAULT_COLOUR,font=(TEXT_FONT,13)).pack()
            tk.Button(centreFrame, text = "Delete Game", command = lambda: self.__clearSlot(gameID, frame), bg = BUTTON_DEFAULT_COLOUR,font=(TEXT_FONT,13)).pack()

    def __maxTiles(self):
        tileTypeCount = open("tiles/tileCount.json", "r")
        tileTypeCountDict = json.loads(tileTypeCount.read())
        tileTypeCount.close()

        count = 0
        for value in tileTypeCountDict.values():
            count += value

        return count

    def __clearSlot(self, gameID, frame):
        self.__dbHandler.disableGame(gameID)

        for widget in frame.winfo_children():
            widget.destroy()
        self.__createSlotDisplay("", frame)
        
    def __slotChoice(self, gameID):
        #removes frame for next frame
        self.__frame.destroy()

        #seed giving max of 100000 different games
        #seed used for loading game so tile order does not have to be stored 
        seed = random.randint(0,99999)
       
        if gameID == "":
            #new game
            gameID = self.__dbHandler.newGame(seed,self.__getLoginIDFunc())
            self.__playerFunc(gameID)
        else:
            #load game
            self.__loadGameFunc(gameID)