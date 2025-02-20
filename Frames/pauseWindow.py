import tkinter as tk
from constants import PAUSE_SIZE, BUTTON_DEFAULT_COLOUR,TEXT_FONT
from .controlsWindow import controlsWindow
from .subwindowBase import subwindowBase

class pauseWindow(subwindowBase):
    def __init__(self, window, isPlaying, saveFunc):
        self.__mainWindow = window
        self.__isPlaying = isPlaying
        self.__saveFunc = saveFunc

        super().__init__(window,"Paused")

    def _displayMainFrame(self):
        self._window.geometry(str(PAUSE_SIZE[0])+"x"+str(PAUSE_SIZE[1]))

        tk.Button(self._mainFrame, text="Resume",font=(TEXT_FONT,13), command = self._window.destroy, bg = BUTTON_DEFAULT_COLOUR).pack()

        if self.__isPlaying:
            #displays if there is a current game being played
            tk.Button(self._mainFrame, text="Save",font=(TEXT_FONT,13), command= self.__saveFunc, bg = BUTTON_DEFAULT_COLOUR).pack()

        tk.Button(self._mainFrame, text = "Controls",font=(TEXT_FONT,13), command = lambda: self.__openControlsWindow(), bg = BUTTON_DEFAULT_COLOUR).pack()
        
        tk.Button(self._mainFrame, text = "Exit",font=(TEXT_FONT,13), command = self.__mainWindow.destroy, bg = BUTTON_DEFAULT_COLOUR).pack()

    def __openControlsWindow(self):
        #holds until controls into window closed
        self._window.winfo_toplevel().wait_window(controlsWindow(self._window).getWindow())
        self._window.grab_set()
        self._window.focus_force()