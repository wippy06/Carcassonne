from constants import STARTING_TILE
import random
import json
from .tile import tile
from .tileStack import tileStack
from .player import player

class game:
    def __init__(self, gameFile):
        
        fileObj = open(gameFile, "r")
        self.__gameFile = json.loads(fileObj.read())
        fileObj.close()

        random.seed(self.__gameFile["Seed"])

        self.__tileList = []
        self.__playerDict = {}
        self.__playerKeys = []
        self.__moves = self.__gameFile["moves"]

        self.__generateTileStack()
        self.__generatePlayerDict()

        if self.__moves != 0:
            self.__loadPreviousMoves()

        '''
        #test player generation and list rotation for next turn
        for key in self.__playerKeys:
            print(self.__playerDict[key].getName())

        self.__nextPlayer()

        for key in self.__playerKeys:
            print(self.__playerDict[key].getName())
        
        #testing tile shuffle
        for i in range(self.__tileStack.getSize()):
            print(self.__tileStack.getItem().getOrder(),self.__tileStack.getItem().getKey())
            self.__tileStack.stackPop()
        '''

    def __loadPreviousMoves(self):
        pass

    def __nextPlayer(self):
        firstPlayer = self.__playerKeys[0]

        for i in range(1, len(self.__playerKeys)):
            self.__playerKeys[i-1] = self.__playerKeys[i]

        self.__playerKeys[len(self.__playerKeys)-1] = firstPlayer

        return self.__playerKeys

    def __generatePlayerDict(self):
        playerList = self.__gameFile["Players"]
        for i in range(len(playerList)):
            self.__playerDict[i] = player(playerList[i])
            self.__playerKeys.append(i)

    def __generateTileStack(self):
        tileCount = self.__generateTiles()
        randomList = self.__generateList(tileCount)
        self.__assignTileOrder(randomList)
        randomTileList = self.__mergeSort(self.__tileList)
        self.__tileStack = tileStack(len(randomTileList)+1)
        self.__populateTileStack(randomTileList)

    def __assignTileOrder(self, randomList):
        for i in range(len(randomList)):
            self.__tileList[i].setOrder(randomList[i])

    def __generateList(self, tileCount):
        generatedList = []
        for i in range(tileCount):
            generatedList.append(i+1)

        generatedList = self.__fisherYates(generatedList)

        return generatedList

    def __fisherYates(self, NumList):
        for i in range(len(NumList) - 1,0,-1):
            j = random.randint(0, i)
            NumList[i], NumList[j] = NumList[j], NumList[i]

        return NumList
    
    def __generateTiles(self):
        tileData = open("tiles/tileData.json", "r")
        tileDataDict = json.loads(tileData.read())
        tileData.close()

        tileTypeCount = open("tiles/tileCount.json", "r")
        tileTypeCountDict = json.loads(tileTypeCount.read())
        tileTypeCount.close()

        tileKeys = tileTypeCountDict.keys()

        tileCount = 0
        for key in tileKeys:
            for i in range(tileTypeCountDict[key]):
                self.__tileList.append(tile(tileDataDict[key], key))
                tileCount += 1

        return tileCount

    def __mergeSort(self, arr):
        if len(arr) == 1:
            return arr
        
        mid = len(arr) // 2
        leftHalf = []
        rightHalf = []

        for i in range(mid):
            leftHalf.append(arr[i])

        for i in range(len(arr)-mid):
            rightHalf.append(arr[i + mid])

        leftHalf = self.__mergeSort(leftHalf)
        rightHalf = self.__mergeSort(rightHalf)
        
        sortedList = []
        i = 0
        j=0
        
        while i < len(leftHalf) and j < len(rightHalf):
            if leftHalf[i].getOrder() >= rightHalf[j].getOrder():
                sortedList.append(leftHalf[i])
                i += 1
            else:
                sortedList.append(rightHalf[j])
                j += 1

        for index in range(len(leftHalf)-i):
            sortedList.append(leftHalf[index + i])

        for index in range(len(rightHalf)-j):
            sortedList.append(rightHalf[index + j])

        return sortedList
    
    def __populateTileStack(self,tileList):
        tileData = open("tiles/tileData.json", "r")
        tileDataDict = json.loads(tileData.read())
        tileData.close()

        for tileObj in tileList:
            self.__tileStack.stackAppend(tileObj)

        startTile = tile(tileDataDict[STARTING_TILE],STARTING_TILE)
        startTile.setOrder(0)
        self.__tileStack.stackAppend(startTile)

