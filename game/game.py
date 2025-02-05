from constants import STARTING_TILE, PLAYER_COLOUR_LIST
import random
import json
import copy
from .board import board
from .tile import tile
from .tileStack import tileStack
from .player import player

class game:
    def __init__(self, gameFileDir, gameOverFunc):
        #load file to check whether game needs to be loaded or not
        #also sets seed for random lib so that game is the same when loaded
        #as well as player info
        self.__gameFileDir = gameFileDir
        self.__gameOver = gameOverFunc
        
        fileObj = open(self.__gameFileDir, "r")
        self.__gameFile = json.loads(fileObj.read())
        fileObj.close()

        random.seed(self.__gameFile["seed"])

        #players stored in dictionary with keys being colours
        #player keys are to store the order of players
        #so that list rotation for next player only has to rotate colour strings not player objects
        self.__playerDict = {}
        self.__playerKeys = []

        self.__generateTileStack()
        self.__generatePlayerDict()

        #board obj handles board methods eg checking if move is valid
        self.__board = board()

        #for keeping track of move for saving and loading game
        self.__placementMade = False
        self.__currentCoord = (0,0)
        self.__currentRotationsPreview = 0
        self.__currentRotations = 0
        self.__currentClaimSide = ""

    def setupBoard(self,canvas):
        #drawing start tile
        self.drawTile(canvas,False)
        self.__board.placeTile(self.__tileStack.getItem(), (0,0))
        self.__tileStack.stackPop()

        if self.__gameFile["moves"] != []:
            self.__loadPreviousMoves()

    def drawTile(self,canvas,preview):
        self.__tileStack.getItem().draw(canvas, preview)

    def placeTempTile(self, canvas, coord):
        #checks if placement is valid then changes current placement vars
        if self.__board.checkValidPlacement(self.__tileStack.getItem(), coord):
            self.__currentCoord = coord
            self.__currentRotations = self.__currentRotationsPreview
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
            amount = 1
        else:
            amount = 3

        for i in range(amount):
            self.__tileStack.getItem().rotate()
            self.__currentRotationsPreview += 1
            if self.__currentClaimSide == "North":
                self.__currentClaimSide = "West"
            elif self.__currentClaimSide == "East":
                self.__currentClaimSide = "North"
            elif self.__currentClaimSide == "South":
                self.__currentClaimSide = "East"
            elif self.__currentClaimSide == "West":
                self.__currentClaimSide = "South"

        self.drawTile(canvas,True)

    def claimFeature(self, side):
        #first checks if side picked is not already claimed
        #then checks if feature on side picked
        #then checks if meeples avaliable
        if self.__tileStack.getItem().getClaimedSide() != side:
            if side == "North" and self.__tileStack.getItem().getSide("North") != None or side == "South" and self.__tileStack.getItem().getSide("South") != None or side == "East" and self.__tileStack.getItem().getSide("East") != None or side == "West" and self.__tileStack.getItem().getSide("West") != None or side == "Centre" and self.__tileStack.getItem().getSide("Centre") != None:
                if self.__playerDict[self.__playerKeys[0]].getRemainingMeeples() != 0:
                    self.__tileStack.getItem().claimFeature(side, self.__playerKeys[0])
                    self.__currentClaimSide = side
        else:
            #removes claim
            self.__tileStack.getItem().claimFeature("", "")
            self.__currentClaimSide = ""

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
        #iterates through move list loaded, decodes and plays move
        #moves encoded as string "rotations,meeplePlacement,xCoord,yCoord"
        for move in self.__gameFile["moves"]:
            moveList = move.split(",")
            for i in range(int(moveList[0])):
                self.__tileStack.getItem().rotate()
            if moveList[1] != "":
                self.claimFeature(moveList[1])
                self.__playerDict[self.__playerKeys[0]].alterMeepleCount(-1)
            self.__board.placeTile(self.__tileStack.getItem(), (int(moveList[2]),int(moveList[3])))               

            #score
            sideOptions = ["North","South","East","West","Centre"]
            for side in sideOptions:
                if self.__tileStack.getItem().getSide(side) != None:
                    self.__scoreFeature((int(moveList[2]),int(moveList[3])),side,False)

            self.__nextPlayer()
            self.__tileStack.stackPop()

        #resets placment vars
        self.__placementMade = False
        self.__currentCoord = (0,0)
        self.__currentRotations = 0
        self.__currentRotationsPreview = 0
        self.__currentClaimSide = ""
            

    def __nextPlayer(self):
        #left list rotation
        #firstPlayer as place holder
        firstPlayer = self.__playerKeys[0]

        #iterates and swaps positions then adds placeHolder onto end
        for i in range(1, len(self.__playerKeys)):
            self.__playerKeys[i-1] = self.__playerKeys[i]

        self.__playerKeys[len(self.__playerKeys)-1] = firstPlayer

        return self.__playerKeys

    def __generatePlayerDict(self):
        playerList = self.__gameFile["players"]
        for i in range(len(playerList)):
            self.__playerDict[PLAYER_COLOUR_LIST[i]] = player(playerList[i], PLAYER_COLOUR_LIST[i])
            self.__playerKeys.append(PLAYER_COLOUR_LIST[i])

    def __generateTileStack(self):
        #method of methods to generate tile stack
        #tiles then random list the assign tiles to random list then sorts then push to stack
        tileList, tileCount = self.__generateTiles()
        self.__gameFile["tileNum"] = tileCount
        self.updateGameFile()
        randomList = self.__generateList(tileCount)
        self.__assignTileOrder(randomList,tileList)
        randomTileList = self.__mergeSort(tileList)
        self.__tileStack = tileStack(len(randomTileList)+1)
        self.__populateTileStack(randomTileList)

    def __assignTileOrder(self, randomList,tileList):
        for i in range(len(randomList)):
            tileList[i].setOrder(randomList[i])

    def __generateList(self, tileCount):
        generatedList = []
        for i in range(tileCount):
            generatedList.append(i+1)

        generatedList = self.__fisherYates(generatedList)

        return generatedList

    def __fisherYates(self, NumList):
        #used to randomise list
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
        tileList = []
        for key in tileKeys:
            for i in range(tileTypeCountDict[key]):
                #use of deep copy so that tiles hold a new list rather than pointer to list
                #separates tile attributes between tiles and avoids unwanted links between tiles
                tileList.append(tile(copy.deepcopy(tileDataDict[key]), key))
                tileCount += 1

        return tileList, tileCount

    def __mergeSort(self, arr):
        #used to sort tiles based on tileOrder
        #merge sort used as number of tiles needed to be sorted can potentially be large
        #uses recursion

        #base case for divisions
        if len(arr) == 1:
            return arr
        
        #split list in half, mid is middle and fills left and right
        mid = len(arr) // 2
        leftHalf = []
        rightHalf = []

        for i in range(mid):
            leftHalf.append(arr[i])

        for i in range(len(arr)-mid):
            rightHalf.append(arr[i + mid])

        #recursion for splits
        leftHalf = self.__mergeSort(leftHalf)
        rightHalf = self.__mergeSort(rightHalf)
        
        sortedList = []
        i= 0
        j= 0
        
        #merging list using while loop, i,j as index for left and right
        while i < len(leftHalf) and j < len(rightHalf):
            #puts in higher score to sortedList
            if leftHalf[i].getScore()>=rightHalf[j].getScore():
                sortedList.append(leftHalf[i])
                i+=1
            else:
                sortedList.append(rightHalf[j])
                j+=1

        #appends remaining ends of lists
        for index in range(len(leftHalf)-i):
            sortedList.append(leftHalf[index + i])

        for index in range(len(rightHalf)-j):
            sortedList.append(rightHalf[index + j])

        return sortedList
    
    def __populateTileStack(self,tileList):
        #to get starting tile
        tileData = open("tiles/tileData.json", "r")
        tileDataDict = json.loads(tileData.read())
        tileData.close()

        #push to stack
        for tileObj in tileList:
            self.__tileStack.stackAppend(tileObj)

        #add start tile
        startTile = tile(tileDataDict[STARTING_TILE],STARTING_TILE)
        startTile.setOrder(0)
        self.__tileStack.stackAppend(startTile)

    def __scoreFeature(self,coord,side,isFinal):
        #returns the score of the feature and whose score to increase
        score,playerList,completed,meepleTiles = self.__board.getFeatureScore(coord,side)

        #conditions for scoring
        if not isFinal:
            if completed:
                for player in playerList:
                    self.__playerDict[player].increaseScore(score)
                    self.__removeMeeples(meepleTiles)
        else:
            for player in playerList:
                self.__playerDict[player].increaseScore(score)
                self.__removeMeeples(meepleTiles)

    def __removeMeeples(self,meepleTiles):
        #removes the meeples in the tiles in the list
        for tile in meepleTiles:
            #self.__board.removeMeeple(tile) returns player key used to increase meeple count for player
            self.__playerDict[self.__board.removeMeeple(tile)].alterMeepleCount(1)

    def __checkGameEnd(self):
        if self.__tileStack.emptyCheck():
            boardDict = self.__board.getBoard()

            #cycle through all tiles on board, if tiles have a meeple score that feature
            for tile in list(boardDict.keys()):
                if boardDict[tile].getClaimingPlayer() != "":
                    self.__scoreFeature(tile,boardDict[tile].getClaimedSide(),True)

            #clear gameFile
            fileObj = open(self.__gameFileDir, "w")
            fileObj.close()

            self.__gameOver()
            

    def completeTurn(self):
        move = []
        if self.__placementMade:
            #sets up move to be appended to move queue to be saved and loaded
            move.append(self.__currentRotations%4)
            move.append(self.__currentClaimSide)
            move.append(self.__currentCoord[0])
            move.append(self.__currentCoord[1])

            self.__gameFile["moves"].append(",".join(str(i) for i in move))

            #alters board and current player attributes
            self.__board.placeTile(self.__tileStack.getItem(), self.__currentCoord)

            if self.__currentClaimSide != "":
                self.__playerDict[self.__playerKeys[0]].alterMeepleCount(-1)

            #score
            sideOptions = ["North","South","East","West","Centre"]
            for side in sideOptions:
                if self.__tileStack.getItem().getSide(side) != None:
                    self.__scoreFeature(self.__currentCoord,side,False)

            #resets placement vars
            self.__placementMade = False
            self.__currentCoord = (0,0)
            self.__currentRotations = 0
            self.__currentRotationsPreview = 0
            self.__currentClaimSide = ""

            self.__nextPlayer()
            self.__tileStack.stackPop()
            self.__checkGameEnd()