import tkinter as tk

class leaderBoardFrame:
    def __init__(self, window, frame, playerScoreDict,startFunc):

        self.__mainFrame = tk.Frame(frame)
        self.__mainFrame.pack()
        self.__window = window
        self.__startFunc = startFunc
        self.__playerScoreDict = playerScoreDict

        self.__leaderBoardListFrame = tk.Frame(self.__mainFrame)
        self.__leaderBoardListFrame.pack(side = "top")

        self.__scoreLableList = []
        for i in range(len(self.__playerScoreDict.keys())):
            self.__scoreLableList.append(tk.Label(self.__leaderBoardListFrame, text=str(i+1)+". "))
            self.__scoreLableList[i].pack(side = "top")

        self.__displayScores()

        self.__buttonFrame = tk.Frame(self.__mainFrame)
        self.__buttonFrame.pack(side="top")

        tk.Button(self.__buttonFrame, text="Play again", command=self.__startFunc).pack(side="left")
        tk.Button(self.__buttonFrame, text = "Exit", command = self.__window.destroy).pack(side="right")

    def __displayScores(self):
        playerNames = list(self.__playerScoreDict.keys())

        #bubble sort to sort playerNames list into order based on scores
        #includes optimisations to stop if no swaps
        #bubble sort used as number of items needed to be sorted is small
        for i in range(len(playerNames)):
            swaps = False
            for j in range(len(playerNames)-i-1):
                if self.__playerScoreDict[playerNames[j]]<self.__playerScoreDict[playerNames[j+1]]:
                    playerNames[j],playerNames[j+1]=playerNames[j+1],playerNames[j]
                    swaps = True      
            if not swaps:
                break

        #updates player scoreboard using loop to reduce code
        for i in range(len(playerNames)):
            self.__scoreLableList[i].config(text=str(i+1)+". "+playerNames[i]+" : "+str(self.__playerScoreDict[playerNames[i]]))

