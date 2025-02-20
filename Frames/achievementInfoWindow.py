import json
import tkinter as tk
from .subwindowBase import subwindowBase
from constants import FRAME_BG_DEFAULT_COLOUR, TEXT_FONT

class achievementInfoWindow(subwindowBase):
    def __init__(self,window):
        super().__init__(window, "Achievement Information")

    def _displayMainFrame(self):
        #opens achievement data to display onto window
        achievementData = open("jsonFiles/achievements.json", "r", encoding="utf-8")
        achievementDataDict = json.loads(achievementData.read())
        achievementData.close()

        for i in achievementDataDict.keys():
            tk.Label(self._mainFrame,text=achievementDataDict[i][0] + ": " + achievementDataDict[i][2],font=(TEXT_FONT,13),bg=FRAME_BG_DEFAULT_COLOUR).pack(anchor="nw")
            tk.Label(self._mainFrame,text="    -  " + achievementDataDict[i][1],font=(TEXT_FONT,13),bg=FRAME_BG_DEFAULT_COLOUR).pack(anchor="nw")         