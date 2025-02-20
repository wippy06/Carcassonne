import tkinter as tk
from constants import FRAME_BG_DEFAULT_COLOUR, TEXT_FONT, CONTROLS
from .subwindowBase import subwindowBase

class controlsWindow(subwindowBase):
    def __init__(self,window):
        super().__init__(window,"Controls")

    def _displayMainFrame(self):

        #displaying controls
        tk.Label(self._mainFrame,font=(TEXT_FONT,16),bg=FRAME_BG_DEFAULT_COLOUR,text="move view up: " + CONTROLS[0]).pack(side = "top",anchor="nw")
        tk.Label(self._mainFrame,font=(TEXT_FONT,16),bg=FRAME_BG_DEFAULT_COLOUR,text="move view down: " + CONTROLS[1]).pack(side = "top",anchor="nw")
        tk.Label(self._mainFrame,font=(TEXT_FONT,16),bg=FRAME_BG_DEFAULT_COLOUR,text="move view left: " + CONTROLS[2]).pack(side = "top",anchor="nw")
        tk.Label(self._mainFrame,font=(TEXT_FONT,16),bg=FRAME_BG_DEFAULT_COLOUR,text="move view right: " + CONTROLS[3]).pack(side = "top",anchor="nw")
        tk.Label(self._mainFrame,font=(TEXT_FONT,16),bg=FRAME_BG_DEFAULT_COLOUR,text="centre view to home: " + CONTROLS[4]).pack(side = "top",anchor="nw")
        tk.Label(self._mainFrame,font=(TEXT_FONT,16),bg=FRAME_BG_DEFAULT_COLOUR,text="rotate tile clockwise: " + CONTROLS[5]).pack(side = "top",anchor="nw")
        tk.Label(self._mainFrame,font=(TEXT_FONT,16),bg=FRAME_BG_DEFAULT_COLOUR,text="rotate tile anticlockwise: " + CONTROLS[6]).pack(side = "top",anchor="nw")
        tk.Label(self._mainFrame,font=(TEXT_FONT,16),bg=FRAME_BG_DEFAULT_COLOUR,text="confirm placement: " + CONTROLS[7]).pack(side = "top",anchor="nw")
        tk.Label(self._mainFrame,font=(TEXT_FONT,16),bg=FRAME_BG_DEFAULT_COLOUR,text="claim north side: " + CONTROLS[8]).pack(side = "top",anchor="nw")
        tk.Label(self._mainFrame,font=(TEXT_FONT,16),bg=FRAME_BG_DEFAULT_COLOUR,text="claim east side: " + CONTROLS[9]).pack(side = "top",anchor="nw")
        tk.Label(self._mainFrame,font=(TEXT_FONT,16),bg=FRAME_BG_DEFAULT_COLOUR,text="claim south side: " + CONTROLS[10]).pack(side = "top",anchor="nw")
        tk.Label(self._mainFrame,font=(TEXT_FONT,16),bg=FRAME_BG_DEFAULT_COLOUR,text="claim west side: " + CONTROLS[11]).pack(side = "top",anchor="nw")
        tk.Label(self._mainFrame,font=(TEXT_FONT,16),bg=FRAME_BG_DEFAULT_COLOUR,text="claim centre side: " + CONTROLS[12]).pack(side = "top",anchor="nw")
        tk.Label(self._mainFrame,font=(TEXT_FONT,16),bg=FRAME_BG_DEFAULT_COLOUR,text="remove claim: " + CONTROLS[13]).pack(side = "top",anchor="nw")
        tk.Label(self._mainFrame,font=(TEXT_FONT,16),bg=FRAME_BG_DEFAULT_COLOUR,text="open/close minimap: " + CONTROLS[14]).pack(side = "top",anchor="nw")
