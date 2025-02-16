import tkinter as tk
from game.game import game
from frames.minimapWindow import minimapWindow
from constants import TILE_SIZE, TILE_GRID_X,TILE_GRID_Y,CONTROLS,BUTTON_DEFAULT_COLOUR,EMPTY_COLOUR,TEXT_FONT,FRAME_BG_DEFAULT_COLOUR

class gameFrame:
    def __init__(self,frame, gameFile, leaderBoardFunc):
        #init game object, gameFrame handles user interface, game obj handles game operations
        self.__game = game(gameFile,self.__gameOver)
        self.__leaderBoardFunc = leaderBoardFunc
        self.__mainFrame = frame

        #creating frames
        self.__leftSideBarFrame = tk.Frame(self.__mainFrame)
        self.__leftSideBarFrame.pack(side="left",expand=True,fill="both")

        self.__scoreFrame = tk.Frame(self.__leftSideBarFrame,highlightbackground="black",highlightthickness=1,bg=FRAME_BG_DEFAULT_COLOUR)
        self.__scoreFrame.pack(side="top",expand=True,fill="both")

        #done as list to reduce code
        self.__scoreLableList = []
        for i in range(self.__game.getNumPlayers()):
            self.__scoreLableList.append(tk.Label(self.__scoreFrame, text=str(i+1)+". ",font=(TEXT_FONT,13),bg=FRAME_BG_DEFAULT_COLOUR))
            self.__scoreLableList[i].pack(anchor = "nw",padx=5,pady=5)

        #tile preview frame
        self.__tilePreviewFrame = tk.Frame(self.__leftSideBarFrame,highlightbackground="black",highlightthickness=1,bg=FRAME_BG_DEFAULT_COLOUR)
        self.__tilePreviewFrame.pack(side="top",expand=True,fill="both")

        self.__tileCanvas = tk.Canvas(self.__tilePreviewFrame, width=200, height=200)
        self.__tileCanvas.pack(side = "top",padx=10,pady=15)
        self.__tileCanvas.bind("<Button-1>",lambda event:self.__placeMeeple(event.x,event.y))

        self.__rotateButtonFrame = tk.Frame(self.__tilePreviewFrame,bg=FRAME_BG_DEFAULT_COLOUR)
        self.__rotateButtonFrame.pack()
        
        self.__tileRotateClock = tk.Button(self.__rotateButtonFrame, text = "⟳",font=(TEXT_FONT,13), command = lambda:self.__game.rotatePreview(False, self.__tileCanvas), bg = BUTTON_DEFAULT_COLOUR)
        self.__tileRotateAntiClock = tk.Button(self.__rotateButtonFrame, text = "⟲",font=(TEXT_FONT,13), command = lambda:self.__game.rotatePreview(True, self.__tileCanvas), bg = BUTTON_DEFAULT_COLOUR)
        self.__tileRotateClock.pack(side="right",padx=5,pady=5)
        self.__tileRotateAntiClock.pack(side="left",padx=5,pady=5)

        self.__confirmPlacementButton = tk.Button(self.__tilePreviewFrame, text="Confirm placement",font=(TEXT_FONT,13), command= self.__confirmPlacement, bg = BUTTON_DEFAULT_COLOUR)
        self.__confirmPlacementButton.pack(pady=5)

        #extra info frame
        self.__extraInfoFrame = tk.Frame(self.__leftSideBarFrame,highlightbackground="black",highlightthickness=1,bg=FRAME_BG_DEFAULT_COLOUR)
        self.__extraInfoFrame.pack(side="top",expand=True,fill="both")

        self.__turnCountLable = tk.Label(self.__extraInfoFrame,font=(TEXT_FONT,13),text = "Turn number: ",bg=FRAME_BG_DEFAULT_COLOUR)
        self.__turnPlayerLable = tk.Label(self.__extraInfoFrame,font=(TEXT_FONT,13), text="Turn player: ",bg=FRAME_BG_DEFAULT_COLOUR)
        self.__MeepleCountLable = tk.Label(self.__extraInfoFrame,font=(TEXT_FONT,13),text="Meeples remaining: ",bg=FRAME_BG_DEFAULT_COLOUR)
        self.__tileRemainingLable = tk.Label(self.__tilePreviewFrame,font=(TEXT_FONT,13), text = "Tiles remaining: ",bg=FRAME_BG_DEFAULT_COLOUR)

        self.__turnCountLable.pack(pady=5)
        self.__turnPlayerLable.pack(pady=5)
        self.__MeepleCountLable.pack(pady=5)
        self.__tileRemainingLable.pack(pady=5)

        #map movement frame
        self.__mapViewKeypadFrame = tk.Frame(self.__leftSideBarFrame,highlightbackground="black",highlightthickness=1,bg=FRAME_BG_DEFAULT_COLOUR)
        self.__mapViewKeypadFrame.pack(side="top",expand=True,fill="both")

        self.__keyPadFrame = tk.Frame(self.__mapViewKeypadFrame,bg=FRAME_BG_DEFAULT_COLOUR)
        self.__keyPadFrame.pack(pady=5)

        #used to get buttons to be square
        self.__pixel = tk.PhotoImage(width=1, height=1)

        self.__viewUpButton = tk.Button(self.__keyPadFrame,width=25,height=25,image=self.__pixel, compound='c', text="↑",font=(TEXT_FONT,13), command= lambda:self.__moveView("Up"), bg = BUTTON_DEFAULT_COLOUR)
        self.__viewUpButton.grid(row=0,column=1)

        self.__viewDownButton = tk.Button(self.__keyPadFrame,width=25,height=25,image=self.__pixel, compound='c', text="↓",font=(TEXT_FONT,13), command= lambda:self.__moveView("Down"), bg = BUTTON_DEFAULT_COLOUR)
        self.__viewDownButton.grid(row=2,column=1)

        self.__viewLeftButton = tk.Button(self.__keyPadFrame,width=25,height=25,image=self.__pixel, compound='c', text="←",font=(TEXT_FONT,13), command= lambda:self.__moveView("Left"), bg = BUTTON_DEFAULT_COLOUR)
        self.__viewLeftButton.grid(row=1,column=0)

        self.__viewRightButton = tk.Button(self.__keyPadFrame,width=25,height=25,image=self.__pixel, compound='c', text="→",font=(TEXT_FONT,13), command= lambda:self.__moveView("Right"), bg = BUTTON_DEFAULT_COLOUR)
        self.__viewRightButton.grid(row=1,column=2)

        self.__viewHomeButton = tk.Button(self.__keyPadFrame,width=25,height=25,image=self.__pixel, compound='c', text="🏠",font=(TEXT_FONT,13), command= lambda:self.__moveView("Home"), bg = BUTTON_DEFAULT_COLOUR)
        self.__viewHomeButton.grid(row=1,column=1)

        self.__minimapButton = tk.Button(self.__mapViewKeypadFrame, text = "Minimap",font=(TEXT_FONT,13), command=self.__openMinimap, bg = BUTTON_DEFAULT_COLOUR)
        self.__minimapButton.pack(pady=5)

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

        #bind key binds for effective gameplay
        self.__window = self.__mainFrame.winfo_toplevel()
        self.__window.bind(CONTROLS[0], lambda event : self.__moveView("Up"))
        self.__window.bind(CONTROLS[1], lambda event : self.__moveView("Down"))
        self.__window.bind(CONTROLS[2], lambda event : self.__moveView("Left"))
        self.__window.bind(CONTROLS[3], lambda event : self.__moveView("Right"))
        self.__window.bind(CONTROLS[4], lambda event : self.__moveView("Home"))
        self.__window.bind(CONTROLS[5], lambda event : self.__game.rotatePreview(False, self.__tileCanvas))
        self.__window.bind(CONTROLS[6], lambda event : self.__game.rotatePreview(True, self.__tileCanvas))
        self.__window.bind(CONTROLS[7], lambda event : self.__confirmPlacement())
        self.__window.bind(CONTROLS[8], lambda event :(self.__game.claimFeature("North"),self.__game.drawTile(self.__tileCanvas,True)))
        self.__window.bind(CONTROLS[9], lambda event :(self.__game.claimFeature("East"),self.__game.drawTile(self.__tileCanvas,True)))
        self.__window.bind(CONTROLS[10],lambda event :(self.__game.claimFeature("South"),self.__game.drawTile(self.__tileCanvas,True)))
        self.__window.bind(CONTROLS[11],lambda event :(self.__game.claimFeature("West"),self.__game.drawTile(self.__tileCanvas,True)))
        self.__window.bind(CONTROLS[12],lambda event :(self.__game.claimFeature("Centre"),self.__game.drawTile(self.__tileCanvas,True)))
        self.__window.bind(CONTROLS[13],lambda event :(self.__game.claimFeature("Remove"),self.__game.drawTile(self.__tileCanvas,True)))
        self.__window.bind(CONTROLS[14],lambda event : self.__openMinimap())

        self.__generateTileGridCanvas()
        self.__reloadFrame()

    def __openMinimap(self):
        board = self.__game.getBoard()
        minimapWindow(self.__window,board)

    def __reloadFrame(self):
        if not self.__game.checkGameEnd():
            self.__updateDisplay()
        else:
            self.__gameOver()

    def __confirmPlacement(self):
        self.__game.completeTurn(self.__reloadFrame)
    
    def __updateDisplay(self):
        #reloads ui
        self.__updateScores()
        self.__tileRemainingLable.config(text="Tiles remaining: " + str(self.__game.getTilesRemaining()))
        self.__game.drawTile(self.__tileCanvas,True)
        self.__turnCountLable.config(text="Turn number: " +str(self.__game.getTurnCount()))
        self.__turnPlayerLable.config(text="Turn player: " + str(self.__game.getTurnPlayerName()))
        self.__MeepleCountLable.config(text="Meeples remaining: " + str(self.__game.getTurnPlayerMeeplesRemaining()))
        self.__redrawBoard()

    def __moveView(self, direction):
        if direction == "Up":
            self.__coordOffsetY += 1
        if direction == "Down":
            self.__coordOffsetY -= 1
        if direction == "Left":
            self.__coordOffsetX += 1
        if direction == "Right":
            self.__coordOffsetX -= 1
        if direction == "Home":
            self.__coordOffsetX = TILE_GRID_X//2
            self.__coordOffsetY = TILE_GRID_Y//2
        self.__redrawBoard()

    def __generateTileGridCanvas(self):
        #grid stored as 2D array
        for i in range(TILE_GRID_X):
            self.__tileGridCanvasList.append([])
            for j in range(TILE_GRID_Y):
                self.__tileGridCanvasList[i].append(tk.Canvas(self.__tileGridFrame, width=TILE_SIZE, height=TILE_SIZE,highlightthickness=1, highlightbackground="black",bg=EMPTY_COLOUR))

        for i in range(len(self.__tileGridCanvasList)):
            for j in range(len(self.__tileGridCanvasList[i])):
                self.__tileGridCanvasList[i][j].grid(row=j,column=i)
                self.__tileGridCanvasList[i][j].bind("<Button-1>", lambda event, i=i, j=j: self.__placeTempTile(self.__tileGridCanvasList[i][j],(i - self.__coordOffsetX, j - self.__coordOffsetY)))

        #places start tile
        self.__game.setupBoard(self.__tileGridCanvasList[TILE_GRID_X//2][TILE_GRID_Y//2],self.__reloadFrame)

    def __placeTempTile(self, canvas, coord):
        if self.__game.checkIfRemoveTempTile(coord):
            self.__game.placeTempTile(canvas,(0,0))
        else:
            self.__game.placeTempTile(canvas,coord)
        self.__redrawBoard()

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

        currentCoord = self.__game.getCurrentCoord()
        if currentCoord != None:
            if currentCoord[0]+self.__coordOffsetX < len(self.__tileGridCanvasList) and currentCoord[0]+self.__coordOffsetX >=0:
                if currentCoord[1]+self.__coordOffsetY < len(self.__tileGridCanvasList[currentCoord[0]+self.__coordOffsetX]) and currentCoord[1]+self.__coordOffsetY >=0:
                    self.__game.redrawTempTile(self.__tileGridCanvasList[currentCoord[0]+self.__coordOffsetX][currentCoord[1]+self.__coordOffsetY])

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
        #playerScoreDict is dictionary, keys is player names, values are [player scores,player colour]
        playerScoreDict = self.__game.getPlayerLeaderboard()
        playerNames = list(playerScoreDict.keys())

        #bubble sort to sort playerNames list into order based on scores then alphabetically
        #includes optimisations to stop if no swaps
        #bubble sort used as number of items needed to be sorted is small
        for i in range(len(playerNames)):
            swaps = False
            for j in range(len(playerNames)-i-1):
                if playerScoreDict[playerNames[j]][0]<playerScoreDict[playerNames[j+1]][0]:
                    playerNames[j],playerNames[j+1]=playerNames[j+1],playerNames[j]
                    swaps = True

                #sort alphabetically if scores are the same
                elif playerScoreDict[playerNames[j]][0]==playerScoreDict[playerNames[j+1]][0]:
                    if playerNames[j]>playerNames[j+1]:
                        playerNames[j],playerNames[j+1]=playerNames[j+1],playerNames[j]
                        swaps = True
            if not swaps:
                break

        #updates player scoreboard using loop to reduce code
        for i in range(len(playerNames)):
            self.__scoreLableList[i].config(text=str(i+1)+". "+playerNames[i]+" : "+playerScoreDict[playerNames[i]][1]+" : "+str(playerScoreDict[playerNames[i]][0]))

    def saveGame(self):
        self.__game.updateGameFile()

    def __gameOver(self):
        playerScoreDict = self.__game.getPlayerLeaderboard()

        #removes tk children to prepare for next frame
        for widget in self.__mainFrame.winfo_children():
            widget.destroy()

        for binding in CONTROLS:
            self.__mainFrame.winfo_toplevel().unbind(binding)

        self.__leaderBoardFunc(playerScoreDict)