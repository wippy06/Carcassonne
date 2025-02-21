from .feature import feature

class board:
    def __init__(self):
        self.__board = {}

    def __generateFeature(self,coord,side):
        #requires a known point of coord and side then generates a feature object linking all the tiles
        featureType = self.__board[coord].getSide(side)

        #only calls recursive function when not a monestry as monestry tiles in feature are predetermined
        if featureType == "Monestry":

            #getting tile adjacencies for monestry surrounding
            tiles = []
            tileCheckList = [coord,(coord[0]+1,coord[1]),(coord[0]-1,coord[1]),(coord[0],coord[1]+1),(coord[0],coord[1]-1),(coord[0]+1,coord[1]+1),(coord[0]+1,coord[1]-1),(coord[0]-1,coord[1]+1),(coord[0]-1,coord[1]-1)]
            for tile in tileCheckList:
                if tile in self.__board:
                    tiles.append(tile)

            #completed var if monestry is completely surrounded
            if len(tiles) == 9:
                completed = True
            else:
                completed = False

            #add meeple if there is one on the centre
            meeples = {}
            if self.__board[coord].getClaimingPlayer() != "" and side == self.__board[coord].getClaimedSide():
                meeples[(coord,self.__board[coord].getClaimedSide())] = self.__board[coord].getClaimingPlayer()

        else:
            tileSides,completed,meeples = self.__generateFeatureFeatures(coord,side,set(),True,{})
            
            tiles = []
            for tileSide in tileSides:
                if tileSide[0] not in tiles:
                    tiles.append(tileSide[0])

        #counts coat of arms in case of scoring castles
        CoAs = 0
        for tile in tiles:
            if self.__board[tile].getCoA():
                CoAs +=1

        return feature(featureType,tiles,meeples,CoAs,completed)
    
    def __generateFeatureFeatures(self,coord,side,tileSet, completed, meeples):
        #recursive algorithm, acts as depth first search
        #nodes as sides of tile
        #edges as connections between tiles and tile sides

        #tileSet acts as visited nodes list
        #set to remove duplicates
        #base case when coord is in tileSet
        if (coord,side) not in tileSet and coord in self.__board:
            tileSet.add((coord,side))
            currentTile = self.__board[coord]

            connectionsList = [side] + currentTile.getConnections(side)

            #append results for side and connections on tiles, for loop used incase of multiple connected sides
            for connections in connectionsList:
                if connections == "North":
                    result = self.__generateFeatureFeatures((coord[0],coord[1]-1),"South",tileSet, completed,meeples)
                    tileSet.update(result[0])
                    completed = result[1]
                    meeples.update(result[2])
                elif connections == "South":
                    result = self.__generateFeatureFeatures((coord[0],coord[1]+1),"North",tileSet, completed,meeples)
                    tileSet.update(result[0])
                    completed = result[1]
                    meeples.update(result[2])
                elif connections == "East":
                    result = self.__generateFeatureFeatures((coord[0]+1,coord[1]),"West",tileSet, completed,meeples)
                    tileSet.update(result[0])
                    completed = result[1]
                    meeples.update(result[2])
                elif connections == "West":
                    result = self.__generateFeatureFeatures((coord[0]-1,coord[1]),"East",tileSet, completed,meeples)
                    tileSet.update(result[0])
                    completed = result[1]
                    meeples.update(result[2])

            #updating meeple dictionary, key as (coord,side) to prevent duplication of counting
            if currentTile.getClaimingPlayer() != "":
                if side == currentTile.getClaimedSide() or side in currentTile.getConnections(currentTile.getClaimedSide()):
                    meeples[(coord,currentTile.getClaimedSide())] = currentTile.getClaimingPlayer()

        #storing completed state in case of scoring feature later on
        if coord not in self.__board:
            completed = False 
        
        return tileSet,completed,meeples

    #programming to interface
    def placeTile(self,tile,coordinate):
        self.__board[coordinate] = tile

    def getBoard(self):
        return self.__board
    
    def getFeatureScore(self,coord,side):
        return self.__generateFeature(coord,side).getScoreChanges()
    
    def checkValidPlacement(self,tile,coordinate):       
        # list to reduce redundancy of coord checking
        coordinateCheckList = [coordinate,(coordinate[0],coordinate[1]-1),(coordinate[0],coordinate[1]+1),(coordinate[0]-1,coordinate[1]),(coordinate[0]+1,coordinate[1])]          

        #checks adjacencies of tiles
        tileAdjecent = False

        if coordinateCheckList[0] in self.__board:
            return False
        
        if coordinateCheckList[1] in self.__board:
            tileAdjecent=True
            if self.__board[coordinateCheckList[1]].getSide("South") != tile.getSide("North"):
                return False    
        if coordinateCheckList[2] in self.__board:
            tileAdjecent=True
            if self.__board[coordinateCheckList[2]].getSide("North") != tile.getSide("South"):
                return False  
        if coordinateCheckList[3] in self.__board:
            tileAdjecent=True
            if self.__board[coordinateCheckList[3]].getSide("East") != tile.getSide("West"):
                return False 
        if coordinateCheckList[4] in self.__board:
            tileAdjecent=True
            if self.__board[coordinateCheckList[4]].getSide("West") != tile.getSide("East"):
                return False  

        if not tileAdjecent:
            return False
        
        #to check if prexisting meeple attached to feature
        #done afer checking tile adjacencies to reduce number of times recursive algorithm needs to be called
        #greatly improves possible placements generation speed for bots
        if tile.getClaimingPlayer():
            claimedSide = tile.getClaimedSide()
            connectedSidesList = tile.getConnections(claimedSide)
            connectedSidesList.insert(0,claimedSide)
            
            for side in connectedSidesList:
                if side == "North" and coordinateCheckList[1] in self.__board and self.__generateFeature(coordinateCheckList[1],"South").getMeepleList() != []:
                    return False
                elif side == "South" and coordinateCheckList[2] in self.__board and self.__generateFeature(coordinateCheckList[2],"North").getMeepleList() != []:
                    return False
                elif side == "East" and coordinateCheckList[4] in self.__board and self.__generateFeature(coordinateCheckList[4],"West").getMeepleList() != []:
                    return False
                elif side == "West" and coordinateCheckList[3]in self.__board and self.__generateFeature(coordinateCheckList[3],"East").getMeepleList() != []:
                    return False
          
        return True
    
    def removeMeeple(self,tile):
        #returns orriginal claimer to know whos meeple count to increase
        currentClaimer = self.__board[tile].getClaimingPlayer()
        self.__board[tile].claimFeature("","")
        return currentClaimer
    
    def checkIfValidPlacements(self,tile):
        #getting adjacent coordinates list
        adjancentCoordList = []
        for coord in self.__board.keys():
            coordCheckList = [(coord[0]+1,coord[1]),(coord[0]-1,coord[1]),(coord[0],coord[1]+1),(coord[0],coord[1]-1)]
            for i in range(len(coordCheckList)):
                if coordCheckList[i] not in self.__board.keys():
                    adjancentCoordList.append(coordCheckList[i])

        #checking all adjacenies with tile
        for rotation in range(4):
            for coord in adjancentCoordList:
                if self.checkValidPlacement(tile,coord):
                    return True

            tile.rotate()

        return False
    
    def getAllValidPlacements(self,tile,meeples):
        #getting adjacent coordinates list
        adjancentCoordList = []
        for coord in self.__board.keys():
            coordCheckList = [(coord[0]+1,coord[1]),(coord[0]-1,coord[1]),(coord[0],coord[1]+1),(coord[0],coord[1]-1)]
            for i in range(len(coordCheckList)):
                if coordCheckList[i] not in self.__board.keys():
                    adjancentCoordList.append(coordCheckList[i])

        #checking valid placements then appending to placementList
        placementList = []
        
        for rotation in range(4):
            for coord in adjancentCoordList:
                tile.claimFeature("","")
                if self.checkValidPlacement(tile,coord):
                        placementList.append((rotation,"",coord[0],coord[1]))

                #only checks for meeples if bot has remaining meeples, optimisation to reduce instances of recursive alg
                if meeples != 0:
                    for meeplePlacment in ["Centre","North","South","East","West"]:
                        if tile.getSide(meeplePlacment) == None:
                            continue

                        tile.claimFeature(meeplePlacment,True)
                        if self.checkValidPlacement(tile,coord):
                            placementList.append((rotation,meeplePlacment,coord[0],coord[1]))

            tile.rotate()
            tile.claimFeature("","")

        return placementList