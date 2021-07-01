import tkinter as tk
from tkinter import ttk
from datetime import datetime
from tkinter import Menu
from . import views as views
from . import models as m
from . import widgets as w


class Application(tk.Tk):
    """Application root window"""

    def __init__(self):
        tk.Tk.__init__(self)
        self.setup_menu()
        self.setup_screen()
        self.config(menu=self.menuBar)

        self.title("IA Tool")
        # start in fullscreen
        #self.state('zoomed')

        # set min and max screen size
        self.minsize(width=800, height=600)
        self.maxsize(width=1920, height=1080)


    def setup_menu(self):
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

    def setup_screen(self):
        notebook = ttk.Notebook(self)

        notebook.add(views.ProjectPurposeScreen(), text='1- Project purpose')
        notebook.add(views.DataCollectionScreen(), text='2- Data collection')
        notebook.add(views.DataAnalysisScreen(), text='3- Data analysis')
        notebook.add(views.ImpactAssessmentScreen(), text='3- Data analysis')

        notebook.pack(expand=1, fill="both")






    # Exit GUI cleanly
    def _quit(self):
        self.quit()
        self.destroy()
        exit()


