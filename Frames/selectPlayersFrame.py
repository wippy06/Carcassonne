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
        self.__topLFrame = tk.Frame(self.__mainFrame,borderwidth=1,relief="solid")
        self.__topLFrame.place(relx=0.25,rely=0.3,anchor="center",width=250,height=250)

        self.__topMFrame = tk.Frame(self.__mainFrame,borderwidth=1,relief="solid")
        self.__topMFrame.place(relx=0.5,rely=0.3,anchor="center",width=250,height=250)

        self.__topRFrame = tk.Frame(self.__mainFrame,borderwidth=1,relief="solid")
        self.__topRFrame.place(relx=0.75,rely=0.3,anchor="center",width=250,height=250)

        self.__bottomLFrame = tk.Frame(self.__mainFrame,borderwidth=1,relief="solid")
        self.__bottomLFrame.place(relx=0.25,rely=0.6,anchor="center",width=250,height=250)

        self.__bottomMFrame = tk.Frame(self.__mainFrame,borderwidth=1,relief="solid")
        self.__bottomMFrame.place(relx=0.5,rely=0.6,anchor="center",width=250,height=250)

        self.__bottomRFrame = tk.Frame(self.__mainFrame,borderwidth=1,relief="solid")
        self.__bottomRFrame.place(relx=0.75,rely=0.6,anchor="center",width=250,height=250)

        self.__playerList = []

        #instantiate player selection boxes and stored in a list for ease of access
        self.__player1 = playerSelectBox(self.__topLFrame, self.__changeOrderButtons)
        self.__player2 = playerSelectBox(self.__topMFrame, self.__changeOrderButtons)
        self.__player3 = playerSelectBox(self.__topRFrame, self.__changeOrderButtons)
        self.__player4 = playerSelectBox(self.__bottomLFrame, self.__changeOrderButtons)
        self.__player5 = playerSelectBox(self.__bottomMFrame, self.__changeOrderButtons)
        self.__player6 = playerSelectBox(self.__bottomRFrame, self.__changeOrderButtons)
        
        self.__playerList = [self.__player1, self.__player2, self.__player3, self.__player4, self.__player5, self.__player6]

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

    def __bubbleSort(self, playerList):
        #standard bubble sort used for sorting players into playing order
        #includes optimisations to stop if no swaps
        #bubble sort used as number of items needed to be sorted is small

        for i in range(len(playerList)):
            swaps = False

            for j in range(len(playerList)-i-1):
                if playerList[j].getOrder()>playerList[j+1].getOrder():
                    playerList[j],playerList[j+1]=playerList[j+1],playerList[j]
                    swaps = True

            if not swaps:
                break

        return playerList

    def __continue(self):
        #to sort players into playing order to be loaded into the file
        sortedPlayerList = self.__bubbleSort(self.__playerList)

        #setting up and writing data to save file
        for i in range(len(sortedPlayerList)):
            if sortedPlayerList[i].getIsPlaying():
                self.__dbHandler.newPlayer(i, sortedPlayerList[i].getName(), sortedPlayerList[i].getType(), self.__gameID)

        #removes tk children to prepare for next frame
        for widget in self.__mainFrame.winfo_children():
            widget.destroy()

        self.__gameFunc(self.__gameID)
 