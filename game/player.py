class player:
    def __init__(self, infoDict):
        self.__name = infoDict["Name"]
        self.__playerType = infoDict["Type"]
        self.__score = 0
        self.__meeples = 7

    def getName(self):
        return self.__name
    
    def getScore(self):
        return self.__score
    
    def getRemainingMeeples(self):
        return self.__meeples