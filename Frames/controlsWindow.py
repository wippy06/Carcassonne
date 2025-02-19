import tkinter as tk
from constants import FRAME_BG_DEFAULT_COLOUR, FRAME_TOP_BAR_COLOUR, TEXT_FONT, BUTTON_DEFAULT_COLOUR, CONTROLS

class controlsWindow:
    def __init__(self,window):
        self.__controlWindow = tk.Toplevel(window,bg=FRAME_BG_DEFAULT_COLOUR,highlightthickness=2)
        self.__controlWindow.grab_set()
        self.__controlWindow.focus_force()
        self.__controlWindow.title("Controls")
        self.__controlWindow.wm_overrideredirect(True)

        controlWindowTopBar = tk.Frame(self.__controlWindow,bg=FRAME_TOP_BAR_COLOUR)
        controlWindowMainFrame = tk.Frame(self.__controlWindow,bg=FRAME_BG_DEFAULT_COLOUR)

        controlWindowTopBar.pack(fill="x",anchor="n")
        controlWindowMainFrame.pack(fill="both",expand=True,anchor="n",side="top")

        tk.Label(controlWindowTopBar,text ="Controls",font=(TEXT_FONT,16),bg=FRAME_TOP_BAR_COLOUR).pack(side="left")

        pixel = tk.PhotoImage(width=1, height=1)
        button = tk.Button(controlWindowTopBar, text="❌",font=(TEXT_FONT,16), width=30,height=30,image=pixel, compound='c', command=self.__controlWindow.destroy, bg = BUTTON_DEFAULT_COLOUR)
        button.image = pixel
        button.pack(side="right")

        tk.Label(controlWindowMainFrame,font=(TEXT_FONT,16),bg=FRAME_BG_DEFAULT_COLOUR,text="move view up: " + CONTROLS[0]).pack(side = "top",anchor="nw")
        tk.Label(controlWindowMainFrame,font=(TEXT_FONT,16),bg=FRAME_BG_DEFAULT_COLOUR,text="move view down: " + CONTROLS[1]).pack(side = "top",anchor="nw")
        tk.Label(controlWindowMainFrame,font=(TEXT_FONT,16),bg=FRAME_BG_DEFAULT_COLOUR,text="move view left: " + CONTROLS[2]).pack(side = "top",anchor="nw")
        tk.Label(controlWindowMainFrame,font=(TEXT_FONT,16),bg=FRAME_BG_DEFAULT_COLOUR,text="move view right: " + CONTROLS[3]).pack(side = "top",anchor="nw")
        tk.Label(controlWindowMainFrame,font=(TEXT_FONT,16),bg=FRAME_BG_DEFAULT_COLOUR,text="centre view to home: " + CONTROLS[4]).pack(side = "top",anchor="nw")
        tk.Label(controlWindowMainFrame,font=(TEXT_FONT,16),bg=FRAME_BG_DEFAULT_COLOUR,text="rotate tile clockwise: " + CONTROLS[5]).pack(side = "top",anchor="nw")
        tk.Label(controlWindowMainFrame,font=(TEXT_FONT,16),bg=FRAME_BG_DEFAULT_COLOUR,text="rotate tile anticlockwise: " + CONTROLS[6]).pack(side = "top",anchor="nw")
        tk.Label(controlWindowMainFrame,font=(TEXT_FONT,16),bg=FRAME_BG_DEFAULT_COLOUR,text="confirm placement: " + CONTROLS[7]).pack(side = "top",anchor="nw")
        tk.Label(controlWindowMainFrame,font=(TEXT_FONT,16),bg=FRAME_BG_DEFAULT_COLOUR,text="claim north side: " + CONTROLS[8]).pack(side = "top",anchor="nw")
        tk.Label(controlWindowMainFrame,font=(TEXT_FONT,16),bg=FRAME_BG_DEFAULT_COLOUR,text="claim east side: " + CONTROLS[9]).pack(side = "top",anchor="nw")
        tk.Label(controlWindowMainFrame,font=(TEXT_FONT,16),bg=FRAME_BG_DEFAULT_COLOUR,text="claim south side: " + CONTROLS[10]).pack(side = "top",anchor="nw")
        tk.Label(controlWindowMainFrame,font=(TEXT_FONT,16),bg=FRAME_BG_DEFAULT_COLOUR,text="claim west side: " + CONTROLS[11]).pack(side = "top",anchor="nw")
        tk.Label(controlWindowMainFrame,font=(TEXT_FONT,16),bg=FRAME_BG_DEFAULT_COLOUR,text="claim centre side: " + CONTROLS[12]).pack(side = "top",anchor="nw")
        tk.Label(controlWindowMainFrame,font=(TEXT_FONT,16),bg=FRAME_BG_DEFAULT_COLOUR,text="remove claim: " + CONTROLS[13]).pack(side = "top",anchor="nw")
        tk.Label(controlWindowMainFrame,font=(TEXT_FONT,16),bg=FRAME_BG_DEFAULT_COLOUR,text="open/close minimap: " + CONTROLS[14]).pack(side = "top",anchor="nw")

        self.__center_window(self.__controlWindow)

    def getWindow(self):
        return self.__controlWindow

    def __center_window(self, window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")