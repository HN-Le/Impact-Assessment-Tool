import tkinter as tk
from tkinter import ttk
from datetime import datetime
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import filedialog
from . import widgets as w
from . import constants as c


class ProjectPurposeScreen(tk.Frame):

    def __init__(self):
        tk.Frame.__init__(self)

        frame_project_goals = ttk.LabelFrame(self, text="1.1 Project Goals",
                                             width=c.Size.label_frame_width, height=c.Size.label_frame_height)
        frame_project_goals.grid_propagate(0)
        frame_project_goals.grid(padx=(10,0),
                                 sticky='nsew')

        label_project_goals = tk.Label(frame_project_goals,
                         text='Identify project goals')

        label_project_goals.grid(row=0, column=0,
                   padx=(20, 0),
                   sticky='nsew')

        self.project_pdf = w.PDFViewer(self)


        button_upload_1 = tk.Button(frame_project_goals,
                                    text='Upload',
                                    width=c.Size.button_width, height=c.Size.button_height,
                                    command= lambda: [self.project_pdf.get_file_path(), tk.Label(frame_project_goals,
                                                text=self.project_pdf.file_path).grid(row=1, column=1, sticky='nsew')])

        button_upload_1.grid(row=1, column=0,
                             padx=(10, 0), pady=5,
                             sticky='w')


        button_show_1 = tk.Button(frame_project_goals,
                                  text='Show',
                                  width=c.Size.button_width, height=c.Size.button_height,
                                  command= self.project_pdf.show_project_goals)

        button_show_1.grid(row=2, column=0,
                         padx=(10, 0),
                         pady=2,
                         sticky='w')

        # -------------------------------------------------------------------------------------------

        frame_goal_model = ttk.LabelFrame(self, text="1.2 Goal Model",
                                          width=c.Size.label_frame_width, height=c.Size.label_frame_height)
        frame_goal_model.grid_propagate(0)
        frame_goal_model.grid(padx=(10, 0),
                              sticky='nsew')

        label_project_goals = tk.Label(frame_goal_model,
                                       text='Create goal model')

        label_project_goals.grid(row=1, column=0,
                                 padx=(20, 0),
                                 sticky='nsew')

        self.goal_pdf = w.PDFViewer(self)

        button_upload_2 = tk.Button(frame_goal_model,
                                    text='Upload',
                                    width=c.Size.button_width, height=c.Size.button_height,
                                    command=lambda: [self.goal_pdf.get_file_path(), tk.Label(frame_goal_model,
                                                                                           text=self.goal_pdf.file_path).grid(
                                      row=2, column=2, sticky='nsew')])

        button_upload_2.grid(row=2, column=0,
                           padx=(10, 0),
                           pady=5,
                           sticky='w')

        button_show_2 = tk.Button(frame_goal_model,
                                  text='Show',
                                  width=c.Size.button_width, height=c.Size.button_height,
                                  command=lambda: [self.goal_pdf.show_project_goals()])

        button_show_2.grid(row=3, column=0,
                         padx=(10, 0),
                         pady=2,
                         sticky='w')

        # -------------------------------------------------------------------------------------------

        frame_select_method_fragments = ttk.LabelFrame(self, text="1.3 Method Fragments",
                                          width=c.Size.label_frame_width, height=c.Size.label_frame_height)
        frame_select_method_fragments.grid_propagate(0)
        frame_select_method_fragments.grid(padx=(10, 0),
                              sticky='nsew')

        label_project_goals = tk.Label(frame_select_method_fragments,
                                       text='Select method fragments')

        label_project_goals.grid(row=1, column=0,
                                 padx=(20, 0),
                                 sticky='nsew')

        button_upload_3 = tk.Button(frame_select_method_fragments,
                                    text='Select',
                                    width=c.Size.button_width, height=c.Size.button_height,
                                  command='')

        button_upload_3.grid(row=3, column=0,
                           padx=(10, 0),
                           pady=2,
                           sticky='w')


class DataCollectionScreen(tk.Frame):

    def __init__(self):
        tk.Frame.__init__(self)
        tk.Label(self, text='Data collection content').pack()


class DataAnalysisScreen(tk.Frame):

    def __init__(self):
        tk.Frame.__init__(self)
        frame_project_goals = ttk.LabelFrame(self, text="Test")
        frame_project_goals.pack(fill="both", expand="yes")

        label = tk.Label(frame_project_goals, text='Data analysis content')
        label.pack()


class ImpactAssessmentScreen(tk.Frame):

    def __init__(self):
        tk.Frame.__init__(self)
        tk.Label(self, text='Impact assessment content').pack()

