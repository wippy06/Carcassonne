import tkinter as tk
from constants import MINIMAP_MAX_SIZE

class minimapWindow:
    def __init__(self,window,board):

        minimapWindow = tk.Toplevel(window)
        minimapWindow.grab_set()
        minimapWindow.title("minimap")

        #used to determine size of grid and size of tiles
        minX, maxX, minY, maxY = 0,0,0,0

        for coord in board.keys():
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
                tileGridCanvasList[i].append(tk.Canvas(minimapWindow, width=tileSize, height=tileSize,highlightthickness=1, highlightbackground="black"))

        for i in range(len(tileGridCanvasList)):
            for j in range(len(tileGridCanvasList[i])):
                tileGridCanvasList[i][j].grid(row=j,column=i)

        tileCoordList = list(board.keys())
        #draws tiles within the grid
        for coord in tileCoordList:
            board[coord].draw(tileGridCanvasList[coord[0]+offsetX][coord[1]+offsetY],False)


        

