
import tkinter as tk
from tkinter import ttk
from tkinter import Menu
from tkinter import messagebox
from . import views as views
from . import models as m
from . import constants as c
import os


class Application(tk.Tk):
    """Application root window"""

    def __init__(self):
        tk.Tk.__init__(self)

        self.style_app()
        self.setup_menu()

        self.select_project_screen()

        self.setup_screen()
        self.config(menu=self.menuBar)

        self.title("SIAM-ED Tool")
        # start in fullscreen
        # self.state('zoomed')

        # set min and max screen size
        self.minsize(width=1280, height=720)
        self.maxsize(width=1920, height=1080)

        # width = self.winfo_screenwidth()
        # height = self.winfo_screenheight()

        width = 1200
        height = 720

        self.geometry("{}x{}".format(width, height))



        # Un hardcode it
        dirname = os.getcwd()
        name_db = 'test2.db'
        database = os.path.join(dirname, 'data', 'sql', name_db)

        # create database
        self.create_database(database)

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

    def select_project_screen(self):

        global project_screen
        global new_project_screen

        self.project_screen = None
        self.new_project_screen = None

        if not self.project_screen:

            self.project_screen = tk.Toplevel()
            self.project_screen.geometry("400x230")

            self.project_screen.title("Project selection")

            frame_project = ttk.LabelFrame(self.project_screen, text="Select new or exisiting project file", style='Doc.TLabelframe',
                                                    width=380, height=210)
            frame_project.grid_propagate(0)
            frame_project.grid(padx=10, pady=10,
                               sticky='nsew')

            tk.Label(frame_project,
                     text='Create new project:',
                     font='Helvetica 13').grid(row=0, column=0,
                                                       sticky='w',
                                                       padx=(20, 0), pady=(10,0))

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

    def style_app(self):
        # styling
        style = ttk.Style()
        print('style names: ', style.theme_names())
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

        # combobox background
        style.map('TCombobox', fieldbackground=[('readonly', 'white')])
        style.map('TCombobox', selectbackground=[('readonly', 'white')])
        style.map('TCombobox', selectforeground=[('readonly', 'black')])

    def create_path_dict(self):
        self.path_model = m.pathModel()

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

    # exit GUI cleanly
    def quit_application(self):
        self.quit()
        self.destroy()
        exit()

    def close_window(self, window):
        window.destroy()
        self.new_project_screen = None

    # create new project
    def create_new_project(self):

        if not self.new_project_screen:

            self.new_project_screen = tk.Toplevel()
            self.new_project_screen.geometry("450x220")

            self.new_project_screen.title("New project")

            self.new_project_screen.protocol("WM_DELETE_WINDOW", lambda: self.close_window(self.new_project_screen))

            frame_new_project = ttk.LabelFrame(self.new_project_screen, text="Create new project",
                                           style='Doc.TLabelframe',
                                           width=430, height=200)

            frame_new_project.grid_propagate(0)
            frame_new_project.grid(padx=10, pady=10,
                               sticky='nsew')

            tk.Label(frame_new_project,
                     text='Enter project name:',
                     font='Helvetica 13').grid(row=0, column=0,
                                               sticky='w',
                                               padx=(20, 0), pady=(20, 0))

            # textbox to save project name
            project_name = tk.StringVar()
            project_name_input = ttk.Entry(frame_new_project, width=50, textvariable=project_name)
            project_name_input.grid(row=1, column=0,
                                               padx=10, pady=5)

            # TODO validate if name isnt already used (if there isnt already a database)
            # TODO save database with the file at the same location

            # textbox to save project name
            status_message = tk.StringVar()
            status_message.set('---STATUS MESSAGE---')

            tk.Label(frame_new_project,
                     textvariable=status_message,
                     foreground='red').grid(row=2, column=0,
                                               sticky='w',
                                               padx=(20, 0))


            # create new project button:
            tk.Button(frame_new_project,
                      text='Create',
                      width=c.Size.button_width, height=c.Size.button_height,
                      command=lambda: []).grid(row=3, column=0,
                                               padx=30, pady=(5, 20),
                                               sticky='w')

            # put it in front
            self.new_project_screen.grab_set()
            self.new_project_screen.focus()
            self.new_project_screen.grab_release()

        else:
            self.new_project_screen.deiconify()

            self.new_project_screen.grab_set()
            self.new_project_screen.focus()
            self.new_project_screen.grab_release()

            # self.new_project_screen.attributes('-topmost', 1)
            # self.new_project_screen.attributes('-topmost', 0)





