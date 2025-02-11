import tkinter as tk
from constants import BG_DEFAULT_COLOUR
from game.playerSelectionBox import playerSelectBox
import json
import random
import re

#skipped deactivating buttons

class selectPlayersFrame:
    def __init__(self, frame, gameSlot, gameFunc):
        self.__gameSlot = gameSlot
        self.__fileName = "gameSlots/slot"+str(self.__gameSlot)+".json"
        self.__gameFile = open(self.__fileName, "r+")
        self.__gameFunc = gameFunc
        self.__mainFrame = frame

        #set up tk frames for children placement
        self.__playerFrame = tk.Frame(frame)
        self.__playerFrame.pack(side="top")

        self.__topLFrame = tk.Frame(self.__playerFrame)
        self.__topLFrame.grid(column=0,row=0)

        self.__topMFrame = tk.Frame(self.__playerFrame)
        self.__topMFrame.grid(column=1,row=0)

        self.__topRFrame = tk.Frame(self.__playerFrame)
        self.__topRFrame.grid(column=2,row=0)

        self.__bottomLFrame = tk.Frame(self.__playerFrame)
        self.__bottomLFrame.grid(column=0,row=1)

        self.__bottomMFrame = tk.Frame(self.__playerFrame)
        self.__bottomMFrame.grid(column=1,row=1)

        self.__bottomRFrame = tk.Frame(self.__playerFrame)
        self.__bottomRFrame.grid(column=2,row=1)

        self.__playerList = []

        #instantiate player selection boxes and stored in a list for ease of access
        self.__player1 = playerSelectBox(self.__topLFrame, self.__changeOrderButtons)
        self.__player2 = playerSelectBox(self.__topMFrame, self.__changeOrderButtons)
        self.__player3 = playerSelectBox(self.__topRFrame, self.__changeOrderButtons)
        self.__player4 = playerSelectBox(self.__bottomLFrame, self.__changeOrderButtons)
        self.__player5 = playerSelectBox(self.__bottomMFrame, self.__changeOrderButtons)
        self.__player6 = playerSelectBox(self.__bottomRFrame, self.__changeOrderButtons)
        
        self.__playerList = [self.__player1, self.__player2, self.__player3, self.__player4, self.__player5, self.__player6]

        tk.Button(self.__playerFrame, text = "Continue", command = lambda: self.__confirmChoice()).grid(column=1, row=2)

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

        if len(nameList) >= 2 and len(list(set(nameList))) == len(nameList) and len(list(set(orderList))) == len(orderList) and not(0 in orderList) and "player" in typeList and validNames:
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
        #seed giving max of 100000 different games
        #seed used for loading game so tile order does not have to be stored 
        seed = str(random.randint(0,99999))

        #to fill seed with leading 0 as random is int initially
        while(len(seed) != 5):
            seed = "0" + seed

        #to sort players into playing order to be loaded into the file
        sortedPlayerList = self.__bubbleSort(self.__playerList)

        fullPlayerList = []

        #setting up and writing data to save file
        for player in sortedPlayerList:
            if player.getIsPlaying():
                playerDict = {"Name" : player.getName(), "Type" : player.getType()}
                fullPlayerList.append(playerDict)         

        self.__gameFile.write(json.dumps({"seed":seed,"players":fullPlayerList,"moves":[], "tileNum":0}, indent=4))

        #removes tk children to prepare for next window
        for widget in self.__mainFrame.winfo_children():
            widget.destroy()
            
        self.__gameFile.close()
        self.__gameFunc(self.__fileName)
 