
import tkinter as tk
from tkinter import ttk
from tkinter import Menu
from tkinter import messagebox
from . import views as views
from . import models as m
from . import constants as c
from tkinter import filedialog
import os
import pickle


FILENAME = "save.pickle"

class Application(tk.Tk):
    """Application root window"""

    def __init__(self):
        tk.Tk.__init__(self)

        # apply style for whole app
        self.apply_style_sheet()

        # select new or load in project
        self.select_project_screen()


# --------------- main screen setup

    # actuall main tool window
    def create_main_screen(self):
        # create main screen
        self.setup_screen()
        self.config(menu=self.menuBar)
        self.title("SIAM-ED Tool")
        # start in fullscreen
        # self.state('zoomed')

        # # set min and max screen size
        # self.minsize(width=1280, height=720)
        # self.maxsize(width=1920, height=1080)

        # .geometry("window width x window height + position right + position down")
        # width = self.winfo_screenwidth()
        # height = self.winfo_screenheight()

        width = 1280
        height = 720

        position_left = 100
        position_right = 100


        self.geometry("{}x{}+{}+{}".format(width, height, position_left, position_right))

        # set size window fixed
        self.resizable(0, 0)

    def setup_screen(self):
        notebook = ttk.Notebook(self)

        self.project_purpose_screen = views.ProjectPurposeScreen()
        self.data_collection_screen = views.DataCollectionScreen()
        self.data_analysis_screen = views.DataAnalysisScreen()
        self.impact_assessment_screen = views.EvaluationScreen()

        notebook.add(self.project_purpose_screen, text='1- Project purpose')
        notebook.add(self.data_collection_screen, text='2- Data collection')
        notebook.add(self.data_analysis_screen, text='3- Data analysis')
        notebook.add(self.impact_assessment_screen, text='4- Evaluation')

        notebook.grid(row=1, column=1, sticky='E', padx=10, pady=(5,10), ipadx=5, ipady=5)

    def apply_style_sheet(self):
        # styling
        style = ttk.Style()
        style.theme_use('winnative')
        style.configure("Treeview.Heading",
                        background="#c0d2ed",
                        foreground="black",
                        font=('Helvetica', 12))

        # normal labelframe style
        style.configure("TLabelframe.Label",
                        foreground="#4085f5")

        # documentation header style
        style.configure("Doc.TLabelframe.Label",
                        font=('lucida', 13),
                        foreground="#234987")

        # highlight active tab
        # style.configure("TNotebook.Tab", background="green3")
        style.map("TNotebook.Tab", background=[("selected", "#c6bef7")])

        # combobox background
        style.map('TCombobox', fieldbackground=[('readonly', 'white')])
        style.map('TCombobox', selectbackground=[('readonly', 'white')])
        style.map('TCombobox', selectforeground=[('readonly', 'black')])

    def setup_menu(self):
        self.menuBar = Menu(master=self)
        self.filemenu = Menu(self.menuBar, tearoff=0)
        self.filemenu.add_command(label="New", command='')
        self.filemenu.add_command(label="Load", command='')
        self.filemenu.add_command(label="Save", command='')
        self.filemenu.add_command(label="Quit", command=self.quit_application)
        self.menuBar.add_cascade(label="File", menu=self.filemenu)

        # menu item: help
        self.help_menu = Menu(self.menuBar, tearoff=0)
        self.help_menu.add_command(label="Documentation")
        self.help_menu.add_command(label="About")
        self.menuBar.add_cascade(label="Help", menu=self.help_menu)

# --------------- select project

    def select_project_screen(self):

        self.project_screen = tk.Toplevel()
        self.project_screen.title("Project selection")

        width = 400
        height = 230
        position_left = 100
        position_right = 100

        self.project_screen.geometry("{}x{}+{}+{}".format(width, height, position_left, position_right))

        # set size window fixed
        self.project_screen.resizable(0, 0)

        frame_project = ttk.LabelFrame(self.project_screen, text="Select new or exisiting project file",
                                       style='Doc.TLabelframe',
                                       width=380, height=210)

        frame_project.grid_propagate(0)
        frame_project.grid(padx=10, pady=10,
                           sticky='nsew')

        tk.Label(frame_project,
                 text='Create new project:',
                 font='Helvetica 13').grid(row=0, column=0,
                                           sticky='w',
                                           padx=(20, 0), pady=(10, 0))

        # create new project button:
        tk.Button(frame_project,
                  text='New',
                  width=c.Size.button_width, height=c.Size.button_height,
                  command=lambda: [self.create_new_project()]).grid(row=1, column=0,
                                                                    padx=30, pady=(5, 20),
                                                                    sticky='w')

        tk.Label(frame_project,
                 text='Load project:',
                 font='Helvetica 13').grid(row=2, column=0,
                                           sticky='w',
                                           padx=(20, 0))

        # create load project button
        tk.Button(frame_project,
                  text='Load',
                  width=c.Size.button_width, height=c.Size.button_height,
                  command=lambda: []).grid(row=3, column=0,
                                           padx=30, pady=5,
                                           sticky='w')

        self.project_screen.transient(self)  # set to be on top of the main window
        self.project_screen.grab_set()  # hijack all commands from the master (clicks on the main window are ignored)

    def create_new_project(self):

        f = filedialog.asksaveasfile(mode='w', defaultextension=".pickle")

        # if cancelled
        if f is None:
            return

        #get file path of new file
        self.file_path = f.name

        print('f: ', f)

        # delete select project screen
        self.project_screen.destroy()

        self.setup_menu()
        self.create_main_screen()

        # Un hardcode it
        dirname = os.getcwd()
        name_db = 'test2.db'
        self.database = os.path.join(dirname, 'data', 'sql', name_db)

        # create db and send data to views
        self.send_data()

# --------------- database

    def send_data(self):
        # create database
        self.create_database(self.database)

        # create path model
        self.create_path_dict()

        # populate measure point table
        self.data_model.populate_measure_point_query()

        # send data_model object to other functions
        self.project_purpose_screen.send_data_object(self.data_model)
        self.data_analysis_screen.send_data_object(self.data_model)
        self.impact_assessment_screen.send_data_object(self.data_model)

        # send path dict to data collection and data analysis
        self.data_collection_screen.send_dict_paths(self.path_model)
        self.data_analysis_screen.send_dict_paths(self.path_model)

    def create_database(self, database):
        self.data_model = m.SQLModel(database)

    def create_path_dict(self):
        self.path_model = m.pathModel()

# --------------- button functions

    # exit GUI cleanly
    def quit_application(self):
        self.quit()
        self.destroy()
        exit()
