import tkinter as tk
from constants import PAUSE_SIZE, BUTTON_DEFAULT_COLOUR,TEXT_FONT,FRAME_BG_DEFAULT_COLOUR,FRAME_TOP_BAR_COLOUR
from .controlsWindow import controlsWindow

class pauseWindow:
    def __init__(self, window, isPlaying, saveFunc):
        #opens new window and sets to root to prevent user from accessing main window

        self.__window = window
        self.__pauseWindow = tk.Toplevel(self.__window,bg=FRAME_BG_DEFAULT_COLOUR,highlightthickness=2)
        self.__pauseWindow.grab_set()
        self.__pauseWindow.focus_force()
        self.__pauseWindow.title("Paused")
        self.__pauseWindow.wm_overrideredirect(True)

        self.__pauseWindow.geometry(str(PAUSE_SIZE[0])+"x"+str(PAUSE_SIZE[1]))

        tk.Label(self.__pauseWindow,text ="Paused",font=(TEXT_FONT,16),bg=FRAME_TOP_BAR_COLOUR).pack(fill="x")
        tk.Button(self.__pauseWindow, text="Resume",font=(TEXT_FONT,13), command = self.__pauseWindow.destroy, bg = BUTTON_DEFAULT_COLOUR).pack()

        if isPlaying:
            #displays if there is a current game being played
            tk.Button(self.__pauseWindow, text="Save",font=(TEXT_FONT,13), command= saveFunc, bg = BUTTON_DEFAULT_COLOUR).pack()

        tk.Button(self.__pauseWindow, text = "Controls",font=(TEXT_FONT,13), command = lambda: controlsWindow(self.__pauseWindow), bg = BUTTON_DEFAULT_COLOUR).pack()
        
        tk.Button(self.__pauseWindow, text = "Exit",font=(TEXT_FONT,13), command = self.__window.destroy, bg = BUTTON_DEFAULT_COLOUR).pack()
        
        self.__center_window(self.__pauseWindow)

    def __openControls(self):
        self.__pauseWindow.winfo_toplevel().wait_window(controlsWindow(self.__pauseWindow).getWindow())
        self.__pauseWindow.grab_set()

    def __center_window(self, window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")