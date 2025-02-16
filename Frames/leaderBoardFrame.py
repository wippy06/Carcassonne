import tkinter as tk
from constants import BUTTON_DEFAULT_COLOUR, TEXT_FONT,FRAME_BG_DEFAULT_COLOUR

class leaderBoardFrame:
    def __init__(self, window, frame, playerScoreDict,startFunc):

        self.__mainFrame = tk.Frame(frame,bg=FRAME_BG_DEFAULT_COLOUR)
        self.__mainFrame.place(relx=0.5,rely=0.4,anchor="center")
        self.__window = window
        self.__startFunc = startFunc
        self.__playerScoreDict = playerScoreDict

        self.__winnerLable = tk.Label(self.__mainFrame, text="Winner: ",borderwidth=3, relief="solid",font=(TEXT_FONT,60),padx=20,pady=20)
        self.__winnerLable.pack(side = "top",padx=10,pady=50)

        self.__leaderBoardListFrame = tk.Frame(self.__mainFrame,bg=FRAME_BG_DEFAULT_COLOUR)
        self.__leaderBoardListFrame.pack(side = "top",pady=20)

        self.__scoreLableList = []
        for i in range(len(self.__playerScoreDict.keys())):
            self.__scoreLableList.append(tk.Label(self.__leaderBoardListFrame,bg=FRAME_BG_DEFAULT_COLOUR, font=(TEXT_FONT,13), text=str(i+1)+". "))
            self.__scoreLableList[i].pack(side = "top",padx=10,pady=10)

        self.__displayScores()

        self.__buttonFrame = tk.Frame(self.__mainFrame,bg=FRAME_BG_DEFAULT_COLOUR)
        self.__buttonFrame.pack(side="top",pady=20)

        tk.Button(self.__buttonFrame, text="Return",font=(TEXT_FONT,20), width=6,command=lambda:self.__return(frame), bg = BUTTON_DEFAULT_COLOUR).pack(side="left",padx=10,pady=10)
        tk.Button(self.__buttonFrame, text = "Exit",font=(TEXT_FONT,20), width=6,command = self.__window.destroy, bg = BUTTON_DEFAULT_COLOUR).pack(side="right",padx=10,pady=10)

    def __return(self,frame):
        #removes tk children to prepare for next frame
        for widget in frame.winfo_children():
            widget.destroy()
        self.__startFunc()
        

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

        self.__winnerLable.config(text="Winner: "+playerNames[i])

        #updates player scoreboard using loop to reduce code
        for i in range(len(playerNames)):
            self.__scoreLableList[i].config(text=str(i+1)+". "+playerNames[i]+" : "+self.__playerScoreDict[playerNames[i]][1]+" : "+str(self.__playerScoreDict[playerNames[i]][0]))

