class feature:
    def __init__(self, featureType, tileList, meepleDict, CoAs, completed):
        self.__featureType = featureType
        self.__tileList = tileList
        self.__meepleDict = meepleDict
        self.__CoAs = CoAs
        self.__completed = completed

    #programming to interface and encapsulating what varies
    #attributes are not altered as feature is discarded once not needed
    #done this way to not have to keep track and update features whenever board changes, reduces code
    def getMeepleList(self):
        return list(self.__meepleDict.values())
    
    def getTileList(self):
        return self.__tileList
    
    def getScoreChanges(self):
        if self.__meepleDict == {}:
            return 0,[],False
        #generate list of players that will increase scores

        #dictionary of playerKeys and haw many meeples for values
        playerMeepleDict = {}
        for meeple in list(self.__meepleDict.values()):
            if meeple not in playerMeepleDict:
                playerMeepleDict[meeple] = 1
            else:
                playerMeepleDict[meeple] += 1

        maxMeeples = max(list(playerMeepleDict.values()))

        #compare player meeple values iteratively to determine player keys to be increased in score
        playerList = []
        for playerKey in list(playerMeepleDict.keys()):
            if playerMeepleDict[playerKey] == maxMeeples:
                playerList.append(playerKey)

        #scoring logic
        score = 0
        if self.__featureType == "Castle":
            if self.__completed:
                score = len(self.__tileList) + self.__CoAs*2
            else:
                score = len(self.__tileList) + self.__CoAs
        else:
            score = len(self.__tileList)

        return score, playerList, self.__completed

            
