
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from . import widgets as w
from . import constants as c


class ProjectPurposeScreen(tk.Frame):

    def __init__(self):
        tk.Frame.__init__(self)

        self.project_goal_selected = False
        self.goal_model_selected = False

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
                                    command= lambda: [select_goal_select_functions()])

        # place upload button
        button_upload_1.grid(row=2, column=0,
                             padx=(10, 0), pady=5,
                             sticky='w')

        def select_goal_select_functions():

            self.project_pdf.get_file_path()
            filename = self.project_pdf.return_file_name()

            if len(filename) > 10:
                self.text_project_pdf.set(filename)
                self.project_goal_selected = True
                status_message_project_txt.set("")
            else:
                self.project_goal_selected = False
                self.text_project_pdf.set('')

        # todo project_goals add validation (don't execute when no filepath is selected)

        status_message_project_txt = tk.StringVar()
        status_message_project_txt.set("")
        status_message_project_label = tk.Label(frame_project_goals,
                                                font='Helvetica 11', foreground='red',
                                                textvariable=status_message_project_txt).grid(row=4, column=0,
                                                                                              sticky='w',
                                                                                              padx=(20, 0),
                                                                                              columnspan=150)

        def select_goal_show_functions():
            if self.project_goal_selected:
                self.project_pdf.show_project_goals()
            else:
                status_message_project_txt.set("Select project goals first!")

        # place show button
        button_show_1 = tk.Button(frame_project_goals,
                                  text='Show',
                                  width=c.Size.button_width, height=c.Size.button_height,
                                  command=select_goal_show_functions)

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

        def goal_model_select_functions():
            self.goal_pdf.get_file_path()
            filename = self.goal_pdf.return_file_name()

            print('Filename length: -----', len(filename))

            if len(filename) > 10:
                self.text_goal_pdf.set(filename)
                status_message_project_model_txt.set("")
                self.goal_model_selected = True
            else:
                self.goal_model_selected = False
                self.text_goal_pdf.set('')


        def goal_model_show_functions():
            if self.goal_model_selected:
                self.goal_pdf.show_project_goals()
            else:
                status_message_project_model_txt.set("Select goal model first!")

        button_upload_2 = tk.Button(frame_goal_model,
                                    text='Select',
                                    width=c.Size.button_width, height=c.Size.button_height,
                                    command=lambda: [goal_model_select_functions()])

        button_upload_2.grid(row=2, column=0,
                           padx=(10, 0),
                           pady=5,
                           sticky='w')

        status_message_project_model_txt = tk.StringVar()
        status_message_project_model_txt.set("")
        tk.Label(frame_goal_model,
                 font='Helvetica 11', foreground='red',
                 textvariable=status_message_project_model_txt).grid(row=5, column=0, sticky='w', padx=(20, 0), columnspan=150)

        # todo goal_model add validation (don't execute when no filepath is selected)
        button_show_2 = tk.Button(frame_goal_model,
                                  text='Show',
                                  width=c.Size.button_width, height=c.Size.button_height,
                                  command=lambda: [goal_model_show_functions()])

        button_show_2.grid(row=2, column=1,
                         padx=(10, 0),
                         pady=2,
                         sticky='w')

        # -------------------------------------------------------------------------------------------

        frame_select_method_fragments = ttk.LabelFrame(self, text="1.3 Method Fragments",
                                          width=c.Size.label_frame_width, height=300)
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
                                  command=lambda : [self.method_fragment.show_selection_screen(),
                                                    self.method_fragment.send_status_message(show_status_message, show_status_message_metric_def)])

        button_upload_3.grid(row=3, column=0,
                           padx=(10, 0),
                           pady=2,
                           sticky='w')

        status_message_show_method_frags = ''
        status_message_add_metric_def = ''

        # todo turn status messages into a function
        def if_clicked(section):
            self.method_fragment.send_status_message(show_status_message, show_status_message_metric_def)

            if self.method_fragment.methode_frags_selected == False:
                show_status_message['text'] = 'Select method fragments first!'
                show_status_message_metric_def['text'] = 'Select method fragments first!'

            else:
                show_status_message['text'] = ''
                show_status_message_metric_def['text'] = ''

                if section == 'method_frag':
                    self.method_fragment.show_info_screen()
                else:
                    self.method_fragment.show_add_metric_definition_window()

        button_upload_4 = tk.Button(frame_select_method_fragments,
                                    text='Show',
                                    width=c.Size.button_width, height=c.Size.button_height,
                                    command=lambda: [if_clicked('method_frag')])

        button_upload_4.grid(row=3, column=1,
                             padx=(10, 0),
                             pady=2,
                             sticky='w')

        # ------------

        show_status_message = ttk.Label(frame_select_method_fragments,
                              font='Helvetica 11', foreground='red',
                              text=status_message_show_method_frags)

        show_status_message.grid(row=4, column=0,
                                columnspan=20,
                                padx=10, pady=(10),
                                sticky='w')

        label_add_definition = tk.Label(frame_select_method_fragments,
                                                   text='Add metric definition & set targets')

        label_add_definition.grid(row=5, column=0, columnspan=100,
                                             padx=(20, 0),
                                             sticky='w')

        button_upload_5 = tk.Button(frame_select_method_fragments,
                                    text='Add / Show',
                                    height=c.Size.button_height,
                                    command=lambda: [if_clicked('add_metrics')])

        button_upload_5.grid(row=6, column=0,
                             padx=(10, 0),
                             pady=2,
                             sticky='w')

        show_status_message_metric_def = ttk.Label(frame_select_method_fragments,
                                        font='Helvetica 11', foreground='red',
                                        text=status_message_add_metric_def)

        show_status_message_metric_def.grid(row=7, column=0,
                                 columnspan=20,
                                 padx=10, pady=(10),
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

        self.sampling_selected = False

        # --------- 2.1 Sampling strategy frame
        frame_sampling = ttk.LabelFrame(self, text="2.1 Sampling strategy",
                                                       width=1200, height=150)
        frame_sampling.grid_propagate(0)
        frame_sampling.grid(padx=(10, 0), sticky='nsew')

        label_sampling = tk.Label(frame_sampling,
                                  text='Determine sampling strategy')

        label_sampling.grid(row=1, column=0, columnspan=100,
                                             padx=(20, 0),
                                             sticky='w')

        # make object
        self.data_collection_pdf = w.FileOpener(self)

        # convert to string var and set init text
        self.text_sampling_pdf = tk.StringVar()
        self.text_sampling_pdf.set("")

        # create label and place in gui
        self.project_label = tk.Label(frame_sampling,
                                      textvariable=self.text_sampling_pdf).grid(row=3, column=0, sticky='w',
                                                                                padx=(20, 0), columnspan=150)

        # functions if valid
        def sampling_show_functions():
            if self.sampling_selected:
                self.data_collection_pdf.show_project_goals()

            else:
                self.text_sampling_pdf.set("Select sampling strategy first!")
                print('Select sampling strategy first!')

        status_message_txt = tk.StringVar()
        status_message_txt.set("")
        status_message_label = tk.Label(frame_sampling,
                                                font='Helvetica 11', foreground='red',
                                                textvariable=status_message_txt).grid(row=4, column=0,
                                                                                              sticky='w',
                                                                                              padx=(20, 0),
                                                                                              columnspan=150)

        # check if valid link
        def sampling_strategy_select_functions():
            self.data_collection_pdf.get_file_path()
            filename = self.data_collection_pdf.return_file_name()

            if len(filename) > 10:
                self.text_sampling_pdf.set(filename)
                status_message_txt.set("")
                self.sampling_selected = True
            else:
                self.sampling_selected = False
                self.text_sampling_pdf.set('')

        # create button with actions
        button_upload_1 = tk.Button(frame_sampling,
                                    text='Select',
                                    width=c.Size.button_width, height=c.Size.button_height,
                                    command=lambda: [sampling_strategy_select_functions()])

        # place upload button
        button_upload_1.grid(row=2, column=0,
                             padx=(10, 0), pady=5,
                             sticky='w')

        # todo sampling_strategy add validation (don't execute when no filepath is selected)
        # place show button
        button_show_1 = tk.Button(frame_sampling,
                                  text='Show',
                                  width=c.Size.button_width, height=c.Size.button_height,
                                  command=sampling_show_functions)

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

            # width =  self.start_project_window.winfo_screenwidth()
            # height =  self.start_project_window.winfo_screenheight()
            #
            # self.start_project_window.geometry('%sx%s' % (int(width-100), int(height)))

            # make notebook
            self.notebook_data_collection = ttk.Notebook(self.start_project_window)

            # make tabs
            self.tab_sop = ttk.Frame(self.start_project_window, width=1200, height=600)
            self.tab_sop.grid(row=0, column=0,
                                  padx=(10, 0),
                                  sticky='nsew')

            self.tab_hop = ttk.Frame(self.start_project_window, width=1200, height=600)
            self.tab_hop.grid(padx=(10, 0),
                                    sticky='nsew')

            self.tab_eop = ttk.Frame(self.start_project_window, width=1200, height=600)
            self.tab_eop.grid(padx=(10, 0),
                              sticky='nsew')

            self.tab_yap = ttk.Frame(self.start_project_window, width=1200, height=600)
            self.tab_yap.grid(padx=(10, 0),
                              sticky='nsew')

            # add tabs to notebook
            self.notebook_data_collection.add(self.tab_sop, text='1- Start of project')
            # self.notebook_summary.add(self.tab_metric_definition, text='Metric Definitions')
            self.notebook_data_collection.add(self.tab_hop, text='2- Halfway of project')
            self.notebook_data_collection.add(self.tab_eop, text='3- End of project')
            self.notebook_data_collection.add(self.tab_yap, text='4- Year after end of project')
            self.notebook_data_collection.grid(row=0, column=0, sticky='E', padx=5, pady=5, ipadx=5, ipady=5)

            self.start_project_window.protocol("WM_DELETE_WINDOW", lambda arg='start_project': self.hide_window(arg))

            # --------------------------------------

            # file_opener_object = FileOpener
            # text_sampling = label_name
            # status_message
            # file_selected = sampling_selected

            data_file_status_list = []

            time_period = ['sop', 'hop', 'eop', 'yap']
            targets = ['provider', 'leader', 'teacher', 'student']

            # fill data_file_status_list
            for period in time_period:
                for target in targets:
                    data_file_status_list.append({'time_period': period,
                                                  'target': target,
                                                  'status': False})

            def create_label(label_name, frame, row, column, color):
                tk.Label(frame,
                         font='Helvetica 11', foreground=color,
                         textvariable=label_name).grid(row=row, column=column,
                                                               sticky='w',
                                                               padx=(10, 0),
                                                               columnspan=150)

            # check if valid link
            def validate_path(file_name_label, status_message_label, file_opener_object, index):
                file_opener_object.get_file_path()
                filename = file_opener_object.return_file_name()

                if len(filename) > 10:
                    file_name_label.set(filename)
                    status_message_label.set("")
                    data_file_status_list[index]['status'] = True

                else:
                    data_file_status_list[index]['status'] = False
                    file_name_label.set('')

            # functions if valid
            def show_csv_file(file_selected, status_message_label, file_opener_object):
                if file_selected and file_opener_object.is_csv():
                    file_opener_object.show_project_goals()

                elif file_selected and file_opener_object.is_csv() == False :
                    status_message_label.set("File is not a CSV file!")

                else:
                    status_message_label.set("Select a CSV file first!")

            # --------------------------------------

            frame_project_start= ttk.LabelFrame( self.tab_sop, text="2.2 Data collection - 1: Start of project",
                                                 width=1200, height=600)
            frame_project_start.grid_propagate(0)
            frame_project_start.grid(padx=(10, 0),
                                     pady=(10,0),
                                     sticky='nsew')

            label_project_provider = tk.Label(frame_project_start,
                                              text='Project provider data (CSV file only)',
                                              font='Helvetica 11 bold')

            label_project_provider.grid(row=2, column=0, columnspan=4,
                                        padx=(10, 0),
                                        pady=(10,0),
                                        sticky='w')

            # make object
            self.provider_object_sop = w.FileOpener(self)

            # validate there is input and that is a csv file
            # sop = start of project

            # label for file_name provider
            provider_file_label_sop = tk.StringVar()
            provider_file_label_sop.set("")

            # place in GUI
            create_label(label_name= provider_file_label_sop,
                         frame=frame_project_start,
                         row=4,
                         column=0,
                         color='black')

            # label for status message provider
            provider_status_message_label_sop = tk.StringVar()
            provider_status_message_label_sop.set("")

            # place in GUI
            create_label(label_name= provider_status_message_label_sop,
                         frame=frame_project_start,
                         row=5,
                         column=0,
                         color='red')

            # check for period and target
            # 0 = sop - provider
            # 1 = sop - leader
            # 2 = sop - teacher
            # 3 = sop - student

            # print(data_file_status_list[0]['target'])

            # create button with actions
            button_upload_1 = tk.Button(frame_project_start,
                                        text='Select',
                                        width=c.Size.button_width, height=c.Size.button_height,
                                        command=lambda: [validate_path(file_name_label= provider_file_label_sop,
                                                                       status_message_label= provider_status_message_label_sop,
                                                                       file_opener_object= self.provider_object_sop,
                                                                       index= 0)
                                                         ])

            # place upload button
            button_upload_1.grid(row=3, column=0,
                                 padx=(10, 0), pady=5,
                                 sticky='w')
            # place show button
            button_show_1 = tk.Button(frame_project_start,
                                      text='Show',
                                      width=c.Size.button_width, height=c.Size.button_height,
                                      command=lambda: [show_csv_file(file_selected= data_file_status_list[0]['status'],
                                                                     status_message_label= provider_status_message_label_sop,
                                                                     file_opener_object= self.provider_object_sop)
                                      ])

            button_show_1.grid(row=3, column=1,
                               padx=(10, 0), pady=5,
                               sticky='w')


            # --------- 2.2 community leader

            label_community_leader = tk.Label(frame_project_start,
                                              text='Community leader data (CSV file only)',
                                              font='Helvetica 11 bold')

            label_community_leader.grid(row=6, column=0, columnspan=4,
                                        pady=(10),
                                        padx=(10, 0),
                                        sticky='w')

            # make object
            self.leader_object_sop = w.FileOpener(self)

            # validate there is input and that is a csv file
            # sop = start of project

            # label for file_name community leader
            leader_file_label_sop = tk.StringVar()
            leader_file_label_sop.set("")

            # place in GUI
            create_label(label_name=leader_file_label_sop,
                         frame=frame_project_start,
                         row=8,
                         column=0,
                         color='black')

            # label for status message community leader
            leader_status_message_label_sop = tk.StringVar()
            leader_status_message_label_sop.set("")

            # place in GUI
            create_label(label_name=leader_status_message_label_sop,
                         frame=frame_project_start,
                         row=9,
                         column=0,
                         color='red')

            # check for period and target
            # 0 = sop - provider
            # 1 = sop - leader
            # 2 = sop - teacher
            # 3 = sop - student

            # create button with actions
            button_upload_2 = tk.Button(frame_project_start,
                                        text='Select',
                                        width=c.Size.button_width, height=c.Size.button_height,
                                        command=lambda: [validate_path(file_name_label=leader_file_label_sop,
                                                                       status_message_label=leader_status_message_label_sop,
                                                                       file_opener_object=self.leader_object_sop,
                                                                       index=1)
                                                         ])

            # place upload button
            button_upload_2.grid(row=7, column=0,
                                 padx=(10, 0), pady=5,
                                 sticky='w')
            # place show button
            button_show_2 = tk.Button(frame_project_start,
                                      text='Show',
                                      width=c.Size.button_width, height=c.Size.button_height,
                                      command=lambda: [show_csv_file(file_selected=data_file_status_list[1]['status'],
                                                                     status_message_label=leader_status_message_label_sop,
                                                                     file_opener_object=self.leader_object_sop)
                                                       ])

            button_show_2.grid(row=7, column=1,
                               padx=(10, 0), pady=5,
                               sticky='w')

            # --------- 2.2 teacher



            label_teacher = tk.Label(frame_project_start,
                                     text='Teacher data (CSV file only)',
                                     font='Helvetica 11 bold')

            label_teacher.grid(row=10,
                               column=0, columnspan=4,
                               padx=(20, 0),
                               pady=10,
                               sticky='w')

            # make object
            self.teacher_object_sop = w.FileOpener(self)

            # convert to string var and set init text
            self.text_teacher= tk.StringVar()
            self.text_teacher.set("")

            # create label and place in gui
            self.teacher_label = tk.Label(frame_project_start,
                                            textvariable=self.text_teacher).grid(row=13, column=0, sticky='w',
                                                                                          pady=(0, 20),
                                                                                          padx=(20, 0), columnspan=150)

            # create button with actions
            button_upload_3 = tk.Button(frame_project_start,
                                        text='Select',
                                        width=c.Size.button_width, height=c.Size.button_height,
                                        command=lambda: [self.teacher.get_file_path(),
                                                         self.text_teacher.set(
                                                             self.teacher.return_file_name())])

            # place upload button
            button_upload_3.grid(row=11, column=0,
                                 padx=(10, 0), pady=5,
                                 sticky='w')
            # place show button
            button_show_3 = tk.Button(frame_project_start,
                                      text='Show',
                                      width=c.Size.button_width, height=c.Size.button_height,
                                      command='')

            button_show_3.grid(row=11, column=1,
                               padx=(10, 0), pady=5,
                               sticky='w')

            # --------- 2.2 student

            self.student = w.FileOpener(self)

            label_student= tk.Label(frame_project_start,
                                    text='Student data (CSV file only)',
                                    font='Helvetica 11 bold')

            label_student.grid(row=14, column=0, columnspan=4,
                               padx=(20, 0),
                               sticky='w')

            # convert to string var and set init text
            self.text_student = tk.StringVar()
            self.text_student.set("")

            # create label and place in gui
            self.student_label = tk.Label(frame_project_start,
                                          textvariable=self.text_student).grid(row=17, column=0, sticky='w',
                                                                               pady=(0, 20),
                                                                               padx=(20, 0), columnspan=150)

            # create button with actions
            button_upload_4 = tk.Button(frame_project_start,
                                        text='Select',
                                        width=c.Size.button_width, height=c.Size.button_height,
                                        command=lambda: [self.student.get_file_path(),
                                                         self.text_student.set(
                                                             self.student.return_file_name())])

            # place upload button
            button_upload_4.grid(row=15, column=0,
                                 padx=(10, 0), pady=5,
                                 sticky='w')
            # place show button
            button_show_4 = tk.Button(frame_project_start,
                                      text='Show',
                                      width=c.Size.button_width, height=c.Size.button_height,
                                      command='')

            button_show_4.grid(row=15, column=1,
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
        frame_project_goals = ttk.LabelFrame(self, text="")
        frame_project_goals.pack(fill="both", expand="yes")

        label = tk.Label(frame_project_goals, text='Data analysis content')
        label.pack()


class ImpactAssessmentScreen(tk.Frame):

    def __init__(self):
        tk.Frame.__init__(self)
        tk.Label(self, text='Impact assessment content').pack()

