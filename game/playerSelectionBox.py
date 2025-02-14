import tkinter as tk
from constants import BUTTON_DEFAULT_COLOUR,TEXT_FONT


class playerSelectBox:
    def __init__(self, frame, changeOrderButtons):
        self.__frame = frame
        self.__type = "player"
        self.__order = 0
        self.__isPlaying = False

        #function to tell selectPlayersFrame a new order has been chosen
        self.__orderChanged = changeOrderButtons

        self.__orderBList = []
        self.__deletePlayer()

    def __newPlayer(self):
        #set for player count conditions in selectPlayers class
        self.__isPlaying = True
        
        #remove new player button and replace with player options
        for widget in self.__frame.winfo_children():
            widget.destroy()

        centreFrame = tk.Frame(self.__frame)
        centreFrame.place(relx=0.5,rely=0.5,anchor="center")

        tk.Label(centreFrame, text = "Name: ",font=(TEXT_FONT,13)).pack()
        self.__nameEntry = tk.Entry(centreFrame)
        self.__nameEntry.pack()

        #types can be bot or player
        tk.Label(centreFrame, text = "Type: ",font=(TEXT_FONT,13)).pack()
        self.__typeButton = tk.Button(centreFrame, text = self.__type,font=(TEXT_FONT,13), command = self.__typeChange, bg = BUTTON_DEFAULT_COLOUR)
        self.__typeButton.pack()

        tk.Label(centreFrame, text = "Order: ",font=(TEXT_FONT,13)).pack()

        self.__orderFrame = tk.Frame(centreFrame)
        self.__orderFrame.pack()

        #not done as for loop for ease of access, buttons stored in button list to be indexed
        self.__orderB1 = tk.Button(self.__orderFrame, text = "1", command = lambda: self.__selectOrder(1), bg = "grey94",font=(TEXT_FONT,13))
        self.__orderB2 = tk.Button(self.__orderFrame, text = "2", command = lambda: self.__selectOrder(2), bg = "grey94",font=(TEXT_FONT,13))
        self.__orderB3 = tk.Button(self.__orderFrame, text = "3", command = lambda: self.__selectOrder(3), bg = "grey94",font=(TEXT_FONT,13))
        self.__orderB4 = tk.Button(self.__orderFrame, text = "4", command = lambda: self.__selectOrder(4), bg = "grey94",font=(TEXT_FONT,13))
        self.__orderB5 = tk.Button(self.__orderFrame, text = "5", command = lambda: self.__selectOrder(5), bg = "grey94",font=(TEXT_FONT,13))
        self.__orderB6 = tk.Button(self.__orderFrame, text = "6", command = lambda: self.__selectOrder(6), bg = "grey94",font=(TEXT_FONT,13))

        self.__orderBList = [self.__orderB1, self.__orderB2, self.__orderB3, self.__orderB4, self.__orderB5, self.__orderB6,]

        #gridded as for loop to make ui easy to interperate
        for i in range(len(self.__orderBList)):
            self.__orderBList[i].grid(column=i, row=0)

        self.__orderChanged()

        tk.Button(centreFrame, text = "Delete", font=(TEXT_FONT,13), command = lambda: self.__deletePlayer(), bg = BUTTON_DEFAULT_COLOUR).pack(pady=10)

    def __typeChange(self):
        #self.__type not a bool even though only 2 states in case of additions in the future
        if self.__type == "player":
            self.__type = "bot"
        else:
            self.__type = "player"

        self.__typeButton.config(text = self.__type)

    #for changing colours and active states of the order buttons
    def __selectOrder(self, number):
        for i in range(len(self.__orderBList)):
            if i == number-1:
                self.__orderBList[i].config(bg = "black", fg = "grey94")
            else:
                self.__orderBList[i].config(bg = "grey94", fg = "black")

        self.__order = number
        self.__orderChanged()

    def deactivateOrderBs(self, takenList):
        if self.__isPlaying:
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
        self.__type = "player"
        self.__order = 0
        self.__orderChanged()

        for widget in self.__frame.winfo_children():
            widget.destroy()

        tk.Button(self.__frame, text = "+", font=(TEXT_FONT,50),command = lambda: self.__newPlayer(), bg = BUTTON_DEFAULT_COLOUR).pack(expand=True,fill="both")