from constants import STARTING_TILE, PLAYER_COLOUR_LIST
import random
import json
import copy
from .board import board
from .tile import tile
from .tileStack import tileStack
from .player import player
from .bot import bot

class game:
    def __init__(self, gameID, gameOverFunc, dbHandler):
        #load file to check whether game needs to be loaded or not
        #also sets seed for random lib so that game is the same when loaded
        #as well as player info
        self.__gameID = gameID
        self.__dbHandler = dbHandler
        self.__gameOver = gameOverFunc

        random.seed(self.__dbHandler.getGameSeed(self.__gameID))

        #players stored in dictionary with keys being colours
        #player keys are to store the order of players
        #so that list rotation for next player only has to rotate colour strings not player objects
        self.__playerDict = {}
        self.__playerKeys = []
        self.__placementList = self.__dbHandler.getMoveList(self.__gameID)

        self.__generateTileStack()
        self.__generatePlayerDict()

        #board obj handles board methods eg checking if placement is valid
        self.__board = board()

        #for keeping track of placement for saving and loading game
        self.__tempRotations = 0
        self.__tempClaimSide = ""
        self.__placementMade = False
        self.__currentCoord = None
        self.__currentRotations = 0
        self.__currentClaimSide = ""

    def setupBoard(self,canvas,redrawFrameFunc):
        #drawing start tile
        self.drawTile(canvas,False)
        self.__board.placeTile(self.__tileStack.getItem(), (0,0))
        self.__tileStack.stackPop()

        if self.__placementList != []:
            #iterates through placement list loaded, decodes and plays move
            for move in self.__placementList:
                self.__loadMove(move)

        while self.__checkIfBot():
            self.__generatePlacement()
            redrawFrameFunc()

            if self.checkGameEnd():
                break
     
    def drawTile(self,canvas,preview):
        self.__tileStack.getItem().draw(canvas, preview)

    def checkIfRemoveTempTile(self,coord):
        if coord == self.__currentCoord and self.__tempClaimSide == self.__currentClaimSide and self.__tempRotations == self.__currentRotations:
            return True
        return False

    def placeTempTile(self, canvas, coord):
        #checks if placement is valid then changes current placement vars
        if self.__board.checkValidPlacement(self.__tileStack.getItem(), coord):
            self.__currentCoord = coord
            self.__currentClaimSide = self.__tempClaimSide
            self.__currentRotations = self.__tempRotations
            self.__placementMade = True
            self.drawTile(canvas, False)
        else:
            self.__placementMade = False
            self.__currentCoord = None

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
            self.__tempRotations += 1

        self.__tempClaimSide = self.__tileStack.getItem().getClaimedSide()

        self.drawTile(canvas,True)

    def claimFeature(self, side):
        #first checks if side picked is not already claimed
        #then checks if feature on side picked
        #then checks if meeples avaliable
        if side == "remove":
            #removes claim for when keys are used
            self.__tileStack.getItem().claimFeature("", "")
            self.__tempClaimSide = ""
            return

        if self.__tileStack.getItem().getClaimedSide() != side:
            if side == "North" and self.__tileStack.getItem().getSide("North") != None or side == "South" and self.__tileStack.getItem().getSide("South") != None or side == "East" and self.__tileStack.getItem().getSide("East") != None or side == "West" and self.__tileStack.getItem().getSide("West") != None or side == "Centre" and self.__tileStack.getItem().getSide("Centre") == "Monestry":
                if self.__playerDict[self.__playerKeys[0]].getRemainingMeeples() != 0:
                    self.__tileStack.getItem().claimFeature(side, self.__playerKeys[0])
                    self.__tempClaimSide = side
        else:
            #removes claim
            self.__tileStack.getItem().claimFeature("", "")
            self.__tempClaimSide = ""

    def getPlayerLeaderboard(self):
        playerScores = {}
        for player in self.__playerKeys:
            playerScores[self.__playerDict[player].getName()] = [self.__playerDict[player].getScore(),player]

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

    def updateRecord(self):
        loadedMoves = self.__dbHandler.getMoveList(self.__gameID)

        for i in range(len(self.__placementList)):
            if self.__placementList[i] not in loadedMoves:
                self.__dbHandler.newMove(i, self.__placementList[i][0],self.__placementList[i][1],self.__placementList[i][2],self.__placementList[i][3],self.__gameID)

    def __scoreTiles(self,coord):
        sideOptions = ["North","South","East","West","Centre"]
        for side in sideOptions:
            if self.__tileStack.getItem().getSide(side) != None:
                self.__scoreFeature(coord,side,False)

        #checks adjacent tiles in case of completed monestry
        monestryCheckList = [(coord[0]+1,coord[1]),(coord[0]-1,coord[1]),(coord[0],coord[1]+1),(coord[0],coord[1]-1),(coord[0]+1,coord[1]+1),(coord[0]+1,coord[1]-1),(coord[0]-1,coord[1]+1),(coord[0]-1,coord[1]-1)]
        for monestryCoord in monestryCheckList:
            boardDict = self.__board.getBoard()
            if monestryCoord in boardDict and self.__board.getBoard()[monestryCoord].getSide("Centre") == "Monestry":
                self.__scoreFeature(monestryCoord,"Centre",False)

    def __loadMove(self,move):
        #moves encoded as string "rotations,meeplePlacement,xCoord,yCoord"
        for i in range(int(move[0])):
            self.__tileStack.getItem().rotate()
        if move[1] != "":
            self.claimFeature(move[1])
            self.__playerDict[self.__playerKeys[0]].alterMeepleCount(-1)
        self.__board.placeTile(self.__tileStack.getItem(), (int(move[2]),int(move[3])))               

        #score
        self.__scoreTiles((int(move[2]),int(move[3])))

        self.__nextPlayer()
        self.__tileStack.stackPop()

        if not self.checkGameEnd():
            #check if there is a valid placment for next tile
            if not self.__board.checkIfValidPlacements(self.__tileStack.getItem()):
                self.__alterTileStack()

        #resets placment vars
        self.__tempRotations = 0
        self.__tempClaimSide = ""
        self.__placementMade = False
        self.__currentCoord = None
        self.__currentRotations = 0
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
        playerList = self.__dbHandler.getGamePlayerInfo(self.__gameID)
        for i in range(len(playerList)):
            if playerList[i][1] == "player":
                self.__playerDict[PLAYER_COLOUR_LIST[i]] = player(playerList[i], PLAYER_COLOUR_LIST[i])
            else:
                self.__playerDict[PLAYER_COLOUR_LIST[i]] = bot(playerList[i], PLAYER_COLOUR_LIST[i])
            self.__playerKeys.append(PLAYER_COLOUR_LIST[i])

    def __generateTileStack(self):
        #method of methods to generate tile stack
        #tiles then random list the assign tiles to random list then sorts then push to stack
        tileList, tileCount = self.__generateTiles()
        randomList = self.__generateRandomNumberList(tileCount)
        self.__assignTileOrder(randomList,tileList)
        randomTileList = self.__mergeSort(tileList)
        self.__tileStack = tileStack(len(randomTileList)+1)
        self.__populateTileStack(randomTileList)

    def __assignTileOrder(self, randomList,tileList):
        for i in range(len(randomList)):
            tileList[i].setOrder(randomList[i])

    def __generateRandomNumberList(self, tileCount):
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
        tileData = open("jsonFiles/tileData.json", "r")
        tileDataDict = json.loads(tileData.read())
        tileData.close()

        tileTypeCount = open("jsonFiles/tileCount.json", "r")
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
        tileData = open("jsonFiles/tileData.json", "r")
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
            playerKey = self.__board.removeMeeple(tile)
            if playerKey != "":
               self.__playerDict[playerKey].alterMeepleCount(1)

    def checkGameEnd(self):
        if self.__tileStack.emptyCheck():
            boardDict = self.__board.getBoard()

            #cycle through all tiles on board, if tiles have a meeple score that feature
            for tile in list(boardDict.keys()):
                if boardDict[tile].getClaimingPlayer() != "":
                    self.__scoreFeature(tile,boardDict[tile].getClaimedSide(),True)

            #disable game
            self.__dbHandler.disableGame(self.__gameID)

            self.__gameOver()

            return True
        return False
    
    def getCurrentCoord(self):
        return self.__currentCoord
            
    def completeTurn(self,updateDisplay):
        if self.__placementMade:
            #sets up move to be appended to move queue to be saved and loaded
            move = (self.__currentRotations%4,self.__currentClaimSide,self.__currentCoord[0],self.__currentCoord[1])

            self.__placementList.append(move)

            #to sync up preview rotations with board placment rotations
            for i in range(self.__tempRotations-self.__currentRotations):
                self.__tileStack.getItem().rotate()
                self.__tileStack.getItem().rotate()
                self.__tileStack.getItem().rotate()
            
            #to sync up preview claim with board claim
            if self.__currentClaimSide != "":
                self.__tileStack.getItem().claimFeature(self.__currentClaimSide,self.__playerKeys[0])
            else:
                self.__tileStack.getItem().claimFeature(self.__currentClaimSide,"")

            #alters board and current player attributes
            self.__board.placeTile(self.__tileStack.getItem(), self.__currentCoord)

            if self.__currentClaimSide != "":
                self.__playerDict[self.__playerKeys[0]].alterMeepleCount(-1)

            #score
            self.__scoreTiles(self.__currentCoord)

            #resets placement vars
            self.__tempRotations = 0
            self.__tempClaimSide = ""
            self.__placementMade = False
            self.__currentCoord = None
            self.__currentRotations = 0
            self.__currentClaimSide = ""

            self.__nextPlayer()
            self.__tileStack.stackPop()
            if not self.checkGameEnd():
                #check if there is a valid placment for next tile
                if not self.__board.checkIfValidPlacements(self.__tileStack.getItem()):
                    self.__alterTileStack()

            #logic to handle bot moves and game over state
            while self.__checkIfBot():
                if self.checkGameEnd():
                    return True
                
                updateDisplay()
                self.__generatePlacement()

            if self.checkGameEnd():
                return True
            
            updateDisplay()
            return False
        
    def __alterTileStack(self):
        #temp stack to hold tiles
        newStack = tileStack(self.__tileStack.getSize())

        #load tiles off stack until a tile with a valid placement is found
        while not self.__board.checkIfValidPlacements(self.__tileStack.getItem()):
            newStack.stackAppend(self.__tileStack.getItem())
            self.__tileStack.stackPop()

            if self.__tileStack.emptyCheck():
                self.__gameOver()
                return
            
        #load tiles back onto stack then push valid placeable tile
        placeHolder = self.__tileStack.getItem()
        self.__tileStack.stackPop()

        while not newStack.emptyCheck():  
            self.__tileStack.stackAppend(newStack.getItem())
            newStack.stackPop()

        self.__tileStack.stackAppend(placeHolder)

    def __generatePlacement(self):
        #deepcopy to avoid changing data related to actual game tile
        validPlacementList = self.__board.getAllValidPlacements(copy.deepcopy(self.__tileStack.getItem()),self.__playerDict[self.__playerKeys[0]].getRemainingMeeples())
        
        placement = self.__playerDict[self.__playerKeys[0]].pickMove(validPlacementList, self.__board, self.__tileStack.getItem())

        self.__placementList.append(placement)

        self.__loadMove(placement)

    def __checkIfBot(self):
        if self.__playerDict[self.__playerKeys[0]].getType() == "player":
            return False
        return True