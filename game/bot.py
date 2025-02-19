from .player import player
from constants import OPPOSITION_MULT,INCOMPLETE_MULT_FUNCTION,MEEPLE_VALUE_FUNCTION,MEEPLE_REMAINING_VALUE_FUNCTION
import math
import copy

class bot(player):
    def __init__(self, infoDict, colour):
        super().__init__(infoDict,colour)

    def pickMove(self, placementList, boardObj, tileObj):
        placementDict = {}
        for placement in placementList:
            #deepcopy to simulate placements without affecting original board or tile
            board = copy.deepcopy(boardObj)
            tile = copy.deepcopy(tileObj)

            coord = (placement[2],placement[3])

            #place tile onto board copy
            for i in range(placement[0]):
                tile.rotate()

            if placement[1] != "":
                tile.claimFeature(placement[1],self._colour)

            board.placeTile(tile,coord)

            #determine tile placement evaluation
            turnCount = len(board.getBoard().values())
            sideOptions = ["North","South","East","West","Centre"]
            completedSides = []
            placementScore = 0

            for side in sideOptions:
                if tile.getSide(side) != None and tile.getSide(side) != "Village" and side not in completedSides:
                    placementScore += self.__evaluateFeature(board,coord,side,turnCount) 

                #done to remove double counting a feature if the sides of a tile are connected
                completedSides.append(side)
                for sideConnection in tile.getConnections(side):
                    if sideConnection not in completedSides:
                        completedSides.append(sideConnection)

            #checks adjacent tiles in case of completed monestry
            monestryCheckList = [(coord[0]+1,coord[1]),(coord[0]-1,coord[1]),(coord[0],coord[1]+1),(coord[0],coord[1]-1),(coord[0]+1,coord[1]+1),(coord[0]+1,coord[1]-1),(coord[0]-1,coord[1]+1),(coord[0]-1,coord[1]-1)]
            for monestryCoord in monestryCheckList:
                boardDict = board.getBoard()
                if monestryCoord in boardDict and board.getBoard()[monestryCoord].getSide("Centre") == "Monestry":
                    placementScore += self.__evaluateFeature(board,monestryCoord,"Centre",turnCount)

            placementDict[placement] = placementScore

        return max(placementDict, key=placementDict.get)             

    def __normalDistFunction(self,sigma,mu,yTranslation,yStrech,x):
        return yStrech*((math.e**((-(x-mu)**2)/(2*(sigma)**2)))/math.sqrt(2*math.pi*sigma**2))+yTranslation
    
    def __modulusFunction(self,yStrech,xSolution,xTranslation,x):
        return -yStrech*(abs(x-xTranslation)-xSolution)
    
    def __evaluateFeature(self,board,coord,side,turnCount):
        score,playerList,completed,meepleTiles = board.getFeatureScore(coord,side)

        #mathmatical functions to determine evaluation
        #modulus function used for remaining meeple bonus
        #normal distribution function used for meeples used multiplier and incomplete feature multiplier

        #meeple bonus used to insentivise bot to keep meeples remaining around 3
        #meeples used multiplier used to insentivise bot to place meeples at the start and end of the game
        #incomplete feature multiplier used to insentivise bot to complete features during the midgame

        if not completed:
            incompleteMult = self.__normalDistFunction(INCOMPLETE_MULT_FUNCTION[0],INCOMPLETE_MULT_FUNCTION[1],INCOMPLETE_MULT_FUNCTION[2],INCOMPLETE_MULT_FUNCTION[3],turnCount)
        else:
            incompleteMult = 1

        botMeepleCount = 0
        opponentMeepleCount = 0
        for meepleTile in meepleTiles:
            if board.getBoard()[meepleTile].getClaimedSide() == self._colour:
                botMeepleCount +=1
            else:
                opponentMeepleCount +=1

        if self._colour in playerList:
            botFeatureScore = score
        else:
            botFeatureScore = 0

        opponentFeatureScore = score*(len(playerList))-botFeatureScore

        botMeepleScore = botMeepleCount*self.__normalDistFunction(MEEPLE_VALUE_FUNCTION[0],MEEPLE_VALUE_FUNCTION[1],MEEPLE_VALUE_FUNCTION[2],MEEPLE_VALUE_FUNCTION[3],turnCount)
        opponentMeepleScore = opponentMeepleCount*self.__normalDistFunction(MEEPLE_VALUE_FUNCTION[0],MEEPLE_VALUE_FUNCTION[1],MEEPLE_VALUE_FUNCTION[2],MEEPLE_VALUE_FUNCTION[3],turnCount)

        meeplesRemainingBonus = self.__modulusFunction(MEEPLE_REMAINING_VALUE_FUNCTION[0],MEEPLE_REMAINING_VALUE_FUNCTION[1],MEEPLE_REMAINING_VALUE_FUNCTION[2],self._meeples)

        return incompleteMult*(botFeatureScore-botMeepleScore-OPPOSITION_MULT*(opponentFeatureScore-opponentMeepleScore))+meeplesRemainingBonus