class achievement:
    def __init__(self, playerDict, claimNumDict):
        #dictionaries used to determine achievements
        self.__playerDict = playerDict
        self.__claimNumDict = claimNumDict

    #methods to work out which achievements have been completed
    def getArchitects(self):
        if self.__claimNumDict["Castle"] < 15:
            return False
        return True
    
    def getTravellers(self):
        if self.__claimNumDict["Road"] < 20:
            return False
        return True
        
    def getMonks(self):
        if self.__claimNumDict["Monestry"] < 5:
            return False
        return True
    
    def getExperts(self):
        scoreTotal = 0
        for player in self.__playerDict.values():
            scoreTotal += player.getScore()

        if scoreTotal < 150:
            return False
        return True
    
    def getCollectors(self):
        if self.__claimNumDict["Castle"] + self.__claimNumDict["Road"] + self.__claimNumDict["Monestry"] < 30:
            return False
        return True
    
    def getMeeplePeople(self):
        for player in self.__playerDict.values():
            if player.getRemainingMeeples() != 7:
                return False
        return True