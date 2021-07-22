import tkinter as tk
from tkinter import ttk
from datetime import datetime
from tkinter import Menu
from . import views as views
from . import models as m
from . import widgets as w
import os
from pathlib import Path
import pandas as pd

class Application(tk.Tk):
    """Application root window"""

    def __init__(self):
        tk.Tk.__init__(self)
        self.setup_menu()
        self.setup_screen()
        self.config(menu=self.menuBar)

        self.title("IA Tool")
        # start in fullscreen
        # self.state('zoomed')

        # set min and max screen size
        self.minsize(width=800, height=600)
        self.maxsize(width=1920, height=1080)

        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()

        # self.geometry("{}x{}".format(width, height))

        # Un hardcode it
        dirname = os.getcwd()
        name_db = 'test2.db'
        database = os.path.join(dirname, 'data', 'sql', name_db)
        self.create_database(database)

        # test_row = ("NAME", 5, "TEST DEFINITION",
        #             "TEST QUESTION? ", "MULTIPLE CHOICE", None, None, "student")

        # self.data_model.create_metric(self.data_model.conn, test_row)

        self.project_purpose_screen.send_data_object(self.data_model)





    def create_database(self, database):
        self.data_model = m.SQLModel(database)


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

        self.project_purpose_screen = views.ProjectPurposeScreen()
        self.data_collection_screen = views.DataCollectionScreen()
        self.data_analysis_screen = views.DataAnalysisScreen()
        self.impact_assessment_screen = views.ImpactAssessmentScreen()

        notebook.add(self.project_purpose_screen, text='1- Project purpose')
        notebook.add(self.data_collection_screen, text='2- Data collection')
        notebook.add(self.data_analysis_screen, text='3- Data analysis')
        notebook.add(self.impact_assessment_screen, text='4- Evaluation')

        notebook.grid(row=1, column=1, sticky='E', padx=5, pady=5, ipadx=5, ipady=5)






    # Exit GUI cleanly
    def _quit(self):
        self.quit()
        self.destroy()
        exit()


