class board:
    def __init__(self):
        self.__board = {}

    def placeTile(self,tile,coordinate):
        self.checkValidPlacement(tile,coordinate)
        self.__board[coordinate] = tile

    def getBoard(self):
        return self.__board

    def checkValidPlacement(self,tile,coordinate):
        coordinateCheckList = [coordinate,(coordinate[0],coordinate[1]-1),(coordinate[0],coordinate[1]+1),(coordinate[0]-1,coordinate[1]),(coordinate[0]+1,coordinate[1])]
        
        tileAdjecent = False

        if coordinateCheckList[0] in self.__board:
            return False
        
        if coordinateCheckList[1] in self.__board:
            tileAdjecent=True
            if self.__board[coordinateCheckList[1]].getSouth() != tile.getNorth():
                return False    
        if coordinateCheckList[2] in self.__board:
            tileAdjecent=True
            if self.__board[coordinateCheckList[2]].getNorth() != tile.getSouth():
                return False  
        if coordinateCheckList[3] in self.__board:
            tileAdjecent=True
            if self.__board[coordinateCheckList[3]].getEast() != tile.getWest():
                return False 
        if coordinateCheckList[4] in self.__board:
            tileAdjecent=True
            if self.__board[coordinateCheckList[4]].getWest() != tile.getEast():
                return False  

        if not tileAdjecent:
            return False        
        return True
            
        