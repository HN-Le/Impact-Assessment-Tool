
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from . import widgets as w
from . import constants as c

from datetime import datetime
from tkinter import scrolledtext
from tkinter import Menu
from data.sql import create_db as database

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
                   padx=(10, 0), columnspan=2,
                   sticky='n')

        # make object
        self.project_pdf = w.FileOpener(self)

        # convert to string var and set init text
        self.text_project_pdf = tk.StringVar()
        self.text_project_pdf.set("")

        # create label and place in gui
        self.project_label = tk.Label(frame_project_goals,
                 textvariable=self.text_project_pdf).grid(row=3, column=0, sticky='w', padx=(20, 0), columnspan=150)

        # create button with actions
        button_upload_1 = tk.Button(frame_project_goals,
                                    text='Select',
                                    width=c.Size.button_width, height=c.Size.button_height,
                                    command= lambda: [self.project_pdf.get_file_path(), self.text_project_pdf.set(self.project_pdf.get_file_name())])

        # place upload button
        button_upload_1.grid(row=2, column=0,
                             padx=(10, 0), pady=5,
                             sticky='w')

        # todo project_goals add validation (don't execute when no filepath is selected)
        # place show button
        button_show_1 = tk.Button(frame_project_goals,
                                  text='Show',
                                  width=c.Size.button_width, height=c.Size.button_height,
                                  command=self.project_pdf.show_project_goals)

        button_show_1.grid(row=2, column=1,
                         padx=(10, 0), pady=5,
                         sticky='w')

        # -------------------------------------------------------------------------------------------

        frame_goal_model = ttk.LabelFrame(self, text="1.2 Goal Model",
                                          width=c.Size.label_frame_width, height=c.Size.label_frame_height)
        frame_goal_model.grid_propagate(0)
        frame_goal_model.grid(padx=(10, 0),
                              sticky='nsew')

        label_project_goals = tk.Label(frame_goal_model,
                                       text='Create goal model')

        label_project_goals.grid(row=0, column=0,
                                 padx=(10, 0),
                                 columnspan=2,
                                 sticky='w')

        self.goal_pdf = w.FileOpener(self)

        # convert to string var and set init text
        self.text_goal_pdf = tk.StringVar()
        self.text_goal_pdf.set("")

        # create label and place in gui
        self.project_goals_label = tk.Label(frame_goal_model,
                                      textvariable=self.text_goal_pdf).grid(row=4, column=0, sticky='w', padx=(20, 0), columnspan=150)

        button_upload_2 = tk.Button(frame_goal_model,
                                    text='Select',
                                    width=c.Size.button_width, height=c.Size.button_height,
                                    command=lambda: [self.goal_pdf.get_file_path(), self.text_goal_pdf.set(self.goal_pdf.get_file_name())])

        button_upload_2.grid(row=2, column=0,
                           padx=(10, 0),
                           pady=5,
                           sticky='w')

        # todo goal_model add validation (don't execute when no filepath is selected)
        button_show_2 = tk.Button(frame_goal_model,
                                  text='Show',
                                  width=c.Size.button_width, height=c.Size.button_height,
                                  command=lambda: [self.goal_pdf.show_project_goals()])

        button_show_2.grid(row=2, column=1,
                         padx=(10, 0),
                         pady=2,
                         sticky='w')

        # -------------------------------------------------------------------------------------------

        frame_select_method_fragments = ttk.LabelFrame(self, text="1.3 Method Fragments",
                                          width=1200, height=700)
        frame_select_method_fragments.grid_propagate(0)
        frame_select_method_fragments.grid(padx=(10, 0),
                              sticky='nsew')

        label_selected_method_fragments = tk.Label(frame_select_method_fragments,
                                       text='Select method fragments')

        label_selected_method_fragments.grid(row=1, column=0, columnspan=2,
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

        button_upload_4 = tk.Button(frame_select_method_fragments,
                                    text='Show',
                                    width=c.Size.button_width, height=c.Size.button_height,
                                    command=self.method_fragment.show_info_screen)

        button_upload_4.grid(row=3, column=1,
                             padx=(10, 0),
                             pady=2,
                             sticky='w')

        label_add_definition = tk.Label(frame_select_method_fragments,
                                                   text='Add metric definition & set targets')

        label_add_definition.grid(row=4, column=0, columnspan=100,
                                             padx=(20, 0), pady=(20, 0),
                                             sticky='w')

        button_upload_5 = tk.Button(frame_select_method_fragments,
                                    text='Add',
                                    width=c.Size.button_width, height=c.Size.button_height,
                                    command='')

        button_upload_5.grid(row=5, column=0,
                             padx=(10, 0),
                             pady=2,
                             sticky='w')

        button_upload_6 = tk.Button(frame_select_method_fragments,
                                    text='Show',
                                    width=c.Size.button_width, height=c.Size.button_height,
                                    command='')

        button_upload_6.grid(row=5, column=1,
                             padx=(10, 0),
                             pady=2,
                             sticky='w')

        self.sendFrame(frame_select_method_fragments)

    def sendFrame(self, frame):
        self.method_fragment.retrieve_frame(frame)


    def getProjectPdfPath(self):
        self.project_pdf_file_path = filedialog.askopenfilename()

    def send_data_object(self, data):
        self.data_object = data
        self.method_fragment.get_data_object(self.data_object)


class DataCollectionScreen(tk.Frame):

    def __init__(self):
        tk.Frame.__init__(self)

        global start_project_window
        self.start_project_window = None

        self.data_collection_window = self

        # --------- 2.1 Sampling strategy frame
        frame_sampling = ttk.LabelFrame(self, text="2.1 Sampling strategy",
                                                       width=1200, height=150)
        frame_sampling.grid_propagate(0)
        frame_sampling.grid(padx=(10, 0),
                                           sticky='nsew')

        label_sampling = tk.Label(frame_sampling,
                                                   text='Determine sampling strategy')

        label_sampling.grid(row=1, column=0, columnspan=100,
                                             padx=(20, 0),
                                             sticky='w')

        # make object
        self.project_pdf = w.FileOpener(self)

        # convert to string var and set init text
        self.text_sampling_pdf = tk.StringVar()
        self.text_sampling_pdf.set("")

        # create label and place in gui
        self.project_label = tk.Label(frame_sampling,
                                      textvariable=self.text_sampling_pdf).grid(row=3, column=0, sticky='w',
                                                                               padx=(20, 0), columnspan=150)

        # create button with actions
        button_upload_1 = tk.Button(frame_sampling,
                                    text='Select',
                                    width=c.Size.button_width, height=c.Size.button_height,
                                    command=lambda: [self.project_pdf.get_file_path(),
                                                     self.text_sampling_pdf.set(self.project_pdf.get_file_name())])

        # place upload button
        button_upload_1.grid(row=2, column=0,
                             padx=(10, 0), pady=5,
                             sticky='w')

        # todo sampling_strategy add validation (don't execute when no filepath is selected)
        # place show button
        button_show_1 = tk.Button(frame_sampling,
                                  text='Show',
                                  width=c.Size.button_width, height=c.Size.button_height,
                                  command=self.project_pdf.show_project_goals)

        button_show_1.grid(row=2, column=1,
                           padx=(10, 0), pady=5,
                           sticky='w')

        # --------- 2.2 Data collection frame
        frame_data_collection = ttk.LabelFrame(self, text="2.2 Data collection",
                                        width=1200, height=700)
        frame_data_collection.grid_propagate(0)
        frame_data_collection.grid(padx=(10, 0),
                            sticky='nsew')

        label_data_collection = tk.Label(frame_data_collection,
                                  text='mWater Guide')

        label_data_collection.grid(row=1, column=0, columnspan=100,
                            padx=(20, 0),
                            sticky='w')

        button_show_2 = tk.Button(frame_data_collection,
                                  text='Show',
                                  width=c.Size.button_width, height=c.Size.button_height,
                                  command='')

        button_show_2.grid(row=2, column=0,
                           padx=(10, 0), pady=(5, 10),
                           sticky='w')

        # header
        label_date = tk.Label(frame_data_collection,
                                         text='Date')

        label_date.grid(row=3, column=0, columnspan=4,
                                   padx=(20, 0), pady=(10),
                                   sticky='w')

        label_time_period_header = tk.Label(frame_data_collection,
                              text='Time period')

        label_time_period_header.grid(row=3, column=5, columnspan=4,
                        padx=(20, 0),
                        sticky='w')

        # row 1
        user_date_1 = tk.StringVar()
        user_date_1_input = ttk.Entry(frame_data_collection, width=15, textvariable=user_date_1)
        user_date_1_input.grid(row=4, column=0, padx=(20, 0), pady=15, sticky='nswe')

        label_time_period_1 = tk.Label(frame_data_collection,
                                     text='Start of project')

        label_time_period_1.grid(row=4, column=5, columnspan=4,
                               padx=(20, 0),
                               sticky='w')

        button_upload_1 = tk.Button(frame_data_collection,
                                  text='Upload',
                                  width=10, height=1,
                                  command=self.show_project_start)

        button_upload_1.grid(row=4, column=11,
                           padx=(100, 0),
                           sticky='w')

        # row 2
        user_date_2 = tk.StringVar()
        user_date_2_input = ttk.Entry(frame_data_collection, width=15, textvariable=user_date_2)
        user_date_2_input.grid(row=5, column=0, padx=(20, 0), pady=15, sticky='nswe')

        label_time_period_2 = tk.Label(frame_data_collection,
                                       text='Halfway point of project')

        label_time_period_2.grid(row=5, column=5, columnspan=4,
                                 padx=(20, 0),
                                 sticky='w')

        button_upload_2 = tk.Button(frame_data_collection,
                                    text='Upload',
                                    width=10, height=1,
                                    command='')

        button_upload_2.grid(row=5, column=11,
                             padx=(100, 0),
                             sticky='w')
        # row 3
        user_date_3 = tk.StringVar()
        user_date_3_input = ttk.Entry(frame_data_collection, width=15, textvariable=user_date_3)
        user_date_3_input.grid(row=6, column=0, padx=(20, 0), pady=15, sticky='nswe')

        label_time_period_3 = tk.Label(frame_data_collection,
                                       text='End of project')

        label_time_period_3.grid(row=6, column=5, columnspan=4,
                                 padx=(20, 0),
                                 sticky='w')

        button_upload_3 = tk.Button(frame_data_collection,
                                    text='Upload',
                                    width=10, height=1,
                                    command='')

        button_upload_3.grid(row=6, column=11,
                             padx=(100, 0),
                             sticky='w')

        # row 4
        user_date_4 = tk.StringVar()
        user_date_4_input = ttk.Entry(frame_data_collection, width=15, textvariable=user_date_4)
        user_date_4_input.grid(row=7, column=0, padx=(20, 0), pady=15, sticky='nswe')

        label_time_period_4 = tk.Label(frame_data_collection,
                                       text='Year after end of project')

        label_time_period_4.grid(row=7, column=5, columnspan=4,
                                 padx=(20, 0),
                                 sticky='w')

        button_upload_4 = tk.Button(frame_data_collection,
                                    text='Upload',
                                    width=10, height=1,
                                    command='')

        button_upload_4.grid(row=7, column=11,
                             padx=(100, 0),
                             sticky='w')

    def show_project_start(self):

        if not self.start_project_window:

            self.start_project_window = tk.Toplevel()
            self.start_project_window.wm_title('Load data')

            width =  self.start_project_window.winfo_screenwidth()
            height =  self.start_project_window.winfo_screenheight()

            self.start_project_window.geometry('%sx%s' % (int(width-100), int(height)))

            self.start_project_window.protocol("WM_DELETE_WINDOW", lambda arg='start_project': self.hide_window(arg))



            frame_project_start= ttk.LabelFrame( self.start_project_window, text="2.2 Data collection",
                                                 width=1200, height=600)
            frame_project_start.grid_propagate(0)
            frame_project_start.grid(padx=(10, 0),
                                     sticky='nsew')

            label_project_header = tk.Label(frame_project_start,
                                           text='1: Start of project')

            label_project_header.grid(row=1, column=0, columnspan=4,
                                     padx=(20, 0), pady=(20),
                                     sticky='w')

            label_project_provider = tk.Label(frame_project_start,
                                            text='Project provider data (CSV file only)')

            label_project_provider.grid(row=2, column=0, columnspan=4,
                                      padx=(20, 0),
                                      sticky='w')

            # make object
            self.project_start = w.FileOpener(self)

            # convert to string var and set init text
            self.text_project_provider = tk.StringVar()
            self.text_project_provider.set("")

            # create label and place in gui
            self.project_label = tk.Label(frame_project_start,
                                          textvariable=self.text_project_provider).grid(row=4, column=0, sticky='w', pady=(0,20),
                                                                                    padx=(20, 0), columnspan=150)

            # create button with actions
            button_upload_1 = tk.Button(frame_project_start,
                                        text='Select',
                                        width=c.Size.button_width, height=c.Size.button_height,
                                        command=lambda: [self.project_start.get_file_path(),
                                                         self.text_project_provider.set(self.project_start.get_file_name()), self.focus_window(self.start_project_window)])

            # place upload button
            button_upload_1.grid(row=3, column=0,
                                 padx=(10, 0), pady=5,
                                 sticky='w')
            # place show button
            button_show_1 = tk.Button(frame_project_start,
                                      text='Show',
                                      width=c.Size.button_width, height=c.Size.button_height,
                                      command='')

            button_show_1.grid(row=3, column=1,
                               padx=(10, 0), pady=5,
                               sticky='w')


            # --------- 2.2 community leader

            self.community_leader = w.FileOpener(self)

            label_community_leader = tk.Label(frame_project_start,
                                              text='Community leader data (CSV file only)')

            label_community_leader.grid(row=5, column=0, columnspan=4, pady=5,
                                        padx=(20, 0),
                                        sticky='w')

            # convert to string var and set init text
            self.text_community_leader= tk.StringVar()
            self.text_community_leader.set("")

            # create label and place in gui
            self.community_label = tk.Label(frame_project_start,
                                          textvariable=self.text_community_leader).grid(row=7, column=0, sticky='w',
                                                                                        pady=(0, 20),
                                                                                        padx=(20, 0),
                                                                                        columnspan=150)

            # create button with actions
            button_upload_2 = tk.Button(frame_project_start,
                                        text='Select',
                                        width=c.Size.button_width, height=c.Size.button_height,
                                        command=lambda: [self.community_leader.get_file_path(),
                                                         self.text_community_leader.set(
                                                             self.community_leader.get_file_name())])

            # place upload button
            button_upload_2.grid(row=6, column=0,
                                 padx=(10, 0), pady=5,
                                 sticky='w')
            # place show button
            button_show_2 = tk.Button(frame_project_start,
                                      text='Show',
                                      width=c.Size.button_width, height=c.Size.button_height,
                                      command='')

            button_show_2.grid(row=6, column=1,
                               padx=(10, 0), pady=5,
                               sticky='w')

            # --------- 2.2 teacher

            self.teacher = w.FileOpener(self)

            label_teacher = tk.Label(frame_project_start,
                                              text='Teacher data (CSV file only)')

            label_teacher.grid(row=8, column=0, columnspan=4,
                                        padx=(20, 0),
                                        sticky='w')

            # convert to string var and set init text
            self.text_teacher= tk.StringVar()
            self.text_teacher.set("")

            # create label and place in gui
            self.teacher_label = tk.Label(frame_project_start,
                                            textvariable=self.text_teacher).grid(row=10, column=0, sticky='w',
                                                                                          pady=(0, 20),
                                                                                          padx=(20, 0), columnspan=150)

            # create button with actions
            button_upload_3 = tk.Button(frame_project_start,
                                        text='Select',
                                        width=c.Size.button_width, height=c.Size.button_height,
                                        command=lambda: [self.teacher.get_file_path(),
                                                         self.text_teacher.set(
                                                             self.teacher.get_file_name())])

            # place upload button
            button_upload_3.grid(row=9, column=0,
                                 padx=(10, 0), pady=5,
                                 sticky='w')
            # place show button
            button_show_3 = tk.Button(frame_project_start,
                                      text='Show',
                                      width=c.Size.button_width, height=c.Size.button_height,
                                      command='')

            button_show_3.grid(row=9, column=1,
                               padx=(10, 0), pady=5,
                               sticky='w')

            # --------- 2.2 student

            self.student = w.FileOpener(self)

            label_student= tk.Label(frame_project_start,
                                     text='Student data (CSV file only)')

            label_student.grid(row=11, column=0, columnspan=4,
                               padx=(20, 0),
                               sticky='w')

            # convert to string var and set init text
            self.text_student = tk.StringVar()
            self.text_student.set("")

            # create label and place in gui
            self.student_label = tk.Label(frame_project_start,
                                          textvariable=self.text_student).grid(row=13, column=0, sticky='w',
                                                                               pady=(0, 20),
                                                                               padx=(20, 0), columnspan=150)

            # create button with actions
            button_upload_4 = tk.Button(frame_project_start,
                                        text='Select',
                                        width=c.Size.button_width, height=c.Size.button_height,
                                        command=lambda: [self.student.get_file_path(),
                                                         self.text_student.set(
                                                             self.student.get_file_name())])

            # place upload button
            button_upload_4.grid(row=12, column=0,
                                 padx=(10, 0), pady=5,
                                 sticky='w')
            # place show button
            button_show_4 = tk.Button(frame_project_start,
                                      text='Show',
                                      width=c.Size.button_width, height=c.Size.button_height,
                                      command='')

            button_show_4.grid(row=12, column=1,
                               padx=(10, 0), pady=5,
                               sticky='w')

            # https://stackoverflow.com/questions/31926991/force-set-tkinter-window-to-always-have-focus/31927283#31927283
            # self.start_project_window.attributes("-topmost", True)


        else:
            self.start_project_window.deiconify()

    def hide_window(self, window):

        if window == "start_project":
            self.start_project_window.withdraw()

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

