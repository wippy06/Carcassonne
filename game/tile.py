import tkinter as tk
from constants import MONESTRY_COLOUR,CASTLE_COLOUR,FIELD_COLOUR,ROAD_COLOUR,COA_COLOUR_1,COA_COLOUR_2,UNCLAIMED_BG_COLOUR

class tile:
    def __init__(self, tileDict, key):
        self.__tileKey = key

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

        self.__tileOrder = 0

        self.__claimedBy = None
        self.__claimedSide = None

    def getNorth(self):
        return self.__north
    
    def getSouth(self):
        return self.__south
    
    def getEast(self):
        return self.__east
    
    def getWest(self):
        return self.__west
    
    def getClaimingPlayer(self):
        return self.__claimedBy
    
    def claimFeature(self,side,player):
        self.__claimedBy = player
        self.__claimedSide = side

    def rotate(self):
        #anti clockwise
        self.__north, self.__east, self.__south, self.__west = self.__east, self.__south, self.__west, self.__north
        self.__connections["North"], self.__connections["East"], self.__connections["South"], self.__connections["West"] = self.__connections["East"], self.__connections["South"], self.__connections["West"],self.__connections["North"]
        
        connectionKeys = list(self.__connections.keys())

        for key in connectionKeys:
            for i in range(len(self.__connections[key])):
                if self.__connections[key][i] == "North":
                    self.__connections[key][i] = "West"
                elif self.__connections[key][i] == "South":
                    self.__connections[key][i] = "East"
                elif self.__connections[key][i] == "East":
                    self.__connections[key][i] = "North"
                elif self.__connections[key][i] == "West":
                    self.__connections[key][i] = "South"

        if self.__claimedSide == "North":
            self.__claimedSide = "West"
        elif self.__claimedSide == "East":
            self.__claimedSide = "North"
        elif self.__claimedSide == "South":
            self.__claimedSide = "East"
        elif self.__claimedSide == "West":
            self.__claimedSide = "South"

    def draw(self, canvas, preview):
        canvas.update()
        width = canvas.winfo_width()
        height = canvas.winfo_height()

        canvas.create_rectangle((0,0),(width,height),fill=FIELD_COLOUR,width=0, outline = FIELD_COLOUR)

        negCastle = False
        road = False

        if ("South" in self.__connections["North"] and "North" in self.__connections["South"] and self.__south == "Castle" and self.__north == "Castle") or ("East" in self.__connections["West"] and "West" in self.__connections["East"] and self.__east == "Castle" and self.__west == "Castle"):
            negCastle = True
            canvas.create_rectangle((width,height),(0,0),fill=CASTLE_COLOUR,width = 0)
            if self.__north != "Castle":
                canvas.create_arc((width, -height/4),(0, height/4),  start = 0, extent = 359, style=tk.CHORD, fill=FIELD_COLOUR, width=0, outline = FIELD_COLOUR)
            if self.__south != "Castle":
                canvas.create_arc((width, height/4*3),(0, height/4*5),  start = 0, extent = 359, style=tk.CHORD, fill=FIELD_COLOUR, width=0, outline = FIELD_COLOUR)
            if self.__east != "Castle":
                canvas.create_arc((width/4*3, 0),(width/4*5, height),  start = 0, extent = 359, style=tk.CHORD, fill=FIELD_COLOUR, width=0, outline = FIELD_COLOUR)
            if self.__west != "Castle":
                canvas.create_arc((-width/4, 0),(width/4, height),  start = 0, extent = 359, style=tk.CHORD, fill=FIELD_COLOUR, width=0, outline = FIELD_COLOUR)

        else:
            if self.__north == "Castle":
                canvas.create_arc((width, -height/4),(0, height/4),  start = 0, extent = 359, style=tk.CHORD, fill=CASTLE_COLOUR, width=0, outline = CASTLE_COLOUR)
                if "West" in self.__connections["North"]:
                    canvas.create_rectangle((0,0),(width/2,height/2),fill = CASTLE_COLOUR, width=0)
                if "East" in self.__connections["North"]:
                    canvas.create_rectangle((width,0),(width/2,height/2),fill = CASTLE_COLOUR, width=0)
            if self.__south == "Castle":
                canvas.create_arc((width, height/4*3),(0, height/4*5),  start = 0, extent = 359, style=tk.CHORD, fill=CASTLE_COLOUR, width=0, outline = CASTLE_COLOUR)
                if "West" in self.__connections["South"]:
                    canvas.create_rectangle((0,height),(width/2,height/2),fill = CASTLE_COLOUR, width=0)
                if "East" in self.__connections["South"]:
                    canvas.create_rectangle((width,height),(width/2,height/2),fill = CASTLE_COLOUR, width=0)
            if self.__east == "Castle":
                canvas.create_arc((width/4*3, 0),(width/4*5, height),  start = 0, extent = 359, style=tk.CHORD, fill=CASTLE_COLOUR, width=0, outline = CASTLE_COLOUR)
            if self.__west == "Castle":
                canvas.create_arc((-width/4, 0),(width/4, height),  start = 0, extent = 359, style=tk.CHORD, fill=CASTLE_COLOUR, width=0, outline = CASTLE_COLOUR)
            canvas.create_oval((width/4,height/4),(width/4*3,height/4*3), fill=FIELD_COLOUR, width=0)
                
        if self.__north == "Road":
            canvas.create_rectangle((width/16*7,0),(width/16*9,height/16*9),fill=ROAD_COLOUR,width = 0)
            road = True
        if self.__south == "Road":
            canvas.create_rectangle((width/16*7,height),(width/16*9,height/16*7),fill=ROAD_COLOUR,width = 0)
            road = True
        if self.__east == "Road":
            canvas.create_rectangle((width,height/16*7),(width/16*7,height/16*9),fill=ROAD_COLOUR,width = 0)
            road = True
        if self.__west == "Road":
            canvas.create_rectangle((0,height/16*7),(width/16*9,height/16*9),fill=ROAD_COLOUR,width = 0)
            road = True

        if negCastle and road:
            canvas.create_rectangle((width/4,height/4),(width/4*3,height/4*3), fill=CASTLE_COLOUR, width=0)

        if self.__centre == "Monestry":
            canvas.create_oval((width/8*3,height/8*3), (width/8*5,height/8*5), fill=MONESTRY_COLOUR,width = 0)
        if self.__centre == "Village":
            canvas.create_rectangle((width/8*3,height/8*3), (width/8*5,height/8*5), fill=FIELD_COLOUR,width = 0)

        if self.__CoA:
            canvas.create_rectangle((width/16,height/16), (width/16*3,height/16*3), fill=COA_COLOUR_1,width = 0)
            canvas.create_rectangle((width/16,height/16), (width/8,height/8), fill=COA_COLOUR_2,width = 0)
            canvas.create_rectangle((width/8,height/8), (width/16*3,height/16*3), fill=COA_COLOUR_2,width = 0)

        if preview:
            if self.__north:
                canvas.create_oval((width/16*7,height/16),(width/16*9,height/16*3),fill=UNCLAIMED_BG_COLOUR,outline="black",width=width/100)
            if self.__south:
                canvas.create_oval((width/16*7,height/16*15),(width/16*9,height/16*13),fill=UNCLAIMED_BG_COLOUR,outline="black",width=width/100)
            if self.__east:
                canvas.create_oval((width/16*15,height/16*7),(width/16*13,height/16*9),fill=UNCLAIMED_BG_COLOUR,outline="black",width=width/100)
            if self.__west:
                canvas.create_oval((width/16,height/16*7),(width/16*3,height/16*9),fill=UNCLAIMED_BG_COLOUR,outline="black",width=width/100)
            if self.__centre=="Monestry":
                canvas.create_oval((width/16*7,height/16*7),(width/16*9,height/16*9),fill=UNCLAIMED_BG_COLOUR,outline="black",width=width/100)

        if self.__claimedBy and self.__claimedSide:
            if self.__claimedSide == "North":
                canvas.create_oval((width/16*7,height/16),(width/16*9,height/16*3),fill=self.__claimedBy.getColour(),outline="black",width=width/100)
            if self.__claimedSide == "South":
                canvas.create_oval((width/16*7,height/16*15),(width/16*9,height/16*13),fill=self.__claimedBy.getColour(),outline="black",width=width/100)
            if self.__claimedSide == "East":
                canvas.create_oval((width/16*15,height/16*7),(width/16*13,height/16*9),fill=self.__claimedBy.getColour(),outline="black",width=width/100)
            if self.__claimedSide == "West":
                canvas.create_oval((width/16,height/16*7),(width/16*3,height/16*9),fill=self.__claimedBy.getColour(),outline="black",width=width/100)
            if self.__claimedSide == "Centre":
                canvas.create_oval((width/16*7,height/16*7),(width/16*9,height/16*9),fill=self.__claimedBy.getColour(),outline="black",width=width/100)
 


    def getScore(self):
        return self.__tileOrder
    
    def getKey(self):
        return self.__tileKey
    
    def setOrder(self, order):
        self.__tileOrder = order