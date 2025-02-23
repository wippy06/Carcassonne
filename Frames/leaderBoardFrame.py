import tkinter as tk
from constants import BUTTON_DEFAULT_COLOUR, TEXT_FONT,FRAME_BG_DEFAULT_COLOUR

class leaderBoardFrame:
    def __init__(self, window, frame, playerList,startFunc):

        mainFrame = tk.Frame(frame,bg=FRAME_BG_DEFAULT_COLOUR)
        mainFrame.place(relx=0.5,rely=0.4,anchor="center")
        self.__window = window
        self.__startFunc = startFunc
        self.__playerList = playerList

        self.__winnerLable = tk.Label(mainFrame, text="Winner: ",borderwidth=3, relief="solid",font=(TEXT_FONT,60),padx=20,pady=20)
        self.__winnerLable.pack(side = "top",padx=10,pady=50)

        leaderBoardListFrame = tk.Frame(mainFrame,bg=FRAME_BG_DEFAULT_COLOUR)
        leaderBoardListFrame.pack(side = "top",pady=20)

        self.__scoreLableList = []
        for i in range(len(self.__playerList)):
            self.__scoreLableList.append(tk.Label(leaderBoardListFrame,bg=FRAME_BG_DEFAULT_COLOUR, font=(TEXT_FONT,13), text=str(i+1)+". "))
            self.__scoreLableList[i].pack(side = "top",padx=10,pady=10)

        self.__displayScores()

        buttonFrame = tk.Frame(mainFrame,bg=FRAME_BG_DEFAULT_COLOUR)
        buttonFrame.pack(side="top",pady=20)

        tk.Button(buttonFrame, text="Return",font=(TEXT_FONT,20), width=6,command=lambda:self.__return(frame), bg = BUTTON_DEFAULT_COLOUR).pack(side="left",padx=10,pady=10)
        tk.Button(buttonFrame, text = "Exit",font=(TEXT_FONT,20), width=6,command = self.__window.destroy, bg = BUTTON_DEFAULT_COLOUR).pack(side="right",padx=10,pady=10)

    def __return(self,frame):
        #removes tk children to prepare for next frame
        for widget in frame.winfo_children():
            widget.destroy()
        self.__startFunc()
        

    def __displayScores(self):
        #playerList is presorted     

        #updates player scoreboard using loop to reduce code
        for i in range(len(self.__playerList)):
            self.__scoreLableList[i].config(text=str(i+1)+". "+self.__playerList[i].getName()+" : "+self.__playerList[i].getColour()+" : "+str(self.__playerList[i].getScore()))
            
        self.__winnerLable.config(text="Winner: "+self.__playerList[0].getName())
