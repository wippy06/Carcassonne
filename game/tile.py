class Tile:
    def __init__(self, tileDict):
        north = tileDict["North"]
        south = tileDict["South"]
        east = tileDict["East"]
        west = tileDict["West"]
        centre = tileDict["Centre"]

        connections = {
            "North" : tileDict["Connections"]["North"],
            "South" : tileDict["Connections"]["South"],
            "East" : tileDict["Connections"]["East"],
            "West" : tileDict["Connections"]["West"]
        }

        CoA = tileDict["CoA"]