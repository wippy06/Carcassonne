import tkinter as tk
from frames.selectPlayersSubFrame import playerSelectBox
import json
import random
import re
from constants import BUTTON_DEFAULT_COLOUR,TEXT_FONT,FRAME_BG_DEFAULT_COLOUR

#skipped deactivating buttons

class selectPlayersFrame:
    def __init__(self, frame, gameID, gameFunc, dbHandler):
        self.__gameID = gameID
        self.__gameFunc = gameFunc
        self.__mainFrame = frame
        self.__dbHandler = dbHandler

        tk.Label(self.__mainFrame,text ="Choose players",font=(TEXT_FONT,30),bg=FRAME_BG_DEFAULT_COLOUR).place(relx=0.5,rely=0.08,anchor="center")

        #set up tk frames for children placement
        topLFrame = tk.Frame(self.__mainFrame,borderwidth=1,relief="solid")
        topLFrame.place(relx=0.25,rely=0.3,anchor="center",width=250,height=250)

        topMFrame = tk.Frame(self.__mainFrame,borderwidth=1,relief="solid")
        topMFrame.place(relx=0.5,rely=0.3,anchor="center",width=250,height=250)

        topRFrame = tk.Frame(self.__mainFrame,borderwidth=1,relief="solid")
        topRFrame.place(relx=0.75,rely=0.3,anchor="center",width=250,height=250)

        bottomLFrame = tk.Frame(self.__mainFrame,borderwidth=1,relief="solid")
        bottomLFrame.place(relx=0.25,rely=0.6,anchor="center",width=250,height=250)

        bottomMFrame = tk.Frame(self.__mainFrame,borderwidth=1,relief="solid")
        bottomMFrame.place(relx=0.5,rely=0.6,anchor="center",width=250,height=250)

        bottomRFrame = tk.Frame(self.__mainFrame,borderwidth=1,relief="solid")
        bottomRFrame.place(relx=0.75,rely=0.6,anchor="center",width=250,height=250)

        self.__playerList = []

        #instantiate player selection boxes and stored in a list for ease of access
        player1 = playerSelectBox(topLFrame, self.__changeOrderButtons)
        player2 = playerSelectBox(topMFrame, self.__changeOrderButtons)
        player3 = playerSelectBox(topRFrame, self.__changeOrderButtons)
        player4 = playerSelectBox(bottomLFrame, self.__changeOrderButtons)
        player5 = playerSelectBox(bottomMFrame, self.__changeOrderButtons)
        player6 = playerSelectBox(bottomRFrame, self.__changeOrderButtons)
        
        self.__playerList = [player1, player2, player3, player4, player5, player6]

        tk.Button(self.__mainFrame, text = "Continue",font=(TEXT_FONT,20), bd=4, command = lambda: self.__confirmChoice(), bg = BUTTON_DEFAULT_COLOUR).place(relx=0.5,rely=0.8,anchor="center")

    def __changeOrderButtons(self):
        #generates list of button indexes that have to be disabled
        orderList = []      
        for player in self.__playerList:
            if player.getIsPlaying():
                if player.getOrder() != 0:
                    orderList.append(player.getOrder())
            
            #for deactivating buttons
            for player in self.__playerList:
                player.deactivateOrderBs(orderList)
        
    def __confirmChoice(self):
        #used to check whether options are valid
        #all players must have a unique order
        #all players must have a unique none "" name
        #there must be 2<=No of players<=6

        orderList = []
        nameList = []
        typeList = []

        for players in self.__playerList:
            if players.getIsPlaying():
                orderList.append(players.getOrder())
                nameList.append(players.getName())
                typeList.append(players.getType())

        validNames = True
        for name in nameList:
            if not re.search("^([a-z]|[A-Z]|[0-9])([a-z]|[A-Z]|[0-9]|( |-)([a-z]|[A-Z]|[0-9]))*$",name):
                validNames = False
                break

        if len(nameList) >= 2 and len(set(nameList)) == len(nameList) and len(set(orderList)) == len(orderList) and not(0 in orderList) and validNames:
            self.__continue()

    def __continue(self):
        #setting up and writing data to db
        for i in range(len(self.__playerList)):
            if self.__playerList[i].getIsPlaying():
                self.__dbHandler.newPlayer(self.__playerList[i].getOrder(), self.__playerList[i].getName(), self.__playerList[i].getType(), self.__gameID)

        #removes tk children to prepare for next frame
        for widget in self.__mainFrame.winfo_children():
            widget.destroy()

        self.__gameFunc(self.__gameID)
 