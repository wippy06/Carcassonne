import tkinter as tk

class selectPlayers:
    def __init__(self, frame, gameSlot, gameFunc):
        self.__frame = frame
        self.__gameSlot = gameSlot
        self.__gameFile = open("gameSlots/slot"+str(self.__gameSlot)+".ccsn", "r+")
        self.__gameFunc = gameFunc

        self.__topLFrame = tk.Frame(frame)
        self.__topLFrame.pack(side="top")

        self.__topMFrame = tk.Frame(frame)
        self.__topMFrame.pack(side="top")

        self.__topRFrame = tk.Frame(frame)
        self.__topRFrame.pack(side="top")

        self.__bottomLFrame = tk.Frame(frame)
        self.__bottomLFrame.pack(side="top")

        self.__bottomMFrame = tk.Frame(frame)
        self.__bottomMFrame.pack(side="top")

        self.__bottomRFrame = tk.Frame(frame)
        self.__bottomRFrame.pack(side="top")

        self.__player1 = playerSelectBox(self.__topLFrame)
        self.__player2 = playerSelectBox(self.__topMFrame)
        self.__player3 = playerSelectBox(self.__topRFrame)
        self.__player4 = playerSelectBox(self.__bottomLFrame)
        self.__player5 = playerSelectBox(self.__bottomMFrame)
        self.__player6 = playerSelectBox(self.__bottomRFrame)
        
        self.__playerList = [self.__player1, self.__player2, self.__player3, self.__player4, self.__player5, self.__player6]

        tk.Button(self.__frame, text = "Continue", command = lambda: self.__confirmChoice()).pack()

    def __confirmChoice(self):
        for widget in self.__frame.winfo_children():
            widget.destroy()
        self.__gameFunc(self.__gameSlot)




class playerSelectBox:
    def __init__(self, frame):
        self.__frame = frame
        self.__name = ""
        self.__deletePlayer()

    def __newPlayer(self):
        for widget in self.__frame.winfo_children():
            widget.destroy()

        tk.Label(self.__frame, text = "Name: ").pack()
        self.__name = tk.Entry(self.__frame)
        self.__name.pack()

        tk.Button(self.__frame, text = "Delete", command = lambda: self.__deletePlayer()).pack()

    def __typeChange(self):
        #tk button, when pressed text on button changes
        pass

    def __deletePlayer(self):
        for widget in self.__frame.winfo_children():
            widget.destroy()
        tk.Button(self.__frame, text = "New Player", command = lambda: self.__newPlayer()).pack()