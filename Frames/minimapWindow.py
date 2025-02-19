import tkinter as tk
from constants import MINIMAP_MAX_SIZE,CONTROLS,EMPTY_COLOUR,FRAME_TOP_BAR_COLOUR,TEXT_FONT,BUTTON_DEFAULT_COLOUR

class minimapWindow:
    def __init__(self,window,board):

        minimapWindow = tk.Toplevel(window, highlightthickness=2)
        minimapWindow.grab_set()
        minimapWindow.focus_force()
        minimapWindow.title("Minimap")
        minimapWindow.wm_overrideredirect(True)

        minimapTopBar = tk.Frame(minimapWindow,bg=FRAME_TOP_BAR_COLOUR)
        minimapMainFrame = tk.Frame(minimapWindow)

        minimapTopBar.pack(fill="x")
        minimapMainFrame.pack()

        tk.Label(minimapTopBar,text ="Minimap",font=(TEXT_FONT,16),bg=FRAME_TOP_BAR_COLOUR).pack(side="left")

        pixel = tk.PhotoImage(width=1, height=1)
        button = tk.Button(minimapTopBar, text="❌",font=(TEXT_FONT,16), width=30,height=30,image=pixel, compound='c', command=minimapWindow.destroy, bg = BUTTON_DEFAULT_COLOUR)
        button.image = pixel
        button.pack(side="right")

        #used to determine size of grid and size of tiles
        minX, maxX, minY, maxY = 0,0,0,0

        for coord in board.keys():
            if coord[0]<minX:
                minX = coord[0]
            elif coord[0]>maxX:
                maxX = coord[0]

            if coord[1]<minY:
                minY = coord[1]
            elif coord[1]>maxY:
                maxY = coord[1]

        gridSizeX = maxX-minX+1
        gridSizeY = maxY-minY+1

        #offset used to translate coord key to grid list index
        offsetX = -minX
        offsetY = -minY

        tileSize = min(MINIMAP_MAX_SIZE[0]//gridSizeX,MINIMAP_MAX_SIZE[1]//gridSizeY)

        tileGridCanvasList = []
        #grid stored as 2D array for tile grid
        for i in range(gridSizeX):
            tileGridCanvasList.append([])
            for j in range(gridSizeY):
                tileGridCanvasList[i].append(tk.Canvas(minimapMainFrame, width=tileSize, height=tileSize,highlightthickness=1, highlightbackground="black",bg="grey94"))

        for i in range(len(tileGridCanvasList)):
            for j in range(len(tileGridCanvasList[i])):
                tileGridCanvasList[i][j].grid(row=j,column=i)

        tileCoordList = list(board.keys())
        #draws tiles within the grid
        for coord in tileCoordList:
            board[coord].draw(tileGridCanvasList[coord[0]+offsetX][coord[1]+offsetY],False)
        
        self.__center_window(minimapWindow)

        minimapWindow.bind(CONTROLS[14],lambda event: minimapWindow.destroy())

    def __center_window(self, window):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - window.winfo_reqwidth()) // 2
        y = (screen_height - window.winfo_reqheight()) // 2
        window.geometry(f"+{x}+{y}")


        

