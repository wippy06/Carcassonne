class feature:
    def __init__(self, featureType, tileList, meepleDict, CoAs, completed):
        self.__featureType = featureType
        self.__tileList = tileList
        self.__meepleDict = meepleDict
        self.__CoAs = CoAs
        self.__completed = completed

    #programming to interface
    #attributes are not altered as feature is discarded once not needed
    #done this way to not have to keep track and update features whenever board changes, reduces code
    def getMeepleList(self):
        return list(self.__meepleDict.values())