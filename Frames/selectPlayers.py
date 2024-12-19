import tkinter as tk
from constants import BGDEFAULTCOLOUR

class selectPlayers:
    def __init__(self, frame, gameSlot, gameFunc):
        self.__frame = frame
        self.__gameSlot = gameSlot
        self.__gameFile = open("gameSlots/slot"+str(self.__gameSlot)+".ccsn", "r+")
        self.__gameFunc = gameFunc

        self.__playerFrame = tk.Frame(frame)
        self.__playerFrame.pack()

        self.__topLFrame = tk.Frame(self.__playerFrame)
        self.__topLFrame.grid(column=0,row=0)

        self.__topMFrame = tk.Frame(self.__playerFrame)
        self.__topMFrame.grid(column=0,row=1)

        self.__topRFrame = tk.Frame(self.__playerFrame)
        self.__topRFrame.grid(column=0,row=2)

        self.__bottomLFrame = tk.Frame(self.__playerFrame)
        self.__bottomLFrame.grid(column=1,row=0)

        self.__bottomMFrame = tk.Frame(self.__playerFrame)
        self.__bottomMFrame.grid(column=1,row=1)

        self.__bottomRFrame = tk.Frame(self.__playerFrame)
        self.__bottomRFrame.grid(column=1,row=2)

        self.__player1 = playerSelectBox(self.__topLFrame, self.__changeOrderButtons)
        self.__player2 = playerSelectBox(self.__topMFrame, self.__changeOrderButtons)
        self.__player3 = playerSelectBox(self.__topRFrame, self.__changeOrderButtons)
        self.__player4 = playerSelectBox(self.__bottomLFrame, self.__changeOrderButtons)
        self.__player5 = playerSelectBox(self.__bottomMFrame, self.__changeOrderButtons)
        self.__player6 = playerSelectBox(self.__bottomRFrame, self.__changeOrderButtons)
        
        self.__playerList = [self.__player1, self.__player2, self.__player3, self.__player4, self.__player5, self.__player6]

        self.__takenOrderList = []

        tk.Button(self.__frame, text = "Continue", command = lambda: self.__confirmChoice()).pack()

    def __changeOrderButtons(self, numberNew, numberOld):
        if numberOld != 0:
            self.__takenOrderList.remove(numberOld)
        self.__takenOrderList.append(numberNew)
        
        for player in self.__playerList:
            player.deactivateOrderBs(self.__takenOrderList)
    
    def __confirmChoice(self):
        for widget in self.__frame.winfo_children():
            widget.destroy()
        self.__gameFunc(self.__gameSlot)

class playerSelectBox:
    def __init__(self, frame, changeOrderButtons):
        self.__frame = frame
        self.__name = ""
        self.__type = "player"
        self.__order = 0
        self.__orderChanged = changeOrderButtons
        self.__orderBList = []
        self.__deletePlayer()

    def __newPlayer(self):
        for widget in self.__frame.winfo_children():
            widget.destroy()

        tk.Label(self.__frame, text = "Name: ").pack()
        self.__name = tk.Entry(self.__frame)
        self.__name.pack()

        tk.Label(self.__frame, text = "Type: ").pack()
        self.__typeButton = tk.Button(self.__frame, text = self.__type, command = self.__typeChange)
        self.__typeButton.pack()

        tk.Label(self.__frame, text = "Order: ").pack()

        self.__orderFrame = tk.Frame(self.__frame)
        self.__orderFrame.pack()

        self.__orderB1 = tk.Button(self.__orderFrame, text = "1", command = lambda: self.__selectOrder(1))
        self.__orderB2 = tk.Button(self.__orderFrame, text = "2", command = lambda: self.__selectOrder(2))
        self.__orderB3 = tk.Button(self.__orderFrame, text = "3", command = lambda: self.__selectOrder(3))
        self.__orderB4 = tk.Button(self.__orderFrame, text = "4", command = lambda: self.__selectOrder(4))
        self.__orderB5 = tk.Button(self.__orderFrame, text = "5", command = lambda: self.__selectOrder(5))
        self.__orderB6 = tk.Button(self.__orderFrame, text = "6", command = lambda: self.__selectOrder(6))

        self.__orderBList = [self.__orderB1, self.__orderB2, self.__orderB3, self.__orderB4, self.__orderB5, self.__orderB6,]

        for i in range(len(self.__orderBList)):
            self.__orderBList[i].grid(column=i, row=0)

        tk.Button(self.__frame, text = "Delete", command = lambda: self.__deletePlayer()).pack()

    def __typeChange(self):
        if self.__type == "player":
            self.__type = "bot"
        else:
            self.__type = "player"

        self.__typeButton.config(text = self.__type)

    def __selectOrder(self, number):
        for i in range(len(self.__orderBList)):
            if i == number-1:
                self.__orderBList[i].config(bg = "black", fg = BGDEFAULTCOLOUR)
            else:
                self.__orderBList[i].config(bg = BGDEFAULTCOLOUR, fg = "black")

        self.__orderChanged(number, self.__order)
        self.__order = number

    def deactivateOrderBs(self, takenList):
        if self.__orderBList != []:
            for i in range(len(self.__orderBList)):
                if i+1 in takenList:
                    self.__orderBList[i].config(state="disabled")
                else:
                    self.__orderBList[i].config(state="normal")


    def __deletePlayer(self):
        for widget in self.__frame.winfo_children():
            widget.destroy()
        tk.Button(self.__frame, text = "New Player", command = lambda: self.__newPlayer()).pack()