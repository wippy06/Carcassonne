import json
import tkinter as tk
from constants import FRAME_BG_DEFAULT_COLOUR, FRAME_TOP_BAR_COLOUR, TEXT_FONT, BUTTON_DEFAULT_COLOUR, CONTROLS

class achievementInfoWindow:
    def __init__(self,window):
        self.__achievementInfoWindow = tk.Toplevel(window,bg=FRAME_BG_DEFAULT_COLOUR,highlightthickness=2)
        self.__achievementInfoWindow.grab_set()
        self.__achievementInfoWindow.focus_force()
        self.__achievementInfoWindow.title("Controls")
        self.__achievementInfoWindow.wm_overrideredirect(True)

        achievementInfoWindowTopBar = tk.Frame(self.__achievementInfoWindow,bg=FRAME_TOP_BAR_COLOUR)
        achievementInfoWindowMainFrame = tk.Frame(self.__achievementInfoWindow,bg=FRAME_BG_DEFAULT_COLOUR)

        achievementInfoWindowTopBar.pack(fill="x",anchor="n")
        achievementInfoWindowMainFrame.pack(fill="both",expand=True,anchor="n",side="top")

        tk.Label(achievementInfoWindowTopBar,text ="Achievement Information",font=(TEXT_FONT,16),bg=FRAME_TOP_BAR_COLOUR).pack(side="left")

        pixel = tk.PhotoImage(width=1, height=1)

        button = tk.Button(achievementInfoWindowTopBar, text="❌",font=(TEXT_FONT,16), width=30,height=30,image=pixel, compound='c', command=self.__achievementInfoWindow.destroy, bg = BUTTON_DEFAULT_COLOUR)
        button.image = pixel
        button.pack(side="right")

        achievementData = open("jsonFiles/achievements.json", "r", encoding="utf-8")
        achievementDataDict = json.loads(achievementData.read())
        achievementData.close()

        for i in achievementDataDict.keys():
            tk.Label(achievementInfoWindowMainFrame,text=achievementDataDict[i][0] + ": " + achievementDataDict[i][2],font=(TEXT_FONT,13),bg=FRAME_BG_DEFAULT_COLOUR).pack(anchor="nw")
            tk.Label(achievementInfoWindowMainFrame,text="    -  " + achievementDataDict[i][1],font=(TEXT_FONT,13),bg=FRAME_BG_DEFAULT_COLOUR).pack(anchor="nw")         

        self.__center_window(self.__achievementInfoWindow)

    def getWindow(self):
        return self.__achievementInfoWindow

    def __center_window(self, window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")