class player:
    def __init__(self, infoDict, colour):
        self.__name = infoDict["Name"]
        self.__playerType = infoDict["Type"]
        self.__score = 0
        self.__meeples = 7
        self.__colour = colour

    def getName(self):
        return self.__name
    
    def getScore(self):
        return self.__score
    
    def getRemainingMeeples(self):
        return self.__meeples
    
    def getColour(self):
        return self.__colour
    
    def increaseScore(self, increase):
        self.__score += increase