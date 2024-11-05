import tkinter as tk

class main_window:
    def __init__(self):
        self.__window = tk.Tk()
        self.__window.attributes('-fullscreen', True)

        self.__window.title("Carcassonne")

        tk.Label(self.__window,text ="Carcassonne").pack()

        tk.Button(self.__window, text = "start", command = self.__start).pack()

        tk.Button(self.__window, text="Exit", command=self.__window.destroy).pack()
    
    def __start(self):
        print("start")

    def run(self):
        self.__window.mainloop()

if __name__ == "__main__":
    main = main_window()
    main.run()