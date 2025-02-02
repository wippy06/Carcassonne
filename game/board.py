from .feature import feature

class board:
    def __init__(self):
        self.__board = {}

    def placeTile(self,tile,coordinate):
        self.checkValidPlacement(tile,coordinate)
        self.__board[coordinate] = tile

    def getBoard(self):
        return self.__board
    
    def generateFeature(self,coord,side):
        featureType = self.__board[coord].getSide(side)
        tiles,completed,meeples = self.__generateTilesInFeature(coord,side,[],True,{})

        CoAs = 0
        for tile in tiles:
            if self.__board[tile].getCoA():
                CoAs +=1

        print(tiles,completed,CoAs,featureType,meeples)

    
    def __generateTilesInFeature(self,coord,side,tileList, completed, meeples):
        if coord not in tileList and coord in list(self.__board.keys()):
            tileList.append(coord)

            if side == "North":
                result = self.__generateTilesInFeature((coord[0],coord[1]-1),"South",tileList, completed,meeples)
                tileList += result[0]
                completed = result[1]
                meeples.update(result[2])
            elif side == "South":
                result = self.__generateTilesInFeature((coord[0],coord[1]+1),"North",tileList, completed,meeples)
                tileList += result[0]
                completed = result[1]
                meeples.update(result[2])
            elif side == "East":
                result = self.__generateTilesInFeature((coord[0]+1,coord[1]),"West",tileList, completed,meeples)
                tileList += result[0]
                completed = result[1]
                meeples.update(result[2])
            elif side == "West":
                result = self.__generateTilesInFeature((coord[0]-1,coord[1]),"East",tileList, completed,meeples)
                tileList += result[0]
                completed = result[1]
                meeples.update(result[2])

            connectionsList = self.__board[coord].getConnections(side)

            for connections in connectionsList:
                if connections == "North":
                    result = self.__generateTilesInFeature((coord[0],coord[1]-1),"South",tileList, completed,meeples)
                    tileList += result[0]
                    completed = result[1]
                    meeples.update(result[2])
                elif connections == "South":
                    result = self.__generateTilesInFeature((coord[0],coord[1]+1),"North",tileList, completed,meeples)
                    tileList += result[0]
                    completed = result[1]
                    meeples.update(result[2])
                elif connections == "East":
                    result = self.__generateTilesInFeature((coord[0]+1,coord[1]),"West",tileList, completed,meeples)
                    tileList += result[0]
                    completed = result[1]
                    meeples.update(result[2])
                elif connections == "West":
                    result = self.__generateTilesInFeature((coord[0]-1,coord[1]),"East",tileList, completed,meeples)
                    tileList += result[0]
                    completed = result[1]
                    meeples.update(result[2])

            if side == self.__board[coord].getClaimedSide() :
                meeples[(coord,side)] = self.__board[coord].getClaimingPlayer().getColour()

        if coord not in list(self.__board.keys()):
            completed = False 
        
        return list(set(tileList)),completed,meeples
    
    def __getFeatureClaim(self):
        #to do
        return None

    def checkValidPlacement(self,tile,coordinate):
        if self.__getFeatureClaim() != None:
            return False

        coordinateCheckList = [coordinate,(coordinate[0],coordinate[1]-1),(coordinate[0],coordinate[1]+1),(coordinate[0]-1,coordinate[1]),(coordinate[0]+1,coordinate[1])]
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
        return True
            
        