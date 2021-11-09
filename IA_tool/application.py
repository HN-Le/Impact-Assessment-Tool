
import tkinter as tk
from tkinter import ttk
from tkinter import Menu
from tkinter import messagebox
from . import views as views
from . import models as m
from . import constants as c
from . import widgets as w

from tkinter import filedialog
import os
import pickle


class Application(tk.Tk):
    """Application root window"""

    def __init__(self):
        tk.Tk.__init__(self)

        self.init_screen = False

        # apply style for whole app
        self.apply_style_sheet()

        # create save file object
        self.save_file_object = m.appDataModel()

        # select new or load in project
        self.select_project_screen()

        w.Window.focus_window(self, self)


# --------------- main screen setup

    def create_main_screen(self):
        # create main screen
        self.setup_screen()
        self.setup_menu()
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

        self.protocol("WM_DELETE_WINDOW", self.quit_application)


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

        self.init_screen = True

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
        style.map("TNotebook.Tab", background=[("selected", "#c6bef7")])

        # combobox background
        style.map('TCombobox', fieldbackground=[('readonly', 'white')])
        style.map('TCombobox', selectbackground=[('readonly', 'white')])
        style.map('TCombobox', selectforeground=[('readonly', 'black')])

    def setup_menu(self):
        self.menuBar = Menu(master=self)
        self.filemenu = Menu(self.menuBar, tearoff=0)

        self.filemenu.add_command(label="New", command=lambda : [self.new_or_load_menu_bar('new_project')])
        self.filemenu.add_command(label="Load", command=lambda : [self.new_or_load_menu_bar('load_project')])
        self.filemenu.add_command(label="Save", command=self.save_application)
        self.filemenu.add_command(label="Quit", command=lambda : [self.quit_application()])

        self.menuBar.add_cascade(label="File", menu=self.filemenu)

        self.help_menu = Menu(self.menuBar, tearoff=0)
        self.help_menu.add_command(label="Documentation")
        self.help_menu.add_command(label="About")
        self.menuBar.add_cascade(label="Help", menu=self.help_menu)

# --------------- new project / load project

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

        self.project_screen.protocol("WM_DELETE_WINDOW", self.quit_application)


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
                  command=lambda: [self.load_in_project()]).grid(row=3, column=0,
                                           padx=30, pady=5,
                                           sticky='w')

        self.project_screen.transient(self)

        self.project_screen.takefocus = True
        self.project_screen.focus_set()

        self.project_screen.grab_set_global()



    def create_new_project(self):

        self.save_file_object.load_from_save_file = False

        filetypes = [
            ('Pickle Save File', '*.pickle')
        ]

        f = filedialog.asksaveasfile(mode='w',
                                     defaultextension=".pickle",
                                     filetypes=filetypes,
                                     title="Create new project")

        # if cancelled
        if f is None:
            return

        #get file path and dir of new file
        self.file_path = f.name
        self.file_dir = (self.file_path.rsplit("/", 1))[0]
        self.file_name = (self.file_path.rsplit("/", 1))[1].replace('.pickle', '')
        # self.file_name = self.file_name + ' - DATABASE'

        # print('self.file_path  ', self.file_path)
        # print('self.file_dir  ', self.file_dir)

        # delete select project screen
        self.project_screen.destroy()

        self.create_main_screen()

        self.send_save_file()

        # # Un hardcode it
        # dirname = os.getcwd()
        # name_db = 'test2.db'
        # self.database = os.path.join(dirname, 'data', 'sql', name_db)

        file_extention = '.db'
        db_file_path = self.file_dir + '/' + self.file_name + file_extention

        # overwrite old db (file name should be identical to db name!)
        if os.path.isfile(db_file_path):
            os.remove(db_file_path)

        self.database = self.file_dir + '/' + self.file_name + file_extention

        # create database
        self.create_database(self.database, True)

        # create path model
        self.create_path_dict()

        # populate measure point table
        self.data_model.populate_measure_point_query()

        # send data to views
        self.send_data_db()

        self.title("SIAM-ED Tool - " + self.file_name)

        self.save_application()

    def load_in_project(self):

        filetypes = [('Pickle Save File', '*.pickle')]

        file = filedialog.askopenfilename(
            title='Load project file',
            filetypes=filetypes)

        # if cancelled
        if file:
            print ("file: ", file)

            self.file_path = file
            self.file_name = (self.file_path.rsplit("/", 1))[1].replace('.pickle', '')

            self.create_main_screen()

            # send save file to views
            self.send_save_file()

            # load from pickle save file
            self.save_file_object.load_from_file()

            self.load_path_dict()

            # check if linked database exists
            if not os.path.isfile(self.save_file_object.data['database_path']):
                print('load_in_project --- PATH DOES NOT EXISTS')
                return

            self.database = self.save_file_object.data['database_path']

            # link database
            self.create_database(self.database, False)

            self.save_file_object.load_from_save_file = True

            # send db to views
            self.send_data_db()

            # load saved variables from file
            self.project_purpose_screen.restore_from_save_file()
            self.data_collection_screen.restore_from_save_file()
            self.impact_assessment_screen.restore_from_save_file()

            self.update()
            self.project_screen.destroy()

            self.title("SIAM-ED Tool - " + self.file_name)


    def new_or_load_menu_bar(self, state):

        self.save_msg_popup()

        if state == 'new_project':
            self.create_new_project()
        elif state == 'load_project':
            self.load_in_project()

    def save_msg_popup(self):
        save_msgbox = messagebox.askquestion("askquestion", "Do you want to save the current project?")

        if save_msgbox == 'yes':
            self.save_application()

    # --------------- database

    def send_data_db(self):

        # send data_model object to other classes
        self.project_purpose_screen.send_data_object(self.data_model)
        self.data_analysis_screen.send_data_object(self.data_model)
        self.impact_assessment_screen.send_data_object(self.data_model)

        # send path dict to other classess
        self.project_purpose_screen.send_dict_paths(self.path_model)
        self.data_collection_screen.send_dict_paths(self.path_model)
        self.data_analysis_screen.send_dict_paths(self.path_model)

    def send_save_file(self):
        # create appDataModel object for all saved data
        self.save_file_object.get_file_name(self.file_path)

        # send appData object to other classes
        self.project_purpose_screen.send_save_file_object(self.save_file_object)
        self.data_collection_screen.send_save_file_object(self.save_file_object)
        self.data_analysis_screen.send_save_file_object(self.save_file_object)
        self.impact_assessment_screen.send_save_file_object(self.save_file_object)

    def create_database(self, database, new):
        self.data_model = m.SQLModel(database, new)

    def create_path_dict(self):
        self.path_model = m.pathModel()

    def load_path_dict(self):
        self.path_model = self.save_file_object.data['path_model']

# --------------- button functions

    # exit GUI cleanly
    def quit_application(self):

        if self.init_screen:
            self.save_msg_popup()
            self.quit()
            self.destroy()
            exit()
        else:
            self.quit()
            self.destroy()
            exit()


    def save_application(self):
        self.project_purpose_screen.save_data()
        self.data_collection_screen.save_data()
        self.data_analysis_screen.save_data()
        self.impact_assessment_screen.save_data()

        self.save_file_object.save_to_file(self.database, self.path_model)





