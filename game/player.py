class player:
    def __init__(self, infoDict, colour):
        #collection of player attributes
        self._name = infoDict[0]
        self._playerType = infoDict[1]
        self._score = 0
        self._meeples = 7
        self._colour = colour

    #methods to program to an interface
    def getName(self):
        return self._name
    
    def getScore(self):
        return self._score
    
    def getRemainingMeeples(self):
        return self._meeples
    
    def getColour(self):
        return self._colour
    
    def increaseScore(self, increase):
        self._score += increase

    def alterMeepleCount(self, amount):
        #only alter not increas and decrease as ammount can be -ve therefoe reducing code
        self._meeples += amount

    def getType(self):
        return self._playerType