import tkinter as tk
from tkinter import ttk
from datetime import datetime
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import filedialog
from . import widgets as w
from . import constants as c
from tkPDFViewer import tkPDFViewer as pdf
import webbrowser

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

        # make object
        self.project_pdf = w.PDFViewer(self)
        # convert to string var and set init text
        self.text_project_pdf = tk.StringVar()
        self.text_project_pdf.set("")
        # create label and place in gui
        self.project_label = tk.Label(frame_project_goals,
                 textvariable=self.text_project_pdf).grid(row=1, column=1, sticky='w')

        # create button with actions
        button_upload_1 = tk.Button(frame_project_goals,
                                    text='Upload',
                                    width=c.Size.button_width, height=c.Size.button_height,
                                    command= lambda: [self.project_pdf.get_file_path(), self.text_project_pdf.set(self.project_pdf.get_file_name())])

        # place upload button
        button_upload_1.grid(row=1, column=0,
                             padx=(10, 0), pady=5,
                             sticky='w')
        # place show button
        button_show_1 = tk.Button(frame_project_goals,
                                  text='Show',
                                  width=c.Size.button_width, height=c.Size.button_height,
                                  command=self.project_pdf.show_project_goals)

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

        # convert to string var and set init text
        self.text_goal_pdf = tk.StringVar()
        self.text_goal_pdf.set("")

        # create label and place in gui
        self.project_goals_label = tk.Label(frame_goal_model,
                                      textvariable=self.text_goal_pdf).grid(row=2, column=1, sticky='w')

        button_upload_2 = tk.Button(frame_goal_model,
                                    text='Upload',
                                    width=c.Size.button_width, height=c.Size.button_height,
                                    command=lambda: [self.goal_pdf.get_file_path(), self.text_goal_pdf.set(self.goal_pdf.get_file_name())])

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
                                          width=c.Size.label_frame_width, height=600)
        frame_select_method_fragments.grid_propagate(0)
        frame_select_method_fragments.grid(padx=(10, 0),
                              sticky='nsew')

        label_selected_method_fragments = tk.Label(frame_select_method_fragments,
                                       text='Select method fragments')

        label_selected_method_fragments.grid(row=1, column=0,
                                 padx=(20, 0),
                                 sticky='w')

        self.method_fragment = w.MethodFragmentSelection(self)

        # checkboxes and method fragments

        button_upload_3 = tk.Button(frame_select_method_fragments,
                                    text='Select',
                                    width=c.Size.button_width, height=c.Size.button_height,
                                  command=self.method_fragment.show_selection_screen)

        button_upload_3.grid(row=3, column=0,
                           padx=(10, 0),
                           pady=2,
                           sticky='w')

        label_generated_survey_questions = tk.Label(frame_select_method_fragments,
                                                    text='Generated survey questions: ')

        label_generated_survey_questions.grid(row=4, column=0,
                                              padx=(20, 0),
                                              sticky='w')
        # show button
        button_show = tk.Button(frame_select_method_fragments,
                                text='Show',
                                width=c.Size.button_width, height=c.Size.button_height,
                                command='')

        button_show.grid(row=5, column=0,
                         padx=(10, 0),
                         pady=2,
                         sticky='w')


        self.sendFrame(frame_select_method_fragments)
        # scrollbar = tk.Scrollbar(frame_select_method_fragments)
        # scrollbar.grid(column=6,
        #                  sticky='ns')
        #
        # mylist = tk.Listbox(frame_select_method_fragments, yscrollcommand=scrollbar.set, width=50)
        #
        # for line in self.method_fragment.checkbox_list:
        #     mylist.insert(tk.END, line)
        #     print("work?")
        #
        # # for line in range(100):
        # #     mylist.insert(tk.END, "This is question " + str(line))
        #
        # mylist.grid(row=6, column=0,
        #                  padx=(10, 0),
        #                  pady=2,
        #                  sticky='nswe')
        # scrollbar.config(command=mylist.yview)

    def sendFrame(self, frame):
        print('SENDFRAME: ',type(frame))
        self.method_fragment.retrieve_frame(frame)


    def getProjectPdfPath(self):
        self.project_pdf_file_path = filedialog.askopenfilename()

    def showProjectPdf(self):
        webbrowser.open("D:/x - Onedrive/OneDrive - Universiteit Utrecht/OneDrive/Uni/3-Master/3-Thesis/test_pdf.pdf")

    # def make_new_object(self):
    #     object = w.PDFViewer(self)
    #     return object

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

