import tkinter as tk
from tkinter import ttk
from datetime import datetime
from tkinter import Menu
from . import views as v
from . import models as m

class Application(tk.Tk):
    """Application root window"""

    def __init__(self):
        tk.Tk.__init__(self)
        self.createWidgets()
        self.config(menu=self.menuBar)

        self.title("IA Tool")
        # start in fullscreen
        self.state('zoomed')

        # set min and max screen size
        self.minsize(width=800, height=600)
        self.maxsize(width=1920, height=1080)

        ttk.Label(
            self,
            text="IA Tool",
            font=("TkDefaultFont", 16)
        ).grid(row=0)



    def createWidgets(self):
        self.menuBar = Menu(master=self)
        self.filemenu = Menu(self.menuBar, tearoff=0)
        self.filemenu.add_command(label="New", command='')
        self.filemenu.add_command(label="Quit", command=self._quit)
        self.menuBar.add_cascade(label="File", menu=self.filemenu)

        # menu item: data
        self.data_menu = Menu(master=self)
        self.data_menu = Menu(self.menuBar, tearoff=0)
        self.data_menu.add_command(label="Tables")
        self.data_menu.add_command(label="Graph")
        self.menuBar.add_cascade(label="Data", menu=self.data_menu)

        # menu item: help
        self.help_menu = Menu(self.menuBar, tearoff=0)
        self.help_menu.add_command(label="About")
        self.menuBar.add_cascade(label="Help", menu=self.help_menu)

        self.project_definition = v.ProjectDefinition(self)
        self.project_definition.grid(row=1, padx=10)

        self.tabs = v.Tabs(self)
        self.tabs.grid()


    # Exit GUI cleanly
    def _quit(self):
        self.quit()
        self.destroy()
        exit()

