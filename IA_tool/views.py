import tkinter as tk
from tkinter import ttk
from datetime import datetime
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import filedialog
from . import widgets as w


class ProjectPurposeScreen(tk.Frame):

    def __init__(self):
        tk.Frame.__init__(self)

        frame_project_goals = ttk.LabelFrame(self, text="1.1 Project Goals", width=600, height=200)
        frame_project_goals.grid_propagate(0)
        frame_project_goals.grid(padx=(10,0),
                                 sticky='nsew')

        label_project_goals = tk.Label(frame_project_goals,
                         text='Identify project goals')

        label_project_goals.grid(row=0, column=0,
                   padx=(20, 0),
                   sticky='nsew')

        button_upload = tk.Button(frame_project_goals, text='Upload', command='')
        button_upload.grid(row=1, column=0,
                           padx=(10, 0),
                           pady=5,
                           sticky='ew')

        button_show = tk.Button(frame_project_goals, text='Show', command='')
        button_show.grid(row=2, column=0,
                         padx=(10, 0),
                         pady=2,
                         sticky='ew')

        label_file_path = tk.Label(frame_project_goals,
                         text='- FILEPATH -')

        label_file_path.grid(row=1, column=1,
                   padx=(20, 0),
                   sticky='nsew')
        



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