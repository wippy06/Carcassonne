import tkinter as tk
from constants import BG_DEFAULT_COLOUR


class playerSelectBox:
    def __init__(self, frame, changeOrderButtons):
        self.__frame = frame
        self.__type = "player"
        self.__order = 0
        self.__isPlaying = False

        #not in use
        #self.__orderChanged = changeOrderButtons

        self.__orderBList = []
        self.__deletePlayer()

    def __newPlayer(self):
        #set for player count conditions in selectPlayers class
        self.__isPlaying = True
        
        #remove new player button and replace with player options
        for widget in self.__frame.winfo_children():
            widget.destroy()

        tk.Label(self.__frame, text = "Name: ").pack()
        self.__nameEntry = tk.Entry(self.__frame)
        self.__nameEntry.pack()

        #types can be bot or player
        tk.Label(self.__frame, text = "Type: ").pack()
        self.__typeButton = tk.Button(self.__frame, text = self.__type, command = self.__typeChange)
        self.__typeButton.pack()

        tk.Label(self.__frame, text = "Order: ").pack()

        self.__orderFrame = tk.Frame(self.__frame)
        self.__orderFrame.pack()

        #not done as for loop for ease of access, buttons stored in button list to be indexed
        self.__orderB1 = tk.Button(self.__orderFrame, text = "1", command = lambda: self.__selectOrder(1))
        self.__orderB2 = tk.Button(self.__orderFrame, text = "2", command = lambda: self.__selectOrder(2))
        self.__orderB3 = tk.Button(self.__orderFrame, text = "3", command = lambda: self.__selectOrder(3))
        self.__orderB4 = tk.Button(self.__orderFrame, text = "4", command = lambda: self.__selectOrder(4))
        self.__orderB5 = tk.Button(self.__orderFrame, text = "5", command = lambda: self.__selectOrder(5))
        self.__orderB6 = tk.Button(self.__orderFrame, text = "6", command = lambda: self.__selectOrder(6))

        self.__orderBList = [self.__orderB1, self.__orderB2, self.__orderB3, self.__orderB4, self.__orderB5, self.__orderB6,]

        #gridded as for loop to make ui easy to interperate
        for i in range(len(self.__orderBList)):
            self.__orderBList[i].grid(column=i, row=0)

        tk.Button(self.__frame, text = "Delete", command = lambda: self.__deletePlayer()).pack()

    def __typeChange(self):
        #self.__type not a bool even though only 2 states incase of additions in the future
        if self.__type == "player":
            self.__type = "bot"
        else:
            self.__type = "player"

        self.__typeButton.config(text = self.__type)

    def __selectOrder(self, number):
        for i in range(len(self.__orderBList)):
            if i == number-1:
                self.__orderBList[i].config(bg = "black", fg = BG_DEFAULT_COLOUR)
            else:
                self.__orderBList[i].config(bg = BG_DEFAULT_COLOUR, fg = "black")

        self.__order = number
        #self.__orderChanged()

    #not working skip for now maybe move back
    def deactivateOrderBs(self, takenList):
        if self.__orderBList != []:
            print(self.__orderBList)
            for i in range(len(self.__orderBList)):
                if i+1 in takenList:
                    self.__orderBList[i].config(state="disabled")
                else:
                    self.__orderBList[i].config(state="active")

    #to read class attributes, programming to an interface
    def getOrder(self):
        return self.__order
    
    def getName(self):
        return self.__nameEntry.get()
    
    def getType(self):
        return self.__type
    
    def getIsPlaying(self):
        return self.__isPlaying

    def __deletePlayer(self):
        #reset all vaiables if player selection box is deleted
        self.__isPlaying = False
        self.__name = ""
        self.__type = "player"
        self.__order = 0

        for widget in self.__frame.winfo_children():
            widget.destroy()
        tk.Button(self.__frame, text = "New Player", command = lambda: self.__newPlayer()).pack()