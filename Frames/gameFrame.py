import tkinter as tk
from game.game import game
from frames.minimapWindow import minimapWindow
from constants import TILE_SIZE, TILE_GRID_X,TILE_GRID_Y

class gameFrame:
    def __init__(self,frame, gameFile, leaderBoardFunc):
        #init game object, gameFrame handles user interface, game obj handles game operations
        self.__game = game(gameFile,self.__gameOver)
        self.__leaderBoardFunc = leaderBoardFunc
        self.__mainFrame = frame

        #creating frames
        self.__leftSideBarFrame = tk.Frame(self.__mainFrame)
        self.__leftSideBarFrame.pack(side="left")

        self.__scoreFrame = tk.Frame(self.__leftSideBarFrame,highlightbackground="black",highlightthickness=1)
        self.__scoreFrame.grid(column=0, row=0)

        #done as list to reduce code
        self.__scoreLableList = []
        for i in range(self.__game.getNumPlayers()):
            self.__scoreLableList.append(tk.Label(self.__scoreFrame, text=str(i+1)+". "))
            self.__scoreLableList[i].pack(side = "top")

        #tile preview frame
        self.__tilePreviewFrame = tk.Frame(self.__leftSideBarFrame,highlightbackground="black",highlightthickness=1)
        self.__tilePreviewFrame.grid(column=0, row=1)

        self.__tileCanvas = tk.Canvas(self.__tilePreviewFrame, width=TILE_SIZE, height=TILE_SIZE)
        self.__tileCanvas.pack(side = "top")
        self.__tileCanvas.bind("<Button-1>",lambda event:self.__placeMeeple(event.x,event.y))

        self.__rotateButtonFrame = tk.Frame(self.__tilePreviewFrame)
        self.__rotateButtonFrame.pack()
        
        self.__tileRotateClock = tk.Button(self.__rotateButtonFrame, text = "clockwise", command = lambda:self.__game.rotatePreview(False, self.__tileCanvas))
        self.__tileRotateAntiClock = tk.Button(self.__rotateButtonFrame, text = "anticlockwise", command = lambda:self.__game.rotatePreview(True, self.__tileCanvas))
        self.__tileRotateClock.pack(side="right")
        self.__tileRotateAntiClock.pack(side="left")

        self.__tileRemainingLable = tk.Label(self.__tilePreviewFrame, text = "Tiles remaining: ")
        self.__tileRemainingLable.pack()

        #extra info frame
        self.__extraInfoFrame = tk.Frame(self.__leftSideBarFrame,highlightbackground="black",highlightthickness=1)
        self.__extraInfoFrame.grid(column=0, row=2)

        self.__turnCountLable = tk.Label(self.__extraInfoFrame,text = "Turn number: ")
        self.__turnPlayerLable = tk.Label(self.__extraInfoFrame, text="Turn player: ")
        self.__MeepleCountLable = tk.Label(self.__extraInfoFrame,text="Meeples remaining: ")

        self.__turnCountLable.pack()
        self.__turnPlayerLable.pack()
        self.__MeepleCountLable.pack()

        #map movement frame
        self.__mapViewKeypadFrame = tk.Frame(self.__leftSideBarFrame,highlightbackground="black",highlightthickness=1)
        self.__mapViewKeypadFrame.grid(column=0,row=3)

        self.__viewUpButton = tk.Button(self.__mapViewKeypadFrame, text="Up", command= lambda:self.__moveView("Up"))
        self.__viewUpButton.pack()

        self.__viewDownButton = tk.Button(self.__mapViewKeypadFrame, text="Down", command= lambda:self.__moveView("Down"))
        self.__viewDownButton.pack()

        self.__viewLeftButton = tk.Button(self.__mapViewKeypadFrame, text="Left", command= lambda:self.__moveView("Left"))
        self.__viewLeftButton.pack()

        self.__viewRightButton = tk.Button(self.__mapViewKeypadFrame, text="Right", command= lambda:self.__moveView("Right"))
        self.__viewRightButton.pack()

        self.__viewRightButton = tk.Button(self.__mapViewKeypadFrame, text="Confirm placement", command= self.__confirmPlacement)
        self.__viewRightButton.pack()

        self.__minimapButton = tk.Button(self.__mapViewKeypadFrame, text = "Minimap", command=self.__openMinimap)
        self.__minimapButton.pack()

        #main game grid frame
        self.__mainGameFrame = tk.Frame(self.__mainFrame)
        self.__mainGameFrame.pack(side="right")

        self.__tileGridFrame = tk.Frame(self.__mainGameFrame,highlightbackground="black",highlightthickness=1)
        self.__tileGridFrame.pack(side ="top")

        #offset used to translate user game grid to coords
        #//2 puts starting tile into centre
        self.__tileGridCanvasList = []
        self.__coordOffsetX = TILE_GRID_X//2
        self.__coordOffsetY = TILE_GRID_Y//2

        self.__generateTileGridCanvas()
        self.__updateDisplay()
        self.__redrawBoard()

    def __openMinimap(self):
        board = self.__game.getBoard()
        minimapWindow(self.__mainFrame.winfo_toplevel(),board)

    def __confirmPlacement(self):
        if not self.__game.completeTurn():
            self.__updateDisplay()
            self.__redrawBoard()
    
    def __updateDisplay(self):
        #reloads ui
        self.__updateScores()
        self.__tileRemainingLable.config(text="Tiles remaining: " + str(self.__game.getTilesRemaining()))
        self.__game.drawTile(self.__tileCanvas,True)
        self.__turnCountLable.config(text="Turn number: " +str(self.__game.getTurnCount()))
        self.__turnPlayerLable.config(text="Turn player: " + str(self.__game.getTurnPlayerName()))
        self.__MeepleCountLable.config(text="Meeples remaining: " + str(self.__game.getTurnPlayerMeeplesRemaining()))

    def __moveView(self, direction):
        if direction == "Up":
            self.__coordOffsetY += 1
        if direction == "Down":
            self.__coordOffsetY -= 1
        if direction == "Left":
            self.__coordOffsetX += 1
        if direction == "Right":
            self.__coordOffsetX -= 1
        self.__redrawBoard()

    def __generateTileGridCanvas(self):
        #grid stored as 2D array
        for i in range(TILE_GRID_X):
            self.__tileGridCanvasList.append([])
            for j in range(TILE_GRID_Y):
                self.__tileGridCanvasList[i].append(tk.Canvas(self.__tileGridFrame, width=TILE_SIZE, height=TILE_SIZE,highlightthickness=1, highlightbackground="black"))

        for i in range(len(self.__tileGridCanvasList)):
            for j in range(len(self.__tileGridCanvasList[i])):
                self.__tileGridCanvasList[i][j].grid(row=j,column=i)
                self.__tileGridCanvasList[i][j].bind("<Button-1>", lambda event, i=i, j=j: self.__placeTempTile(self.__tileGridCanvasList[i][j],(i - self.__coordOffsetX, j - self.__coordOffsetY)))

        #places start tile
        self.__game.setupBoard(self.__tileGridCanvasList[TILE_GRID_X//2][TILE_GRID_Y//2])

    def __placeTempTile(self, canvas, coord):
        self.__redrawBoard()
        self.__game.placeTempTile(canvas,coord)

    def __redrawBoard(self):
        #clears and reloads tiles in tile grid
        board = self.__game.getBoard()

        #tile clears
        for i in range(len(self.__tileGridCanvasList)):
            for j in range(len(self.__tileGridCanvasList[i])):
                self.__tileGridCanvasList[i][j].delete("all")

        tileCoordList = list(board.keys())

        #redraws tile that are within the grid to avoid index out of range errors
        for coord in tileCoordList:
            if coord[0]+self.__coordOffsetX < len(self.__tileGridCanvasList) and coord[0]+self.__coordOffsetX >=0:
                if coord[1]+self.__coordOffsetY < len(self.__tileGridCanvasList[coord[0]+self.__coordOffsetX]) and coord[1]+self.__coordOffsetY >=0:
                    self.__game.tileRedraw(self.__tileGridCanvasList[coord[0]+self.__coordOffsetX][coord[1]+self.__coordOffsetY],board[coord])

    def __placeMeeple(self,cursorX,cursorY):
        #preview tile canvas
        self.__tileCanvas.update()
        width = self.__tileCanvas.winfo_width()
        height = self.__tileCanvas.winfo_height()

        #locates cursor position on click and determines which side the user clicks on
        if cursorX >= width/16*7 and cursorX <= width/16*9 and cursorY <= height/16*3 and cursorY >= height/16:
            self.__game.claimFeature("North")

        elif cursorX >= width/16*7 and cursorX <= width/16*9 and cursorY <= height/16*15 and cursorY >= height/16*13:
            self.__game.claimFeature("South")

        elif cursorX >= width/16*13 and cursorX <= width/16*15 and cursorY <= height/16*9 and cursorY >= height/16*7:
            self.__game.claimFeature("East")

        elif cursorX >= width/16 and cursorX <= width/16*3 and cursorY <= height/16*9 and cursorY >= height/16*7:
            self.__game.claimFeature("West")

        elif cursorX >= width/16*7 and cursorX <= width/16*9 and cursorY <= height/16*9 and cursorY >= height/16*7:
            self.__game.claimFeature("Centre")

        self.__game.drawTile(self.__tileCanvas,True)

    def __updateScores(self):
        #playerScoreDict is dictionary, keys is player names, values are player scores
        playerScoreDict = self.__game.getPlayerLeaderboard()
        playerNames = list(playerScoreDict.keys())

        #bubble sort to sort playerNames list into order based on scores
        #includes optimisations to stop if no swaps
        #bubble sort used as number of items needed to be sorted is small
        for i in range(len(playerNames)):
            swaps = False
            for j in range(len(playerNames)-i-1):
                if playerScoreDict[playerNames[j]]<playerScoreDict[playerNames[j+1]]:
                    playerNames[j],playerNames[j+1]=playerNames[j+1],playerNames[j]
                    swaps = True      
            if not swaps:
                break

        #updates player scoreboard using loop to reduce code
        for i in range(len(playerNames)):
            self.__scoreLableList[i].config(text=str(i+1)+". "+playerNames[i]+" : "+str(playerScoreDict[playerNames[i]]))

    def saveGame(self):
        self.__game.updateGameFile()

    def __gameOver(self):
        playerScoreDict = self.__game.getPlayerLeaderboard()

        #removes tk children to prepare for next window
        for widget in self.__mainFrame.winfo_children():
            widget.destroy()

        self.__leaderBoardFunc(playerScoreDict)

