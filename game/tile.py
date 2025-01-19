class tile:
    def __init__(self, tileDict, order):
        self.__north = tileDict["North"]
        self.__south = tileDict["South"]
        self.__east = tileDict["East"]
        self.__west = tileDict["West"]
        self.__centre = tileDict["Centre"]

        self.__connections = {
            "North" : tileDict["Connections"]["North"],
            "South" : tileDict["Connections"]["South"],
            "East" : tileDict["Connections"]["East"],
            "West" : tileDict["Connections"]["West"]
        }

        self.__CoA = tileDict["CoA"]

        self.__tileOrder = order

    def getOrder(self):
        return self.__tileOrder