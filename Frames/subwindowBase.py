import tkinter as tk
from constants import FRAME_BG_DEFAULT_COLOUR, TEXT_FONT,FRAME_TOP_BAR_COLOUR,BUTTON_DEFAULT_COLOUR

class subwindowBase:
    def __init__(self,window,title):
        #tkinter window base class
        self._window = tk.Toplevel(window,bg=FRAME_BG_DEFAULT_COLOUR,highlightthickness=2)
        self._window.grab_set()
        self._window.focus_force()
        self._window.title(title)
        self._window.wm_overrideredirect(True)

        self._topBar = tk.Frame(self._window,bg=FRAME_TOP_BAR_COLOUR)
        self._mainFrame = tk.Frame(self._window,bg=FRAME_BG_DEFAULT_COLOUR)

        self._topBar.pack(fill="x",anchor="n")
        self._mainFrame.pack(fill="both",expand=True,anchor="n",side="top")

        tk.Label(self._topBar,text =title,font=(TEXT_FONT,16),bg=FRAME_TOP_BAR_COLOUR).pack(side="left")

        #for setting size of buttons
        self._pixel = tk.PhotoImage(width=1, height=1)

        button = tk.Button(self._topBar, text="❌",font=(TEXT_FONT,16), width=30,height=30,image=self._pixel, compound='c', command=self._window.destroy, bg = BUTTON_DEFAULT_COLOUR)
        button.image = self._pixel
        button.pack(side="right")

        self._displayMainFrame()

        self._center_window()

    #abstract method to require implementation for children
    def _displayMainFrame(self):
        pass

    def getWindow(self):
        return self._window

    def _center_window(self):
        self._window.update_idletasks()
        width = self._window.winfo_width()
        height = self._window.winfo_height()
        screen_width = self._window.winfo_screenwidth()
        screen_height = self._window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self._window.geometry(f"{width}x{height}+{x}+{y}")