import tkinter as tk
from constants import MINIMAP_MAX_SIZE,CONTROLS
from .subwindowBase import subwindowBase

class minimapWindow(subwindowBase):
    def __init__(self,window,board):
        self.__board = board

        super().__init__(window,"Minimap")

    def _displayMainFrame(self):
        #used to determine size of grid and size of tiles
        minX, maxX, minY, maxY = 0,0,0,0

        for coord in self.__board.keys():
            if coord[0]<minX:
                minX = coord[0]
            elif coord[0]>maxX:
                maxX = coord[0]

            if coord[1]<minY:
                minY = coord[1]
            elif coord[1]>maxY:
                maxY = coord[1]

        gridSizeX = maxX-minX+1
        gridSizeY = maxY-minY+1

        #offset used to translate coord key to grid list index
        offsetX = -minX
        offsetY = -minY

        tileSize = min(MINIMAP_MAX_SIZE[0]//gridSizeX,MINIMAP_MAX_SIZE[1]//gridSizeY)

        tileGridCanvasList = []
        #grid stored as 2D array for tile grid
        for i in range(gridSizeX):
            tileGridCanvasList.append([])
            for j in range(gridSizeY):
                tileGridCanvasList[i].append(tk.Canvas(self._mainFrame, width=tileSize, height=tileSize,highlightthickness=1, highlightbackground="black",bg="grey94"))

        for i in range(len(tileGridCanvasList)):
            for j in range(len(tileGridCanvasList[i])):
                tileGridCanvasList[i][j].grid(row=j,column=i)

        tileCoordList = list(self.__board.keys())
        #draws tiles within the grid
        for coord in tileCoordList:
            self.__board[coord].draw(tileGridCanvasList[coord[0]+offsetX][coord[1]+offsetY],False)

        self._window.bind(CONTROLS[14],lambda event: self._window.destroy())


        

