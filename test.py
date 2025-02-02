import tkinter as tk
import json

class tile:
    def __init__(self, tileDict, key):
        self.__tileKey = key

        self.__north = tileDict["North"]
        self.__south = tileDict["South"]
        self.__east = tileDict["East"]
        self.__west = tileDict["West"]
        self.__centre = tileDict["Centre"]

        self.__claimedSide = None
        self.__claimedPlayer = None

        self.__connections = {
            "North" : tileDict["Connections"]["North"],
            "South" : tileDict["Connections"]["South"],
            "East" : tileDict["Connections"]["East"],
            "West" : tileDict["Connections"]["West"]
        }

        self.__CoA = tileDict["CoA"]

        self.__tileOrder = 0

    def getScore(self):
        return self.__tileOrder
    
    def getKey(self):
        return self.__tileKey
    
    def setOrder(self, order):
        self.__tileOrder = order

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

    def draw(self, canvas, preview):
        canvas.update()
        width = canvas.winfo_width()
        height = canvas.winfo_height()

        negCastle = False
        road = False

        if ("South" in self.__connections["North"] and "North" in self.__connections["South"] and self.__south == "Castle" and self.__north == "Castle") or ("East" in self.__connections["West"] and "West" in self.__connections["East"] and self.__east == "Castle" and self.__west == "Castle"):
            negCastle = True
            canvas.create_rectangle((width,height),(0,0),fill="orange",width = 0)
            if self.__north != "Castle":
                canvas.create_oval((-width/8,-height),(width/8*9, height/4), fill="Green", width=0)
            if self.__south != "Castle":
                canvas.create_oval((-width/8,2*height),(width/8*9, height/4*3), fill="Green", width=0)
            if self.__east != "Castle":
                canvas.create_oval((width/4*3,-height/8),(width*2, height/8*9), fill="Green", width=0)
            if self.__west != "Castle":
                canvas.create_oval((width/4,-height/8),(-width, height/8*9), fill="Green", width=0)

        else:
            if self.__north == "Castle":
                canvas.create_arc((width, -height/4),(0, height/4),  start = 0, extent = 359, style=tk.CHORD, fill="orange", width=0, outline = "orange")
                if "West" in self.__connections["North"]:
                    canvas.create_rectangle((0,0),(width/2,height/2),fill = "orange", width=0)
                if "East" in self.__connections["North"]:
                    canvas.create_rectangle((width,0),(width/2,height/2),fill = "orange", width=0)
            if self.__south == "Castle":
                canvas.create_arc((width, height/4*3),(0, height/4*5),  start = 0, extent = 359, style=tk.CHORD, fill="orange", width=0, outline = "orange")
                if "West" in self.__connections["South"]:
                    canvas.create_rectangle((0,height),(width/2,height/2),fill = "orange", width=0)
                if "East" in self.__connections["South"]:
                    canvas.create_rectangle((width,height),(width/2,height/2),fill = "orange", width=0)
            if self.__east == "Castle":
                canvas.create_arc((width/4*3, 0),(width/4*5, height),  start = 0, extent = 359, style=tk.CHORD, fill="orange", width=0, outline = "orange")
            if self.__west == "Castle":
                canvas.create_arc((-width/4, 0),(width/4, height),  start = 0, extent = 359, style=tk.CHORD, fill="orange", width=0, outline = "orange")
            canvas.create_oval((width/4,height/4),(width/4*3,height/4*3), fill="green", width=0)
                
        if self.__north == "Road":
            canvas.create_rectangle((width/16*7,0),(width/16*9,height/16*9),fill="gray",width = 0)
            road = True
        if self.__south == "Road":
            canvas.create_rectangle((width/16*7,height),(width/16*9,height/16*7),fill="gray",width = 0)
            road = True
        if self.__east == "Road":
            canvas.create_rectangle((width,height/16*7),(width/16*7,height/16*9),fill="gray",width = 0)
            road = True
        if self.__west == "Road":
            canvas.create_rectangle((0,height/16*7),(width/16*9,height/16*9),fill="gray",width = 0)
            road = True

        if negCastle and road:
            canvas.create_rectangle((width/4,height/4),(width/4*3,height/4*3), fill="orange", width=0)

        if self.__centre == "Monestry":
            canvas.create_oval((width/8*3,height/8*3), (width/8*5,height/8*5), fill="red",width = 0)
        if self.__centre == "Village":
            canvas.create_rectangle((width/8*3,height/8*3), (width/8*5,height/8*5), fill="green",width = 0)

        if self.__CoA:
            canvas.create_rectangle((width/16,height/16), (width/16*3,height/16*3), fill="white",width = 0)
            canvas.create_rectangle((width/16,height/16), (width/8,height/8), fill="blue",width = 0)
            canvas.create_rectangle((width/8,height/8), (width/16*3,height/16*3), fill="blue",width = 0)

        if preview:
            if self.__north:
                canvas.create_oval((width/16*7,height/16),(width/16*9,height/16*3),fill="white",outline="black",width=width/100)
            if self.__south:
                canvas.create_oval((width/16*7,height/16*15),(width/16*9,height/16*13),fill="white",outline="black",width=width/100)
            if self.__east:
                canvas.create_oval((width/16*15,height/16*7),(width/16*13,height/16*9),fill="white",outline="black",width=width/100)
            if self.__west:
                canvas.create_oval((width/16,height/16*7),(width/16*3,height/16*9),fill="white",outline="black",width=width/100)
            if self.__centre=="Monestry":
                canvas.create_oval((width/16*7,height/16*7),(width/16*9,height/16*9),fill="white",outline="black",width=width/100)

size = 200

window = tk.Tk()
canvas = tk.Canvas(window, width=size, height=size, bg='black')
canvas.pack(anchor=tk.CENTER, expand=True)

tileData = open("tiles/tileData.json", "r")
tileDataDict = json.loads(tileData.read())
tileData.close()

tileObj = tile(tileDataDict["S"], "S")

tileObj.rotate()
tileObj.rotate()
tileObj.rotate()
tileObj.rotate()

tileObj.draw(canvas, True)

window.mainloop()