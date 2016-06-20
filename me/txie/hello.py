import tkinter as tk
import tkinter.ttk as ttk


class Window(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)  # Creates self.master
        helloLabel = ttk.Label(self, text="Hello Tkinter!")
        quitButton = ttk.Button(self, text="Quit", command=self.quit)
        helloLabel.pack()
        quitButton.pack()
        self.pack()


window = Window()  # Implicitly creates tk.Tk object
window.master.title("Hello")
window.master.mainloop()
