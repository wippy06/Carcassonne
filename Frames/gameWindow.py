import tkinter as tk
from game.game import game
from constants import TILE_SIZE

class gameWindow:
    def __init__(self,frame, gameFile):
        self.__game = game(gameFile)

        self.__leftSideBarFrame = tk.Frame(frame)
        self.__leftSideBarFrame.pack(side="left")

        self.__scoreFrame = tk.Frame(self.__leftSideBarFrame,highlightbackground="black",highlightthickness=1)
        self.__scoreFrame.grid(column=0, row=0)

        self.__score1 = tk.Label(self.__scoreFrame, text="1. ")
        self.__score2 = tk.Label(self.__scoreFrame, text="2. ")
        self.__score3 = tk.Label(self.__scoreFrame, text="3. ")
        self.__score4 = tk.Label(self.__scoreFrame, text="4. ")
        self.__score5 = tk.Label(self.__scoreFrame, text="5. ")
        self.__score6 = tk.Label(self.__scoreFrame, text="6. ")

        self.__scoreLableList = [self.__score1,self.__score2,self.__score3,self.__score4,self.__score5,self.__score6]
        self.__packScoreLables()

        self.__tilePreviewFrame = tk.Frame(self.__leftSideBarFrame,highlightbackground="black",highlightthickness=1)
        self.__tilePreviewFrame.grid(column=0, row=1)

        self.__tileCanvas = tk.Canvas(self.__tilePreviewFrame, width=TILE_SIZE, height=TILE_SIZE, bg='green')
        self.__tileCanvas.pack(side = "top")

        self.__rotateButtonFrame = tk.Frame(self.__tilePreviewFrame)
        self.__rotateButtonFrame.pack()
        
        self.__tileRotateClock = tk.Button(self.__rotateButtonFrame, text = "clockwise", command = lambda:self.__game.rotatePreview(False, self.__tileCanvas))
        self.__tileRotateAntiClock = tk.Button(self.__rotateButtonFrame, text = "anticlockwise", command = lambda:self.__game.rotatePreview(True, self.__tileCanvas))
        self.__tileRotateClock.pack(side="left")
        self.__tileRotateAntiClock.pack(side="right")

        self.__tileRemainingLable = tk.Label(self.__tilePreviewFrame, text = "Tiles remaining: ")
        self.__tileRemainingLable.pack()

        self.__extraInfoFrame = tk.Frame(self.__leftSideBarFrame,highlightbackground="black",highlightthickness=1)
        self.__extraInfoFrame.grid(column=0, row=2)

        self.__turnCountLable = tk.Label(self.__extraInfoFrame,text = "Turn number: ")
        self.__turnPlayerLable = tk.Label(self.__extraInfoFrame, text="Turn player: ")
        self.__MeepleCountLable = tk.Label(self.__extraInfoFrame,text="Meeples remaining: ")

        self.__turnCountLable.pack()
        self.__turnPlayerLable.pack()
        self.__MeepleCountLable.pack()

        self.__mainGameFrame = tk.Frame(frame)
        self.__mainGameFrame.pack(side="right")

        self.__updateDisplay()

    def __updateDisplay(self):
        self.__updateScores()
        self.__tileRemainingLable.config(text="Tiles remaining: " + str(self.__game.getTilesRemaining()))
        self.__game.drawTilePreview(self.__tileCanvas)
        self.__turnCountLable.config(text="Turn number: " +str(self.__game.getTurnCount()))
        self.__turnPlayerLable.config(text="Turn player: " + str(self.__game.getTurnPlayerName()))
        self.__MeepleCountLable.config(text="Meeples remaining: " + str(self.__game.getTurnPlayerMeeplesRemaining()))


    def __packScoreLables(self):
        for i in range(self.__game.getNumPlayers()):
            self.__scoreLableList[i].pack(side="top")

    def __updateScores(self):
        playerScoreDict = self.__game.getPlayerLeaderboard()
        playerNames = list(playerScoreDict.keys())

        for i in range(len(playerNames)):
            swaps = False
            for j in range(len(playerNames)-i-1):
                if playerScoreDict[playerNames[j]]>playerScoreDict[playerNames[j+1]]:
                    playerNames[j],playerNames[j+1]=playerNames[j+1],playerNames[j]
                    swaps = True      
            if not swaps:
                break

        for i in range(len(playerNames)):
            self.__scoreLableList[i].config(text=str(i+1)+". "+playerNames[i]+" : "+str(playerScoreDict[playerNames[i]]))

