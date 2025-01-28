from constants import STARTING_TILE, PLAYER_COLOUR_LIST
import random
import json
from .board import board
from .tile import tile
from .tileStack import tileStack
from .player import player

class game:
    def __init__(self, gameFileDir):

        self.__gameFileDir = gameFileDir
        
        fileObj = open(self.__gameFileDir, "r")
        self.__gameFile = json.loads(fileObj.read())
        fileObj.close()

        random.seed(self.__gameFile["seed"])

        self.__tileList = []
        self.__playerDict = {}
        self.__playerKeys = []

        self.__generateTileStack()
        self.__generatePlayerDict()

        self.__board = board()

        #for keeping track of move
        self.__placementMade = False
        self.__currentCoord = (0,0)
        self.__currentRotations = 0
        self.__currentClaimSide = None

    def setupBoard(self,canvas):
        self.drawTile(canvas,False)
        self.__board.placeTile(self.__tileStack.getItem(), (0,0))
        self.__tileStack.stackPop()

        if self.__gameFile["moves"] != []:
            self.__loadPreviousMoves()

    def drawTile(self,canvas,preview):
        self.__tileStack.getItem().draw(canvas, preview)

    def placeTempTile(self, canvas, coord):
        if self.__board.checkValidPlacement(self.__tileStack.getItem(), coord):
            self.__currentCoord = coord
            self.__placementMade = True
            self.drawTile(canvas, False)
        else:
            self.__placementMade = False

    def tileRedraw(self,canvas,tile):
        tile.draw(canvas, False)

    def getBoard(self):
        return self.__board.getBoard()

    def rotatePreview(self,anticlockwise,canvas):
        if anticlockwise:
            self.__tileStack.getItem().rotate()
            self.__currentRotations += 1
        else:
            self.__tileStack.getItem().rotate()
            self.__tileStack.getItem().rotate()
            self.__tileStack.getItem().rotate()
            self.__currentRotations -= 1
        self.drawTile(canvas,True)

    def claimFeature(self, side):
        if self.__tileStack.getItem().getClaimingPlayer() == None:
            self.__tileStack.getItem().claimFeature(side, self.__playerDict[self.__playerKeys[0]])
            self.__currentClaimSide = side
        else:
            self.__tileStack.getItem().claimFeature(None, None)
            self.__currentClaimSide = None

    def getPlayerLeaderboard(self):
        playerScores = {}
        for player in self.__playerKeys:
            playerScores[self.__playerDict[player].getName()] = self.__playerDict[player].getScore()

        return playerScores
    
    def getTurnPlayerName(self):
        return self.__playerDict[self.__playerKeys[0]].getName()
    
    def getTurnPlayerMeeplesRemaining(self):
        return self.__playerDict[self.__playerKeys[0]].getRemainingMeeples()

    def getNumPlayers(self):
        return len(self.__playerKeys)
    
    def getTurnCount(self):
        return self.__tileStack.getMaxSize()-self.__tileStack.getSize()
    
    def getTilesRemaining(self):
        return self.__tileStack.getSize()

    def updateGameFile(self):
        fileObj = open(self.__gameFileDir, "w")
        fileObj.write(json.dumps(self.__gameFile, indent=4))
        fileObj.close()

    def __loadPreviousMoves(self):
        for move in self.__gameFile["moves"]:
            for i in range(move[0]):
                self.__tileStack.getItem().rotate()
            if move[1] != None:
                self.claimFeature(move[1])
            self.__board.placeTile(self.__tileStack.getItem(), tuple(move[2]))

            #increase player scores
            self.__nextPlayer()
            self.__tileStack.stackPop()

        self.__placementMade = False
        self.__currentCoord = (0,0)
        self.__currentRotations = 0
        self.__currentClaimSide = None
            

    def __nextPlayer(self):
        firstPlayer = self.__playerKeys[0]

        for i in range(1, len(self.__playerKeys)):
            self.__playerKeys[i-1] = self.__playerKeys[i]

        self.__playerKeys[len(self.__playerKeys)-1] = firstPlayer

        return self.__playerKeys

    def __generatePlayerDict(self):
        playerList = self.__gameFile["players"]
        for i in range(len(playerList)):
            self.__playerDict[i] = player(playerList[i], PLAYER_COLOUR_LIST[i])
            self.__playerKeys.append(i)

    def __generateTileStack(self):
        tileCount = self.__generateTiles()
        self.__gameFile["tileNum"] = tileCount
        self.updateGameFile()
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
            if leftHalf[i].getScore() >= rightHalf[j].getScore():
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

    def completeTurn(self):
        move = []
        if self.__placementMade:
            move.append(self.__currentRotations%4)
            move.append(self.__currentClaimSide)
            move.append(self.__currentCoord)

            self.__gameFile["moves"].append(move)

            self.__board.placeTile(self.__tileStack.getItem(), self.__currentCoord)

            self.__placementMade = False
            self.__currentCoord = (0,0)
            self.__currentRotations = 0
            self.__currentClaimSide = None

            #increase player scores
            self.__nextPlayer()
            self.__tileStack.stackPop()