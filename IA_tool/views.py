
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from . import widgets as w
from . import constants as c
import os
import webbrowser
from tkinter.scrolledtext import ScrolledText


class ProjectPurposeScreen(tk.Frame):


    def __init__(self):
        tk.Frame.__init__(self)

        self.project_goal_selected = False
        self.goal_model_selected = False

        self.create_doc()
        self.create_project_goals_section()
        self.create_goal_model_section()
        self.create_method_fragment_section()

    def create_doc(self):
        # load in documentation
        dirname = os.getcwd()
        filename_docs_project_goals = os.path.join(dirname, 'docs', 'project_goals.pdf')
        filename_docs_goal_model = os.path.join(dirname, 'docs', 'goal_model.pdf')
        filename_docs_method_frag = os.path.join(dirname, 'docs', 'method_fragments.pdf')

        frame_project_docs = ttk.LabelFrame(self, text="View help documentation",
                                            width=c.Size.label_frame_width,
                                            height=80,
                                            style="Doc.TLabelframe")

        frame_project_docs.grid_propagate(0)
        frame_project_docs.grid(padx=(10, 0),
                                pady=(10, 0),
                                sticky='nsew')

        tk.Button(frame_project_docs,
                  text='1.1 Project Goals',
                  width=20, height=c.Size.button_height,
                  command=lambda: [webbrowser.open(filename_docs_project_goals)]).grid(row=0, column=0,
                                                                                       padx=(10, 0), pady=5,
                                                                                       sticky='w')

        tk.Button(frame_project_docs,
                  text='1.2 Goal Model',
                  width=20, height=c.Size.button_height,
                  command=lambda: [webbrowser.open(filename_docs_goal_model)]).grid(row=0, column=1,
                                                                                    padx=(10, 0), pady=5,
                                                                                    sticky='w')
        tk.Button(frame_project_docs,
                  text='1.3 Method Fragments',
                  width=20, height=c.Size.button_height,
                  command=lambda: [webbrowser.open(filename_docs_method_frag)]).grid(row=0, column=2,
                                                                                     padx=(10, 0), pady=5,
                                                                                     sticky='w')

    def create_project_goals_section(self):
        frame_project_goals = ttk.LabelFrame(self, text="1.1 Project Goals",
                                             width=c.Size.label_frame_width, height=c.Size.label_frame_height)
        frame_project_goals.grid_propagate(0)
        frame_project_goals.grid(padx=(10, 0),
                                 pady=(10, 0),
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
                                      textvariable=self.text_project_pdf).grid(row=3, column=0, sticky='w',
                                                                               padx=(20, 0), columnspan=150)

        # create button with actions
        button_upload_1 = tk.Button(frame_project_goals,
                                    text='Select',
                                    width=c.Size.button_width, height=c.Size.button_height,
                                    command=lambda: [select_goal_select_functions()])

        # place upload button
        button_upload_1.grid(row=2, column=0,
                             padx=(10, 0), pady=5,
                             sticky='w')

        def select_goal_select_functions():

            file_path = self.project_pdf.get_file_path()
            filename = self.project_pdf.return_file_name()

            if file_path:
                self.text_project_pdf.set(filename)
                self.project_goal_selected = True
                self.status_message_project_txt.set("")
                self.dict_paths.update_user_doc_path_dict('project_goals', file_path)

            else:
                self.project_goal_selected = False
                self.text_project_pdf.set('')
                self.dict_paths.update_user_doc_path_dict('project_goals', '')

        self.status_message_project_txt = tk.StringVar()
        self.status_message_project_txt.set("")
        status_message_project_label = tk.Label(frame_project_goals,
                                                font='Helvetica 11', foreground='red',
                                                textvariable=self.status_message_project_txt).grid(row=4, column=0,
                                                                                              sticky='w',
                                                                                              padx=(20, 0),
                                                                                              columnspan=150)

        def select_goal_show_functions():
            if self.project_goal_selected:
                self.project_pdf.show_project_goals()
            else:
                self.status_message_project_txt.set("Select project goals first!")

        # place show button
        button_show_1 = tk.Button(frame_project_goals,
                                  text='Show',
                                  width=c.Size.button_width, height=c.Size.button_height,
                                  command=select_goal_show_functions)

        button_show_1.grid(row=2, column=1,
                           padx=(10, 0), pady=5,
                           sticky='w')

    def create_goal_model_section(self):
        frame_goal_model = ttk.LabelFrame(self, text="1.2 Goal Model",
                                          width=c.Size.label_frame_width, height=c.Size.label_frame_height)
        frame_goal_model.grid_propagate(0)
        frame_goal_model.grid(padx=(10, 0),
                              pady=(10, 0),
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
                                            textvariable=self.text_goal_pdf).grid(row=4, column=0, sticky='w',
                                                                                  padx=(20, 0), columnspan=150)

        def goal_model_select_functions():
            file_path = self.goal_pdf.get_file_path()
            filename = self.goal_pdf.return_file_name()

            if file_path:
                self.text_goal_pdf.set(filename)
                status_message_project_model_txt.set("")
                self.goal_model_selected = True
                self.dict_paths.update_user_doc_path_dict('goal_model', file_path)
            else:
                self.goal_model_selected = False
                self.text_goal_pdf.set('')
                self.dict_paths.update_user_doc_path_dict('goal_model', '')

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
                 textvariable=status_message_project_model_txt).grid(row=5, column=0, sticky='w', padx=(20, 0),
                                                                     columnspan=150)

        button_show_2 = tk.Button(frame_goal_model,
                                  text='Show',
                                  width=c.Size.button_width, height=c.Size.button_height,
                                  command=lambda: [goal_model_show_functions()])

        button_show_2.grid(row=2, column=1,
                           padx=(10, 0),
                           pady=2,
                           sticky='w')

    def create_method_fragment_section(self):
        frame_select_method_fragments = ttk.LabelFrame(self, text="1.3 Method Fragments",
                                                       width=c.Size.label_frame_width, height=250)
        frame_select_method_fragments.grid_propagate(0)
        frame_select_method_fragments.grid(padx=(10, 0),
                                           pady=(10, 0),
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
                                    command=lambda: [self.method_fragment.show_selection_screen(),
                                                     self.method_fragment.send_status_message(show_status_message,
                                                                                              show_status_message_metric_def)])

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

    def save_data(self):
        self.save_file_object.get_project_purpose(self.dict_paths.user_doc_file_paths,
                                                  self.method_fragment.checkbox_list,
                                                  self.method_fragment.methode_frags_selected)

    def sendFrame(self, frame):
        self.method_fragment.retrieve_frame(frame)

    def getProjectPdfPath(self):
        self.project_pdf_file_path = filedialog.askopenfilename()

    def send_data_object(self, data):
        self.data_object = data
        self.method_fragment.get_data_object(self.data_object)

    def send_dict_paths(self, dict):
        self.dict_paths = dict

    def send_save_file_object(self, data):
        self.save_file_object = data

    def restore_from_save_file(self):

        # if path to project model was saved
        if self.save_file_object.data['project_goals_path']:
            self.project_goal_selected = True
            self.text_project_pdf.set(self.project_pdf.clean_file_name(self.save_file_object.data['project_goals_path']))

        # if path to goal model was saved
        if self.save_file_object.data['goal_model_path']:
            self.goal_model_selected = True
            self.text_goal_pdf.set(self.project_pdf.clean_file_name(self.save_file_object.data['goal_model_path']))

        # if method fragments were saved

        # checkboxes
        if self.save_file_object.data['selected_method_fragments']:

            self.method_fragment.show_selection_screen()
            self.method_fragment.selection_window.withdraw()

            sql = 'select method_fragment_name from method_fragment'
            retrieve_sql = self.data_object.query_no_par(sql)

            for item in self.save_file_object.data['selected_method_fragments']:
                self.method_fragment.checkbox[item].select()

            self.method_fragment.methode_frags_selected = True
            self.method_fragment.checkbox_list = self.save_file_object.data['selected_method_fragments']

            self.method_fragment.show_info_screen()
            self.method_fragment.delete_frame(self.method_fragment.scrollable_metric_frame)
            self.method_fragment.delete_frame(self.method_fragment.add_metrics_frame)
            self.method_fragment.delete_frame(self.method_fragment.remove_frame)
            self.method_fragment.add_metric()
            self.method_fragment.show_summary_metrics()
            self.method_fragment.info_window.withdraw()
















class DataCollectionScreen(tk.Frame):

    def __init__(self):
        tk.Frame.__init__(self)

        global start_project_window
        self.start_project_window = None

        self.data_collection_window = self

        self.sampling_selected = False

        dirname = os.getcwd()
        filename_docs_sampling_strategy = os.path.join(dirname, 'docs', 'sampling_strategy.pdf')

        frame_project_docs = ttk.LabelFrame(self, text="View help documentation",
                                            width=c.Size.label_frame_width,
                                            height=80,
                                            style="Doc.TLabelframe")

        frame_project_docs.grid_propagate(0)
        frame_project_docs.grid(padx=(10, 0),
                                pady=(10, 0),
                                sticky='nsew')

        tk.Button(frame_project_docs,
                  text='2.1 Sampling Strategy',
                  width=20, height=c.Size.button_height,
                  command=lambda: [webbrowser.open(filename_docs_sampling_strategy)]).grid(row=0, column=0,
                                   padx=(10, 0), pady=5,
                                   sticky='w')

        tk.Button(frame_project_docs,
                  text='2.2 Data Collection',
                  width=20, height=c.Size.button_height,
                  command="").grid(row=0, column=1,
                                   padx=(10, 0), pady=5,
                                   sticky='w')

        # --------- 2.1 Sampling strategy frame
        frame_sampling = ttk.LabelFrame(self, text="2.1 Sampling strategy",
                                                       width=1200, height=150)
        frame_sampling.grid_propagate(0)
        frame_sampling.grid(padx=(10, 0),
                            pady=(10, 0),
                            sticky='nsew')

        label_sampling = tk.Label(frame_sampling,
                                  text='Determine sampling strategy')

        label_sampling.grid(row=1, column=0, columnspan=100,
                                             padx=(20, 0),
                                             sticky='w')

        # make file opener object
        self.data_collection_pdf = w.FileOpener(self)

        # make data collection object
        self.data_collection = w.DataCollection(self)

        # convert to string var and set init text
        self.text_sampling_pdf = tk.StringVar()
        self.text_sampling_pdf.set("")

        # create label and place in gui
        self.project_label = tk.Label(frame_sampling,
                                      textvariable=self.text_sampling_pdf,
                                      foreground = "black")

        self.project_label.grid(row=3, column=0,
                                sticky='w',
                                padx=(20, 0),
                                columnspan=150)

        # functions if valid
        def sampling_show_functions():
            if self.sampling_selected:
                self.project_label["foreground"] = "black"
                self.data_collection_pdf.show_project_goals()

            else:
                self.status_message_label.config(foreground="red")
                self.status_message_txt.set("Select sampling strategy first!")

        self.status_message_txt = tk.StringVar()
        self.status_message_txt.set("")
        self.status_message_label = tk.Label(frame_sampling,
                                                font='Helvetica 11', foreground='red',
                                                textvariable=self.status_message_txt)

        self.status_message_label.grid(row=4, column=0,
                                  sticky='w',
                                  padx=(20, 0),
                                  columnspan=150)

        # check if valid link
        def sampling_strategy_select_functions():
            file_path = self.data_collection_pdf.get_file_path()
            filename = self.data_collection_pdf.return_file_name()

            if file_path:
                self.text_sampling_pdf.set(filename)
                self.status_message_txt.set("")
                self.sampling_selected = True
                self.dict_paths.update_user_doc_path_dict('sampling_strategy', file_path)
            else:
                self.sampling_selected = False
                self.text_sampling_pdf.set('')
                self.dict_paths.update_user_doc_path_dict('sampling_strategy', '')


        # create button with actions
        button_upload_1 = tk.Button(frame_sampling,
                                    text='Select',
                                    width=c.Size.button_width, height=c.Size.button_height,
                                    command=lambda: [sampling_strategy_select_functions()])

        # place upload button
        button_upload_1.grid(row=2, column=0,
                             padx=(10, 0), pady=5,
                             sticky='w')

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
                                        width=1200, height=400)
        frame_data_collection.grid_propagate(0)
        frame_data_collection.grid(padx=(10, 0),
                                   pady=(10, 0),
                            sticky='nsew')

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
        self.user_date_1 = tk.StringVar()
        self.user_date_1_input = ttk.Entry(frame_data_collection, width=15, textvariable=self.user_date_1)
        self.user_date_1_input.grid(row=4, column=0, padx=(20, 0), pady=15, sticky='nswe')

        label_time_period_1 = tk.Label(frame_data_collection,
                                     text='Start of project')

        label_time_period_1.grid(row=4, column=5, columnspan=4,
                               padx=(20, 0),
                               sticky='w')

        button_upload_1 = tk.Button(frame_data_collection,
                                  text='Upload',
                                  width=10, height=1,
                                  command=lambda : [self.show_project_start(), self.notebook_data_collection.select(0)])

        button_upload_1.grid(row=4, column=11,
                           padx=(100, 0),
                           sticky='w')

        # row 2
        self.user_date_2 = tk.StringVar()
        self.user_date_2_input = ttk.Entry(frame_data_collection, width=15, textvariable=self.user_date_2)
        self.user_date_2_input.grid(row=5, column=0, padx=(20, 0), pady=15, sticky='nswe')

        label_time_period_2 = tk.Label(frame_data_collection,
                                       text='Halfway point of project')

        label_time_period_2.grid(row=5, column=5, columnspan=4,
                                 padx=(20, 0),
                                 sticky='w')

        button_upload_2 = tk.Button(frame_data_collection,
                                    text='Upload',
                                    width=10, height=1,
                                    command=lambda : [self.show_project_start(), self.notebook_data_collection.select(1)])

        button_upload_2.grid(row=5, column=11,
                             padx=(100, 0),
                             sticky='w')
        # row 3
        self.user_date_3 = tk.StringVar()
        self.user_date_3_input = ttk.Entry(frame_data_collection, width=15, textvariable=self.user_date_3)
        self.user_date_3_input.grid(row=6, column=0, padx=(20, 0), pady=15, sticky='nswe')

        label_time_period_3 = tk.Label(frame_data_collection,
                                       text='End of project')

        label_time_period_3.grid(row=6, column=5, columnspan=4,
                                 padx=(20, 0),
                                 sticky='w')

        button_upload_3 = tk.Button(frame_data_collection,
                                    text='Upload',
                                    width=10, height=1,
                                    command=lambda : [self.show_project_start(), self.notebook_data_collection.select(2)])

        button_upload_3.grid(row=6, column=11,
                             padx=(100, 0),
                             sticky='w')

        # row 4
        self.user_date_4 = tk.StringVar()
        self.user_date_4_input = ttk.Entry(frame_data_collection, width=15, textvariable=self.user_date_4)
        self.user_date_4_input.grid(row=7, column=0, padx=(20, 0), pady=15, sticky='nswe')

        label_time_period_4 = tk.Label(frame_data_collection,
                                       text='Year after end of project')

        label_time_period_4.grid(row=7, column=5, columnspan=4,
                                 padx=(20, 0),
                                 sticky='w')

        button_upload_4 = tk.Button(frame_data_collection,
                                    text='Upload',
                                    width=10, height=1,
                                    command=lambda : [self.show_project_start(), self.notebook_data_collection.select(3)])

        button_upload_4.grid(row=7, column=11,
                             padx=(100, 0),
                             sticky='w')

        self.user_dates_objects =   [self.user_date_1,
                                    self.user_date_2,
                                    self.user_date_3,
                                    self.user_date_4]

    def restore_from_save_file(self):

        self.user_date_1.set(self.save_file_object.data['date_sop'])
        self.user_date_2.set(self.save_file_object.data['date_hop'])
        self.user_date_3.set(self.save_file_object.data['date_eop'])
        self.user_date_4.set(self.save_file_object.data['date_yap'])

        # if path to sampling strategy was saved
        if self.save_file_object.data['sampling_strategy_path']:
            self.sampling_selected = True
            self.text_sampling_pdf.set(self.data_collection_pdf.clean_file_name(self.save_file_object.data['sampling_strategy_path']))

        # if paths to loading in data were saved
        if self.save_file_object.data['data_collection_paths']:

            # make  toplevel than hide
            self.show_project_start()
            self.start_project_window.withdraw()

            self.dict_paths.dc_file_paths = self.save_file_object.data['data_collection_paths']
            self.data_file_status_list = self.save_file_object.data['data_file_status_list']

            # set paths back
            self.provider_file_label_sop.set(self.data_collection_pdf.clean_file_name(self.dict_paths.dc_file_paths['sop_provider']))
            self.leader_file_label_sop.set(self.data_collection_pdf.clean_file_name(self.dict_paths.dc_file_paths['sop_leader']))
            self.teacher_file_label_sop.set(self.data_collection_pdf.clean_file_name(self.dict_paths.dc_file_paths['sop_teacher']))
            self.student_file_label_sop.set(self.data_collection_pdf.clean_file_name(self.dict_paths.dc_file_paths['sop_student']))

            self.provider_file_label_hop.set(self.data_collection_pdf.clean_file_name(self.dict_paths.dc_file_paths['hop_provider']))
            self.leader_file_label_hop.set(self.data_collection_pdf.clean_file_name(self.dict_paths.dc_file_paths['hop_leader']))
            self.teacher_file_label_hop.set(self.data_collection_pdf.clean_file_name(self.dict_paths.dc_file_paths['hop_teacher']))
            self.student_file_label_hop.set(self.data_collection_pdf.clean_file_name(self.dict_paths.dc_file_paths['hop_student']))

            self.provider_file_label_eop.set(self.data_collection_pdf.clean_file_name(self.dict_paths.dc_file_paths['eop_provider']))
            self.leader_file_label_eop.set(self.data_collection_pdf.clean_file_name(self.dict_paths.dc_file_paths['eop_leader']))
            self.teacher_file_label_eop.set(self.data_collection_pdf.clean_file_name(self.dict_paths.dc_file_paths['eop_teacher']))
            self.student_file_label_eop.set(self.data_collection_pdf.clean_file_name(self.dict_paths.dc_file_paths['eop_student']))

            self.provider_file_label_yap.set(self.data_collection_pdf.clean_file_name(self.dict_paths.dc_file_paths['yap_provider']))
            self.leader_file_label_yap.set(self.data_collection_pdf.clean_file_name(self.dict_paths.dc_file_paths['yap_leader']))
            self.teacher_file_label_yap.set(self.data_collection_pdf.clean_file_name(self.dict_paths.dc_file_paths['yap_teacher']))
            self.student_file_label_yap.set(self.data_collection_pdf.clean_file_name(self.dict_paths.dc_file_paths['yap_student']))

            self.provider_object_sop.file_path = self.dict_paths.dc_file_paths['sop_provider']
            self.provider_object_hop.file_path = self.dict_paths.dc_file_paths['hop_provider']
            self.provider_object_eop.file_path = self.dict_paths.dc_file_paths['eop_provider']
            self.provider_object_yap.file_path = self.dict_paths.dc_file_paths['yap_provider']

            self.leader_object_sop.file_path = self.dict_paths.dc_file_paths['sop_leader']
            self.leader_object_hop.file_path = self.dict_paths.dc_file_paths['hop_leader']
            self.leader_object_eop.file_path = self.dict_paths.dc_file_paths['eop_leader']
            self.leader_object_yap.file_path = self.dict_paths.dc_file_paths['yap_leader']

            self.teacher_object_sop.file_path = self.dict_paths.dc_file_paths['sop_teacher']
            self.teacher_object_hop.file_path = self.dict_paths.dc_file_paths['hop_teacher']
            self.teacher_object_eop.file_path = self.dict_paths.dc_file_paths['eop_teacher']
            self.teacher_object_yap.file_path = self.dict_paths.dc_file_paths['yap_teacher']

            self.student_object_sop.file_path = self.dict_paths.dc_file_paths['sop_student']
            self.student_object_hop.file_path = self.dict_paths.dc_file_paths['hop_student']
            self.student_object_eop.file_path = self.dict_paths.dc_file_paths['eop_student']
            self.student_object_yap.file_path = self.dict_paths.dc_file_paths['yap_student']


    def send_dict_paths(self, dict):
        self.dict_paths = dict
        self.data_collection.get_dict_paths(self.dict_paths)

    def send_save_file_object(self, data):
        self.save_file_object = data

    # 1234
    def save_data(self):

        self.user_dates = {'date_sop' : self.user_dates_objects[0].get(),
                           'date_hop' : self.user_dates_objects[1].get(),
                           'date_eop' : self.user_dates_objects[2].get(),
                           'date_yap' : self.user_dates_objects[3].get()}

        try:
            self.save_file_object.get_data_collection(self.user_dates, self.dict_paths.dc_file_paths, self.data_file_status_list)

        except:
            self.data_file_status_list = []
            self.save_file_object.get_data_collection(self.user_dates, self.dict_paths.dc_file_paths, self.data_file_status_list)

    def reset_status_messages(self):
        self.provider_status_message_label_sop.set('')
        self.provider_status_message_label_hop.set('')
        self.provider_status_message_label_eop.set('')
        self.provider_status_message_label_yap.set('')

        self.leader_status_message_label_sop.set('')
        self.leader_status_message_label_hop.set('')
        self.leader_status_message_label_eop.set('')
        self.leader_status_message_label_yap.set('')

        self.teacher_status_message_label_sop.set('')
        self.teacher_status_message_label_hop.set('')
        self.teacher_status_message_label_eop.set('')
        self.teacher_status_message_label_yap.set('')

        self.student_status_message_label_sop.set('')
        self.student_status_message_label_hop.set('')
        self.student_status_message_label_eop.set('')
        self.student_status_message_label_yap.set('')

    def show_project_start(self):
        # TODO split into multiple functions (sop, hop, eop, yap)
        # TODO adjust buttons accordingly to function
        # TODO figure out where to place notebook

        self.data_file_status_list = []

        time_period = ['sop', 'hop', 'eop', 'yap']
        targets = ['provider', 'leader', 'teacher', 'student']

        # fill data_file_status_list
        for period in time_period:
            for target in targets:
                self.data_file_status_list.append({'time_period': period,
                                                   'target': target,
                                                   'status': False})

        # if there is not already a 'start of project' window
        if not self.start_project_window:

            # create pop up window
            self.start_project_window = tk.Toplevel()
            self.start_project_window.wm_title('Load in survey data')

            width = 1280
            height = 600
            position_left = 150
            position_right = 150

            self.start_project_window.geometry("{}x{}+{}+{}".format(width, height, position_left, position_right))

            # set size window fixed
            self.start_project_window.resizable(0, 0)

            width_tab = 1280
            height_tab = 600


            # width =  self.start_project_window.winfo_screenwidth()
            # height =  self.start_project_window.winfo_screenheight()
            #
            # self.start_project_window.geometry('%sx%s' % (int(width-100), int(height)))

            #------------------------- Notebook
            # make notebook
            self.notebook_data_collection = ttk.Notebook(self.start_project_window)

            # make tabs
            self.tab_sop = ttk.Frame(self.start_project_window, width=width_tab, height=height_tab)
            self.tab_sop.grid(row=0, column=0,
                                  padx=(10, 0),
                                  sticky='nsew')

            self.tab_hop = ttk.Frame(self.start_project_window, width=width_tab, height=height_tab)
            self.tab_hop.grid(padx=(10, 0),
                                    sticky='nsew')

            self.tab_eop = ttk.Frame(self.start_project_window, width=width_tab, height=height_tab)
            self.tab_eop.grid(padx=(10, 0),
                              sticky='nsew')

            self.tab_yap = ttk.Frame(self.start_project_window, width=width_tab, height=height_tab)
            self.tab_yap.grid(padx=(10, 0),
                              sticky='nsew')

            # add tabs to notebook
            self.notebook_data_collection.add(self.tab_sop, text='1- Start of project')
            self.notebook_data_collection.add(self.tab_hop, text='2- Halfway of project')
            self.notebook_data_collection.add(self.tab_eop, text='3- End of project')
            self.notebook_data_collection.add(self.tab_yap, text='4- Year after end of project')
            self.notebook_data_collection.grid(row=0, column=0, sticky='E', padx=5, pady=5, ipadx=5, ipady=5)

            # hide window if closed
            self.start_project_window.protocol("WM_DELETE_WINDOW", lambda arg='start_project': self.hide_window(arg))

            #------------------------- functions for validation and label creation
            self.data_file_status_list = []

            time_period = ['sop', 'hop', 'eop', 'yap']
            targets = ['provider', 'leader', 'teacher', 'student']

            targets_with_period = ['sop_provider',
                                   'sop_leader',
                                   'sop_teacher',
                                   'sop_student',

                                   'hop_provider',
                                   'hop_leader',
                                   'hop_teacher',
                                   'hop_student',

                                   'eop_provider',
                                   'eop_leader',
                                   'eop_teacher',
                                   'eop_student',

                                   'yap_provider',
                                   'yap_leader',
                                   'yap_teacher',
                                   'yap_student'
                                   ]

            # fill data_file_status_list
            for period in time_period:
                for target in targets:
                    self.data_file_status_list.append({'time_period': period,
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
            # TODO change validation file paths first tab
            def validate_path(file_name_label, status_message_label, file_opener_object, index, status_list):

                print('status_list: ',status_list)

                self.start_project_window.attributes("-topmost", False)
                file_path = file_opener_object.get_file_path_csv()
                filename = file_opener_object.return_file_name()

                # check if a file is selected
                if file_path:

                    file_name_label.set(filename)
                    status_message_label.set('')
                    status_list[index]['status'] = True

                    self.dict_paths.update_dc_path_dict(targets_with_period, index, file_opener_object.file_path)

                        # print('----')
                        # print('target: ', targets_with_period[index])
                        # print('path: ', file_opener_object.file_path)
                        # print('----')

                # if no file is selected
                else:
                    file_name_label.set('Filename: ')
                    self.dict_paths.update_dc_path_dict(targets_with_period, index, '')

                    # print('----')
                    # print('target: ', targets_with_period[index])
                    # print('path: ', file_opener_object.file_path)
                    # print('----')

                self.start_project_window.attributes("-topmost", True)

            # functions if valid
            def show_csv_file(file_selected, status_message_label, file_opener_object):

                if file_selected and file_opener_object.is_csv():
                    file_opener_object.show_project_goals()
                else:
                    status_message_label.set("Select a file first!")

            #------------------------- Data collection: Start of project (SOP) Frame

            frame_project_sop= ttk.LabelFrame( self.tab_sop, text="2.2 Data collection - 1: Start of project",
                                                 width=1200, height=700)
            frame_project_sop.grid_propagate(0)
            frame_project_sop.grid(padx=(10, 0),
                                     pady=(10,0),
                                     sticky='nsew')

            # ------------------------- SOP

            # ------------------------- SOP: Project provider

            tk.Label(frame_project_sop,
                     text='Project provider data (CSV file only)',
                     font='Helvetica 11 bold').grid(row=2, column=0, columnspan=4,
                                                    padx=(10, 0),
                                                    pady=(10, 0),
                                                    sticky='w')

            # make FileOpener object
            self.provider_object_sop = w.FileOpener(self)

            # label for file_name provider (to store file path)
            self.provider_file_label_sop = tk.StringVar()
            self.provider_file_label_sop.set("Filename: ")

            # place in GUI
            create_label(label_name= self.provider_file_label_sop,
                         frame=frame_project_sop,
                         row=4,
                         column=0,
                         color='black')

            # label for status message provider
            self.provider_status_message_label_sop = tk.StringVar()
            self.provider_status_message_label_sop.set("")

            # place in GUI
            create_label(label_name= self.provider_status_message_label_sop,
                         frame=frame_project_sop,
                         row=5,
                         column=0,
                         color='red')

            # check for period and target
            # 0 = sop - provider
            # 1 = sop - leader
            # 2 = sop - teacher
            # 3 = sop - student
            # print(data_file_status_list[0]['target'])

            print('self.data_file_status_list 1234: ', self.data_file_status_list)

            # create and place 'select' button with actions
            tk.Button(frame_project_sop,
                                        text='Select',
                                        width=c.Size.button_width, height=c.Size.button_height,
                                        command=lambda: [validate_path(file_name_label= self.provider_file_label_sop,
                                                                       status_message_label= self.provider_status_message_label_sop,
                                                                       file_opener_object= self.provider_object_sop,
                                                                       index=0,
                                                                       status_list=self.data_file_status_list)
                                                         ] ).grid(row=3, column=0,
                                                                 padx=(10, 0), pady=5,
                                                                 sticky='w')

            # create and place 'show' button with actions
            tk.Button(frame_project_sop,
                                      text='Show',
                                      width=c.Size.button_width, height=c.Size.button_height,
                                      command=lambda: [show_csv_file(file_selected= self.data_file_status_list[0]['status'],
                                                                     status_message_label= self.provider_status_message_label_sop,
                                                                     file_opener_object= self.provider_object_sop)
                                      ]).grid(row=3, column=1,
                                              padx=(10, 0), pady=5,
                                              sticky='w')

            #------------------------- SOP: Community leader

            tk.Label(frame_project_sop,
                     text='Community leader data (CSV file only)',
                     font='Helvetica 11 bold').grid(row=6, column=0, columnspan=4,
                                                    pady=(10), padx=(10, 0),
                                                    sticky='w')

            # make FileOpener object
            self.leader_object_sop = w.FileOpener(self)

            # label for file_name community leader (to store path)
            self.leader_file_label_sop = tk.StringVar()
            self.leader_file_label_sop.set("Filename: ")

            create_label(label_name=self.leader_file_label_sop,
                         frame=frame_project_sop,
                         row=8,
                         column=0,
                         color='black')

            # label for status message community leader
            self.leader_status_message_label_sop = tk.StringVar()
            self.leader_status_message_label_sop.set("")

            create_label(label_name=self.leader_status_message_label_sop,
                         frame=frame_project_sop,
                         row=9,
                         column=0,
                         color='red')

            # check for period and target
            # 0 = sop - provider
            # 1 = sop - leader
            # 2 = sop - teacher
            # 3 = sop - student

            # create and place 'select' button with actions
            tk.Button(frame_project_sop,
                                        text='Select',
                                        width=c.Size.button_width, height=c.Size.button_height,
                                        command=lambda: [validate_path(file_name_label=self.leader_file_label_sop,
                                                                       status_message_label=self.leader_status_message_label_sop,
                                                                       file_opener_object=self.leader_object_sop,
                                                                       index=1,
                                                                       status_list=self.data_file_status_list)
                                                         ]).grid(row=7, column=0,
                                                                 padx=(10, 0), pady=5,
                                                                 sticky='w')

            # place show button
            tk.Button(frame_project_sop,
                                      text='Show',
                                      width=c.Size.button_width, height=c.Size.button_height,
                                      command=lambda: [show_csv_file(file_selected=self.data_file_status_list[1]['status'],
                                                                     status_message_label=self.leader_status_message_label_sop,
                                                                     file_opener_object=self.leader_object_sop)
                                                       ]).grid(row=7, column=1,
                                                               padx=(10, 0), pady=5,
                                                               sticky='w')

            # ------------------------- SOP: Teacher

            tk.Label(frame_project_sop,
                                     text='Teacher data (CSV file only)',
                                     font='Helvetica 11 bold').grid(row=10,
                                                                    column=0, columnspan=4,
                                                                    padx=(10, 0), pady=10,
                                                                    sticky='w')

            # make FileOpener object
            self.teacher_object_sop = w.FileOpener(self)

            # label for file_name teacher (to store path)
            self.teacher_file_label_sop = tk.StringVar()
            self.teacher_file_label_sop.set("Filename: ")

            create_label(label_name=self.teacher_file_label_sop,
                         frame=frame_project_sop,
                         row=14,
                         column=0,
                         color='black')

            # label for status message community leader
            self.teacher_status_message_label_sop = tk.StringVar()
            self.teacher_status_message_label_sop.set("")

            create_label(label_name=self.teacher_status_message_label_sop,
                         frame=frame_project_sop,
                         row=15,
                         column=0,
                         color='red')

            # check for period and target
            # 0 = sop - provider
            # 1 = sop - leader
            # 2 = sop - teacher
            # 3 = sop - student

            # create and placee 'select' button with actions
            tk.Button(frame_project_sop,
                                        text='Select',
                                        width=c.Size.button_width, height=c.Size.button_height,
                                        command=lambda: [validate_path(file_name_label=self.teacher_file_label_sop,
                                                                       status_message_label=self.teacher_status_message_label_sop,
                                                                       file_opener_object=self.teacher_object_sop,
                                                                       index=2,
                                                                       status_list=self.data_file_status_list)
                                                         ]).grid(row=11, column=0,
                                                                 padx=(10, 0), pady=5,
                                                                 sticky='w')

            # create and placee 'show' button with actions
            tk.Button(frame_project_sop,
                                      text='Show',
                                      width=c.Size.button_width, height=c.Size.button_height,
                                      command=lambda: [show_csv_file(file_selected=self.data_file_status_list[2]['status'],
                                                                     status_message_label=self.teacher_status_message_label_sop,
                                                                     file_opener_object=self.teacher_object_sop)
                                                       ]).grid(row=11, column=1,
                                                       padx=(10, 0), pady=5,
                                                       sticky='w')

            # ------------------------- SOP: Student

            self.student_object_sop = w.FileOpener(self)

            tk.Label(frame_project_sop,
                     text='Student data (CSV file only)',
                     font='Helvetica 11 bold').grid(row=16, column=0,
                                                    columnspan=4,
                                                    padx=(10, 0), pady=10,
                                                    sticky='w')

            # convert to string var and set init text
            self.student_file_label_sop = tk.StringVar()
            self.student_file_label_sop.set("Filename: ")

            create_label(label_name=self.student_file_label_sop,
                        frame=frame_project_sop,
                        row=19,
                        column=0,
                        color='black')

            # label for status message community leader
            self.student_status_message_label_sop = tk.StringVar()
            self.student_status_message_label_sop.set("")

            create_label(label_name=self.student_status_message_label_sop,
                         frame=frame_project_sop,
                         row=20,
                         column=0,
                         color='red')

            # check for period and target
            # 0 = sop - provider
            # 1 = sop - leader
            # 2 = sop - teacher
            # 3 = sop - student

            # create button with actions
            tk.Button(frame_project_sop,
                                        text='Select',
                                        width=c.Size.button_width, height=c.Size.button_height,
                                        command=lambda: [validate_path(file_name_label=self.student_file_label_sop,
                                                                       status_message_label=self.student_status_message_label_sop,
                                                                       file_opener_object=self.student_object_sop,
                                                                       index=3,
                                                                       status_list=self.data_file_status_list)]).grid(row=17, column=0,
                                                                                                                      padx=(10, 0), pady=5,
                                                                                                                      sticky='w')

            # place show button
            tk.Button(frame_project_sop,
                                      text='Show',
                                      width=c.Size.button_width, height=c.Size.button_height,
                                      command=lambda: [show_csv_file(file_selected=self.data_file_status_list[3]['status'],
                                                                     status_message_label=self.student_status_message_label_sop,
                                                                     file_opener_object=self.student_object_sop)
                                                       ]).grid(row=17, column=1,
                                                       padx=(10, 0), pady=5,
                                                       sticky='w')

            # ------------------------- HOP

            # ------------------------- Data collection: Halfway of project (HOP) Frame
            frame_project_hop = ttk.LabelFrame(self.tab_hop, text="2.2 Data collection - 2: Halfway of project",
                                                 width=1200, height=700)
            frame_project_hop.grid_propagate(0)
            frame_project_hop.grid(padx=(10, 0),
                                     pady=(10, 0),
                                     sticky='nsew')

            # ------------------------- HOP: Project provider
            tk.Label(frame_project_hop,
                     text='Project provider data (CSV file only)',
                     font='Helvetica 11 bold').grid(row=2, column=0, columnspan=4,
                                                    padx=(10, 0),
                                                    pady=(10, 0),
                                                    sticky='w')

            # make FileOpener object
            self.provider_object_hop = w.FileOpener(self)

            # label for file_name provider (to store file path)
            self.provider_file_label_hop = tk.StringVar()
            self.provider_file_label_hop.set("Filename: ")

            # place in GUI
            create_label(label_name= self.provider_file_label_hop,
                         frame=frame_project_hop,
                         row=4,
                         column=0,
                         color='black')

            # label for status message provider
            self.provider_status_message_label_hop = tk.StringVar()
            self.provider_status_message_label_hop.set("")

            # place in GUI
            create_label(label_name= self.provider_status_message_label_hop,
                         frame=frame_project_hop,
                         row=5,
                         column=0,
                         color='red')

            # check for period and target
            # 4 = hop - provider
            # 5 = hop - leader
            # 6 = hop - teacher
            # 7 = hop - student
            # print(data_file_status_list[4])

            # create and place 'select' button with actions
            tk.Button(frame_project_hop,
                                        text='Select',
                                        width=c.Size.button_width, height=c.Size.button_height,
                                        command=lambda: [validate_path(file_name_label= self.provider_file_label_hop,
                                                                       status_message_label= self.provider_status_message_label_hop,
                                                                       file_opener_object= self.provider_object_hop,
                                                                       index= 4,
                                                                       status_list=self.data_file_status_list)
                                                         ]).grid(row=3, column=0,
                                                                 padx=(10, 0), pady=5,
                                                                 sticky='w')

            # create and place 'show' button with actions
            tk.Button(frame_project_hop,
                                      text='Show',
                                      width=c.Size.button_width, height=c.Size.button_height,
                                      command=lambda: [show_csv_file(file_selected= self.data_file_status_list[4]['status'],
                                                                     status_message_label= self.provider_status_message_label_hop,
                                                                     file_opener_object= self.provider_object_hop)
                                      ]).grid(row=3, column=1,
                                              padx=(10, 0), pady=5,
                                              sticky='w')

            #------------------------- HOP: Community leader

            tk.Label(frame_project_hop,
                     text='Community leader data (CSV file only)',
                     font='Helvetica 11 bold').grid(row=6, column=0, columnspan=4,
                                                    pady=(10), padx=(10, 0),
                                                    sticky='w')

            # make FileOpener object
            self.leader_object_hop = w.FileOpener(self)

            # label for file_name community leader (to store path)
            self.leader_file_label_hop = tk.StringVar()
            self.leader_file_label_hop.set("Filename: ")

            create_label(label_name=self.leader_file_label_hop,
                         frame=frame_project_hop,
                         row=8,
                         column=0,
                         color='black')

            # label for status message community leader
            self.leader_status_message_label_hop = tk.StringVar()
            self.leader_status_message_label_hop.set("")

            create_label(label_name=self.leader_status_message_label_hop,
                         frame=frame_project_hop,
                         row=9,
                         column=0,
                         color='red')

            # check for period and target
            # 4 = hop - provider
            # 5 = hop - leader
            # 6 = hop - teacher
            # 7 = hop - student
            # print(data_file_status_list[4])

            # create and place 'select' button with actions
            tk.Button(frame_project_hop,
                                        text='Select',
                                        width=c.Size.button_width, height=c.Size.button_height,
                                        command=lambda: [validate_path(file_name_label=self.leader_file_label_hop,
                                                                       status_message_label=self.leader_status_message_label_hop,
                                                                       file_opener_object=self.leader_object_hop,
                                                                       index=5,
                                                                       status_list=self.data_file_status_list)
                                                         ]).grid(row=7, column=0,
                                                                 padx=(10, 0), pady=5,
                                                                 sticky='w')

            # place show button
            tk.Button(frame_project_hop,
                                      text='Show',
                                      width=c.Size.button_width, height=c.Size.button_height,
                                      command=lambda: [show_csv_file(file_selected=self.data_file_status_list[5]['status'],
                                                                     status_message_label=self.leader_status_message_label_hop,
                                                                     file_opener_object=self.leader_object_hop)
                                                       ]).grid(row=7, column=1,
                                                               padx=(10, 0), pady=5,
                                                               sticky='w')

            # ------------------------- HOP: Teacher

            tk.Label(frame_project_hop,
                                     text='Teacher data (CSV file only)',
                                     font='Helvetica 11 bold').grid(row=10,
                                                                    column=0, columnspan=4,
                                                                    padx=(10, 0), pady=10,
                                                                    sticky='w')

            # make FileOpener object
            self.teacher_object_hop = w.FileOpener(self)

            # label for file_name teacher (to store path)
            self.teacher_file_label_hop = tk.StringVar()
            self.teacher_file_label_hop.set("Filename: ")

            create_label(label_name=self.teacher_file_label_hop,
                         frame=frame_project_hop,
                         row=14,
                         column=0,
                         color='black')

            # label for status message community leader
            self.teacher_status_message_label_hop = tk.StringVar()
            self.teacher_status_message_label_hop.set("")

            create_label(label_name=self.teacher_status_message_label_hop,
                         frame=frame_project_hop,
                         row=15,
                         column=0,
                         color='red')

            # check for period and target
            # 4 = hop - provider
            # 5 = hop - leader
            # 6 = hop - teacher
            # 7 = hop - student

            # create and placee 'select' button with actions
            tk.Button(frame_project_hop,
                                        text='Select',
                                        width=c.Size.button_width, height=c.Size.button_height,
                                        command=lambda: [validate_path(file_name_label=self.teacher_file_label_hop,
                                                                       status_message_label=self.teacher_status_message_label_hop,
                                                                       file_opener_object=self.teacher_object_hop,
                                                                       index=6,
                                                                       status_list=self.data_file_status_list)
                                                         ]).grid(row=11, column=0,
                                                                 padx=(10, 0), pady=5,
                                                                 sticky='w')

            # create and placee 'show' button with actions
            tk.Button(frame_project_hop,
                                      text='Show',
                                      width=c.Size.button_width, height=c.Size.button_height,
                                      command=lambda: [show_csv_file(file_selected=self.data_file_status_list[6]['status'],
                                                                     status_message_label=self.teacher_status_message_label_hop,
                                                                     file_opener_object=self.teacher_object_hop)
                                                       ]).grid(row=11, column=1,
                                                       padx=(10, 0), pady=5,
                                                       sticky='w')

            # ------------------------- HOP: Student

            self.student_object_hop = w.FileOpener(self)

            tk.Label(frame_project_hop,
                     text='Student data (CSV file only)',
                     font='Helvetica 11 bold').grid(row=16, column=0,
                                                    columnspan=4,
                                                    padx=(10, 0), pady=10,
                                                    sticky='w')

            # convert to string var and set init text
            self.student_file_label_hop = tk.StringVar()
            self.student_file_label_hop.set("Filename: ")

            create_label(label_name=self.student_file_label_hop,
                        frame=frame_project_hop,
                        row=19,
                        column=0,
                        color='black')

            # label for status message community leader
            self.student_status_message_label_hop = tk.StringVar()
            self.student_status_message_label_hop.set("")

            create_label(label_name=self.student_status_message_label_hop,
                         frame=frame_project_hop,
                         row=20,
                         column=0,
                         color='red')

            # check for period and target
            # 4 = hop - provider
            # 5 = hop - leader
            # 6 = hop - teacher
            # 7 = hop - student

            # create button with actions
            tk.Button(frame_project_hop,
                                        text='Select',
                                        width=c.Size.button_width, height=c.Size.button_height,
                                        command=lambda: [validate_path(file_name_label=self.student_file_label_hop,
                                                                       status_message_label=self.student_status_message_label_hop,
                                                                       file_opener_object=self.student_object_hop,
                                                                       index=7,
                                                                       status_list=self.data_file_status_list
                                                                       )]).grid(row=17, column=0,
                                                                 padx=(10, 0), pady=5,
                                                                 sticky='w')

            # place show button
            tk.Button(frame_project_hop,
                                      text='Show',
                                      width=c.Size.button_width, height=c.Size.button_height,
                                      command=lambda: [show_csv_file(file_selected=self.data_file_status_list[7]['status'],
                                                                     status_message_label=self.student_status_message_label_hop,
                                                                     file_opener_object=self.student_object_hop)
                                                       ]).grid(row=17, column=1,
                                                       padx=(10, 0), pady=5,
                                                       sticky='w')

            # ------------------------- EOP

            # ------------------------- Data collection: End of project (EOP) Frame
            frame_project_eop = ttk.LabelFrame(self.tab_eop, text="2.2 Data collection - 3: End of project",
                                                   width=1200, height=700)
            frame_project_eop.grid_propagate(0)
            frame_project_eop.grid(padx=(10, 0),
                                       pady=(10, 0),
                                       sticky='nsew')

            # ------------------------- EOP: Project provider
            tk.Label(frame_project_eop,
                     text='Project provider data (CSV file only)',
                     font='Helvetica 11 bold').grid(row=2, column=0, columnspan=4,
                                                    padx=(10, 0),
                                                    pady=(10, 0),
                                                    sticky='w')

            # make FileOpener object
            self.provider_object_eop = w.FileOpener(self)

            # label for file_name provider (to store file path)
            self.provider_file_label_eop = tk.StringVar()
            self.provider_file_label_eop.set("Filename: ")

            # place in GUI
            create_label(label_name=self.provider_file_label_eop,
                         frame=frame_project_eop,
                         row=4,
                         column=0,
                         color='black')

            # label for status message provider
            self.provider_status_message_label_eop = tk.StringVar()
            self.provider_status_message_label_eop.set("")

            # place in GUI
            create_label(label_name=self.provider_status_message_label_eop,
                         frame=frame_project_eop,
                         row=5,
                         column=0,
                         color='red')

            # check for period and target
            # 12 = eop - provider
            # 13 = eop - leader
            # 14 = eop - teacher
            # 15 = eop - student
            # print(data_file_status_list[8])

            # create and place 'select' button with actions
            tk.Button(frame_project_eop,
                      text='Select',
                      width=c.Size.button_width, height=c.Size.button_height,
                      command=lambda: [validate_path(file_name_label=self.provider_file_label_eop,
                                                     status_message_label=self.provider_status_message_label_eop,
                                                     file_opener_object=self.provider_object_eop,
                                                     index=8,
                                                     status_list=self.data_file_status_list)
                                       ]).grid(row=3, column=0,
                                               padx=(10, 0), pady=5,
                                               sticky='w')

            # create and place 'show' button with actions
            tk.Button(frame_project_eop,
                      text='Show',
                      width=c.Size.button_width, height=c.Size.button_height,
                      command=lambda: [show_csv_file(file_selected=self.data_file_status_list[8]['status'],
                                                     status_message_label=self.provider_status_message_label_eop,
                                                     file_opener_object=self.provider_object_eop)
                                       ]).grid(row=3, column=1,
                                               padx=(10, 0), pady=5,
                                               sticky='w')

            # ------------------------- EOP: Community leader

            tk.Label(frame_project_eop,
                     text='Community leader data (CSV file only)',
                     font='Helvetica 11 bold').grid(row=6, column=0, columnspan=4,
                                                    pady=(10), padx=(10, 0),
                                                    sticky='w')

            # make FileOpener object
            self.leader_object_eop = w.FileOpener(self)

            # label for file_name community leader (to store path)
            self.leader_file_label_eop = tk.StringVar()
            self.leader_file_label_eop.set("Filename: ")

            create_label(label_name=self.leader_file_label_eop,
                         frame=frame_project_eop,
                         row=8,
                         column=0,
                         color='black')

            # label for status message community leader
            self.leader_status_message_label_eop = tk.StringVar()
            self.leader_status_message_label_eop.set("")

            create_label(label_name=self.leader_status_message_label_eop,
                         frame=frame_project_eop,
                         row=9,
                         column=0,
                         color='red')

            # check for period and target
            # 8 = eop - provider
            # 9 = eop - leader
            # 10 = eop - teacher
            # 11 = eop - student

            # create and place 'select' button with actions
            tk.Button(frame_project_eop,
                      text='Select',
                      width=c.Size.button_width, height=c.Size.button_height,
                      command=lambda: [validate_path(file_name_label=self.leader_file_label_eop,
                                                     status_message_label=self.leader_status_message_label_eop,
                                                     file_opener_object=self.leader_object_eop,
                                                     index=9,
                                                     status_list=self.data_file_status_list)
                                       ]).grid(row=7, column=0,
                                               padx=(10, 0), pady=5,
                                               sticky='w')

            # place show button
            tk.Button(frame_project_eop,
                      text='Show',
                      width=c.Size.button_width, height=c.Size.button_height,
                      command=lambda: [show_csv_file(file_selected=self.data_file_status_list[9]['status'],
                                                     status_message_label=self.leader_status_message_label_eop,
                                                     file_opener_object=self.leader_object_eop)
                                       ]).grid(row=7, column=1,
                                               padx=(10, 0), pady=5,
                                               sticky='w')

            # ------------------------- HOP: Teacher

            tk.Label(frame_project_eop,
                     text='Teacher data (CSV file only)',
                     font='Helvetica 11 bold').grid(row=10,
                                                    column=0, columnspan=4,
                                                    padx=(10, 0), pady=10,
                                                    sticky='w')

            # make FileOpener object
            self.teacher_object_eop = w.FileOpener(self)

            # label for file_name teacher (to store path)
            self.teacher_file_label_eop = tk.StringVar()
            self.teacher_file_label_eop.set("Filename: ")

            create_label(label_name=self.teacher_file_label_eop,
                         frame=frame_project_eop,
                         row=14,
                         column=0,
                         color='black')

            # label for status message community leader
            self.teacher_status_message_label_eop = tk.StringVar()
            self.teacher_status_message_label_eop.set("")

            create_label(label_name=self.teacher_status_message_label_eop,
                         frame=frame_project_eop,
                         row=15,
                         column=0,
                         color='red')

            # check for period and target
            # 8 = eop - provider
            # 9 = eop - leader
            # 10 = eop - teacher
            # 11 = eop - student

            # create and placee 'select' button with actions
            tk.Button(frame_project_eop,
                      text='Select',
                      width=c.Size.button_width, height=c.Size.button_height,
                      command=lambda: [validate_path(file_name_label=self.teacher_file_label_eop,
                                                     status_message_label=self.teacher_status_message_label_eop,
                                                     file_opener_object=self.teacher_object_eop,
                                                     index=10,
                                                     status_list=self.data_file_status_list)
                                       ]).grid(row=11, column=0,
                                               padx=(10, 0), pady=5,
                                               sticky='w')

            # create and placee 'show' button with actions
            tk.Button(frame_project_eop,
                      text='Show',
                      width=c.Size.button_width, height=c.Size.button_height,
                      command=lambda: [show_csv_file(file_selected=self.data_file_status_list[10]['status'],
                                                     status_message_label=self.teacher_status_message_label_eop,
                                                     file_opener_object=self.teacher_object_eop)
                                       ]).grid(row=11, column=1,
                                               padx=(10, 0), pady=5,
                                               sticky='w')

            # ------------------------- EOP: Student

            self.student_object_eop = w.FileOpener(self)

            tk.Label(frame_project_eop,
                     text='Student data (CSV file only)',
                     font='Helvetica 11 bold').grid(row=16, column=0,
                                                    columnspan=4,
                                                    padx=(10, 0), pady=10,
                                                    sticky='w')

            # convert to string var and set init text
            self.student_file_label_eop = tk.StringVar()
            self.student_file_label_eop.set("Filename: ")

            create_label(label_name=self.student_file_label_eop,
                         frame=frame_project_eop,
                         row=19,
                         column=0,
                         color='black')

            # label for status message community leader
            self.student_status_message_label_eop = tk.StringVar()
            self.student_status_message_label_eop.set("")

            create_label(label_name=self.student_status_message_label_eop,
                         frame=frame_project_eop,
                         row=20,
                         column=0,
                         color='red')

            # check for period and target
            # 8 = eop - provider
            # 9 = eop - leader
            # 10 = eop - teacher
            # 11 = eop - student

            # create button with actions
            tk.Button(frame_project_eop,
                      text='Select',
                      width=c.Size.button_width, height=c.Size.button_height,
                      command=lambda: [validate_path(file_name_label=self.student_file_label_eop,
                                                     status_message_label=self.student_status_message_label_eop,
                                                     file_opener_object=self.student_object_eop,
                                                     index=11,
                                                     status_list=self.data_file_status_list
                                                     )]).grid(row=17, column=0,
                                                              padx=(10, 0), pady=5,
                                                              sticky='w')

            # place show button
            tk.Button(frame_project_eop,
                      text='Show',
                      width=c.Size.button_width, height=c.Size.button_height,
                      command=lambda: [show_csv_file(file_selected=self.data_file_status_list[11]['status'],
                                                     status_message_label=self.student_status_message_label_eop,
                                                     file_opener_object=self.student_object_eop)
                                       ]).grid(row=17, column=1,
                                               padx=(10, 0), pady=5,
                                               sticky='w')

            # ------------------------- YAP

            # ------------------------- Data collection: Year after end project (YAP) Frame
            frame_project_yap = ttk.LabelFrame(self.tab_yap, text="2.2 Data collection - 4: Year after end of project",
                                               width=1200, height=700)
            frame_project_yap.grid_propagate(0)
            frame_project_yap.grid(padx=(10, 0),
                                   pady=(10, 0),
                                   sticky='nsew')

            # ------------------------- YAP: Project provider
            tk.Label(frame_project_yap,
                     text='Project provider data (CSV file only)',
                     font='Helvetica 11 bold').grid(row=2, column=0, columnspan=4,
                                                    padx=(10, 0),
                                                    pady=(10, 0),
                                                    sticky='w')

            # make FileOpener object
            self.provider_object_yap = w.FileOpener(self)

            # label for file_name provider (to store file path)
            self.provider_file_label_yap = tk.StringVar()
            self.provider_file_label_yap.set("Filename: ")

            # place in GUI
            create_label(label_name=self.provider_file_label_yap,
                         frame=frame_project_yap,
                         row=4,
                         column=0,
                         color='black')

            # label for status message provider
            self.provider_status_message_label_yap = tk.StringVar()
            self.provider_status_message_label_yap.set("")

            # place in GUI
            create_label(label_name=self.provider_status_message_label_yap,
                         frame=frame_project_yap,
                         row=5,
                         column=0,
                         color='red')

            # check for period and target
            # 12 = yap - provider
            # 13 = yap - leader
            # 14 = yap - teacher
            # 15 = yap - student
            # print(data_file_status_list[12])

            # create and place 'select' button with actions
            tk.Button(frame_project_yap,
                      text='Select',
                      width=c.Size.button_width, height=c.Size.button_height,
                      command=lambda: [validate_path(file_name_label=self.provider_file_label_yap,
                                                     status_message_label=self.provider_status_message_label_yap,
                                                     file_opener_object=self.provider_object_yap,
                                                     index=12,
                                                     status_list=self.data_file_status_list)
                                       ]).grid(row=3, column=0,
                                               padx=(10, 0), pady=5,
                                               sticky='w')

            # create and place 'show' button with actions
            tk.Button(frame_project_yap,
                      text='Show',
                      width=c.Size.button_width, height=c.Size.button_height,
                      command=lambda: [show_csv_file(file_selected=self.data_file_status_list[12]['status'],
                                                     status_message_label=self.provider_status_message_label_yap,
                                                     file_opener_object=self.provider_object_yap)
                                       ]).grid(row=3, column=1,
                                               padx=(10, 0), pady=5,
                                               sticky='w')

            # ------------------------- YAP: Community leader

            tk.Label(frame_project_yap,
                     text='Community leader data (CSV file only)',
                     font='Helvetica 11 bold').grid(row=6, column=0, columnspan=4,
                                                    pady=(10), padx=(10, 0),
                                                    sticky='w')

            # make FileOpener object
            self.leader_object_yap = w.FileOpener(self)

            # label for file_name community leader (to store path)
            self.leader_file_label_yap = tk.StringVar()
            self.leader_file_label_yap.set("Filename: ")

            create_label(label_name=self.leader_file_label_yap,
                         frame=frame_project_yap,
                         row=8,
                         column=0,
                         color='black')

            # label for status message community leader
            self.leader_status_message_label_yap = tk.StringVar()
            self.leader_status_message_label_yap.set("")

            create_label(label_name=self.leader_status_message_label_yap,
                         frame=frame_project_yap,
                         row=9,
                         column=0,
                         color='red')

            # check for period and target
            # 12 = yap - provider
            # 13 = yap - leader
            # 14 = yap - teacher
            # 15 = yap - student

            # create and place 'select' button with actions
            tk.Button(frame_project_yap,
                      text='Select',
                      width=c.Size.button_width, height=c.Size.button_height,
                      command=lambda: [validate_path(file_name_label=self.leader_file_label_yap,
                                                     status_message_label=self.leader_status_message_label_yap,
                                                     file_opener_object=self.leader_object_yap,
                                                     index=13,
                                                     status_list=self.data_file_status_list)
                                       ]).grid(row=7, column=0,
                                               padx=(10, 0), pady=5,
                                               sticky='w')

            # place show button
            tk.Button(frame_project_yap,
                      text='Show',
                      width=c.Size.button_width, height=c.Size.button_height,
                      command=lambda: [show_csv_file(file_selected=self.data_file_status_list[13]['status'],
                                                     status_message_label=self.leader_status_message_label_yap,
                                                     file_opener_object=self.leader_object_yap)
                                       ]).grid(row=7, column=1,
                                               padx=(10, 0), pady=5,
                                               sticky='w')

            # ------------------------- YAP: Teacher

            tk.Label(frame_project_yap,
                     text='Teacher data (CSV file only)',
                     font='Helvetica 11 bold').grid(row=10,
                                                    column=0, columnspan=4,
                                                    padx=(10, 0), pady=10,
                                                    sticky='w')

            # make FileOpener object
            self.teacher_object_yap = w.FileOpener(self)

            # label for file_name teacher (to store path)
            self.teacher_file_label_yap = tk.StringVar()
            self.teacher_file_label_yap.set("Filename: ")

            create_label(label_name=self.teacher_file_label_yap,
                         frame=frame_project_yap,
                         row=14,
                         column=0,
                         color='black')

            # label for status message community leader
            self.teacher_status_message_label_yap = tk.StringVar()
            self.teacher_status_message_label_yap.set("")

            create_label(label_name=self.teacher_status_message_label_yap,
                         frame=frame_project_yap,
                         row=15,
                         column=0,
                         color='red')

            # check for period and target
            # 12 = yap - provider
            # 13 = yap - leader
            # 14 = yap - teacher
            # 15 = yap - student

            # create and placee 'select' button with actions
            tk.Button(frame_project_yap,
                      text='Select',
                      width=c.Size.button_width, height=c.Size.button_height,
                      command=lambda: [validate_path(file_name_label=self.teacher_file_label_yap,
                                                     status_message_label=self.teacher_status_message_label_yap,
                                                     file_opener_object=self.teacher_object_yap,
                                                     index=14,
                                                     status_list=self.data_file_status_list)
                                       ]).grid(row=11, column=0,
                                               padx=(10, 0), pady=5,
                                               sticky='w')

            # create and placee 'show' button with actions
            tk.Button(frame_project_yap,
                      text='Show',
                      width=c.Size.button_width, height=c.Size.button_height,
                      command=lambda: [show_csv_file(file_selected=self.data_file_status_list[14]['status'],
                                                     status_message_label=self.teacher_status_message_label_yap,
                                                     file_opener_object=self.teacher_object_yap)
                                       ]).grid(row=11, column=1,
                                               padx=(10, 0), pady=5,
                                               sticky='w')

            # ------------------------- YAP: Student

            self.student_object_yap = w.FileOpener(self)

            tk.Label(frame_project_yap,
                     text='Student data (CSV file only)',
                     font='Helvetica 11 bold').grid(row=16, column=0,
                                                    columnspan=4,
                                                    padx=(10, 0), pady=10,
                                                    sticky='w')

            # convert to string var and set init text
            self.student_file_label_yap = tk.StringVar()
            self.student_file_label_yap.set("Filename: ")

            create_label(label_name=self.student_file_label_yap,
                         frame=frame_project_yap,
                         row=19,
                         column=0,
                         color='black')

            # label for status message community leader
            self.student_status_message_label_yap = tk.StringVar()
            self.student_status_message_label_yap.set("")

            create_label(label_name=self.student_status_message_label_yap,
                         frame=frame_project_yap,
                         row=20,
                         column=0,
                         color='red')

            # check for period and target
            # 12 = yap - provider
            # 13 = yap - leader
            # 14 = yap - teacher
            # 15 = yap - student

            # create button with actions
            tk.Button(frame_project_yap,
                      text='Select',
                      width=c.Size.button_width, height=c.Size.button_height,
                      command=lambda: [validate_path(file_name_label=self.student_file_label_yap,
                                                     status_message_label=self.student_status_message_label_yap,
                                                     file_opener_object=self.student_object_yap,
                                                     index=15,
                                                     status_list=self.data_file_status_list
                                                     )]).grid(row=17, column=0,
                                                              padx=(10, 0), pady=5,
                                                              sticky='w')

            # place show button
            tk.Button(frame_project_yap,
                      text='Show',
                      width=c.Size.button_width, height=c.Size.button_height,
                      command=lambda: [show_csv_file(file_selected=self.data_file_status_list[15]['status'],
                                                     status_message_label=self.student_status_message_label_yap,
                                                     file_opener_object=self.student_object_yap)
                                       ]).grid(row=17, column=1,
                                               padx=(10, 0), pady=5,
                                               sticky='w')

            # focus on window
            window_obj = w.Window()
            window_obj.focus_window(self.start_project_window)

        else:
            # reset all the red status messages when re opening window
            self.reset_status_messages()
            self.start_project_window.deiconify()

    def hide_window(self, window):

        if window == "start_project":
            self.start_project_window.withdraw()

class DataAnalysisScreen(tk.Frame):

    def __init__(self):
        tk.Frame.__init__(self)

        global popup_window
        self.popup_window = None

        # create new instance of DataAnalysis class
        self.data_analysis_object = w.DataAnalysis(self)

        frame_project_docs = ttk.LabelFrame(self, text="View help documentation",
                                            width=c.Size.label_frame_width,
                                            height=80,
                                            style="Doc.TLabelframe")

        frame_project_docs.grid_propagate(0)
        frame_project_docs.grid(padx=(10, 0),
                                pady=(10, 0),
                                sticky='nsew')

        tk.Button(frame_project_docs,
                  text='3.1 Loading in Data',
                  width=20, height=c.Size.button_height,
                  command="").grid(row=0, column=0,
                                   padx=(10, 0), pady=5,
                                   sticky='w')

        tk.Button(frame_project_docs,
                  text='3.2 Summary Data',
                  width=20, height=c.Size.button_height,
                  command="").grid(row=0, column=1,
                                   padx=(10, 0), pady=5,
                                   sticky='w')

        # ------------------------- Data Analysis: Load all data files

        frame_load_data = ttk.LabelFrame(self, text="3.1 Load All Data",
                                            width=1200, height=150)
        frame_load_data.grid_propagate(0)
        frame_load_data.grid(padx=(10, 0),
                                pady=(10, 0),
                                sticky='nsew')

        # status message
        tk.Label(frame_load_data,
                 text='Load all data for data analysis').grid(row=1, column=0,
                                            padx=(10,0), pady=5,
                                            sticky='w')

        # delete window and reset state every time load in data button is clicked
        def adjusted_state_window():
            self.popup_window = None

        tk.Button(frame_load_data, text='Load in data',
                  width=18, height=1,
                  command=lambda: [self.data_analysis_object.delete_frame(self.popup_window), adjusted_state_window(),
                                   self.data_analysis_object.load_into_database(self.dict_paths.dc_file_paths, frame_load_data)]).grid(row=2, column=0,
                                                                                                                                       padx=(10,0), pady=5,
                                                                                                                                       sticky='w')

        # ------------------------- Data Analysis: 3.1 Summary Data Frame

        frame_summary_data = ttk.LabelFrame(self, text="3.2 Summary Data",
                                           width=1200, height=150)
        frame_summary_data.grid_propagate(0)
        frame_summary_data.grid(padx=(10, 0),
                               pady=(10, 0),
                               sticky='nsew')

        self.status_message_summary_data = tk.StringVar()
        self.status_message_summary_data.set("")

        # status message
        tk.Label(frame_summary_data,
                 textvariable=self.status_message_summary_data,
                 foreground='red',
                 font='Helvetica 12').grid(row=3, column=0,
                                           padx=(10, 0),
                                           pady=5,
                                           sticky='w')

        # validation for file input
        def data_files_selected(tab_index):
            if not self.data_analysis_object.selected_file_counter:
                self.status_message_summary_data.set('Please load in csv files!')
            else:
                self.status_message_summary_data.set("")
                self.create_popup()
                self.notebook_data_analysis.select(tab_index)

        tk.Button(frame_summary_data, text='Show tables',
                  width=18, height=1,
                  command=lambda : [data_files_selected(0)]).grid(row=1, column=0,
                                                                  padx=(10,0), pady=(10,5),
                                                                  sticky='w')

        tk.Button(frame_summary_data, text='Show visualisations',
                  width=18, height=1,
                  command=lambda: [data_files_selected(1)]).grid(row=2, column=0,
                                                                 padx=(10, 0),
                                                                 pady=5,
                                                                 sticky='w')



    # ------------------------- Data Analysis: Get data from SQL model
    def send_data_object(self, data):
        self.data_object = data
        self.data_analysis_object.get_data_object(self.data_object)

    def send_dict_paths(self, dict):
        self.dict_paths = dict
        self.data_analysis_object.get_paths_dict(self.dict_paths)

    def send_save_file_object(self, data):
        self.save_file_object = data

    # 1234
    def save_data(self):
        self.save_file_object.get_data_analysis(self.data_analysis_object.selected_file_counter)

    # ------------------------- Popup window
    def create_popup(self):

        # if there is not already a 'start of project' window
        if not self.popup_window:
            # create pop up window
            self.popup_window = tk.Toplevel()

            width = 1280
            height = 720
            position_left = 150
            position_right = 150
            self.popup_window.geometry("{}x{}+{}+{}".format(width, height, position_left, position_right))

            # set size window fixed
            self.popup_window.resizable(0, 0)

            self.popup_window.wm_title('Data Analysis')

            # make notebook
            self.notebook_data_analysis = ttk.Notebook(self.popup_window)

            # make tabs
            self.tab_tables = ttk.Frame(self.popup_window, width=c.Size.hd_frame_width, height=c.Size.hd_frame_height)
            self.tab_tables.pack(side="left", fill="both", expand=True)


            self.tab_visualisations = ttk.Frame(self.popup_window, width=c.Size.hd_frame_width, height=c.Size.hd_frame_height)
            self.tab_visualisations.pack(side="left", fill="both", expand=True)

            # add tabs to notebook
            self.notebook_data_analysis.add(self.tab_tables, text='Summary Tables')
            self.notebook_data_analysis.add(self.tab_visualisations, text='Visualisations')

            self.notebook_data_analysis.pack(side="left", fill="both", expand='true')

            # hide window if closed
            self.popup_window.protocol("WM_DELETE_WINDOW", lambda arg='popup': self.hide_window(arg))

            # prevent shrinking to widget size
            # self.tab_tables.pack_propagate(False)
            # self.tab_visualisations.pack_propagate(False)

            sql_check_file_id = "select distinct file_id from metric_value"
            retrieve_check_file_id = self.data_object.query_no_par(sql_check_file_id)

            provider_id = [0, 4, 8,  12]
            leader_id =   [1, 5, 9,  13]
            teacher_id =  [2, 6, 10, 14]
            student_id =  [3, 7, 11, 15]

            self.time_option_list = []

            time_option_dict = {
                0: "Start of project",
                1: "Halfway point of project",
                2: "End of project",
                3: "Year after end of project"
            }

            def get_target(event):

                self.select_time_frame.set('')
                self.time_option_list = []
                self.input_target = event.widget.get()

                # check in database which timeframe is present
                for index, file_id in enumerate(retrieve_check_file_id):

                    if file_id[0] in provider_id:
                        if self.input_target == "Project Provider":
                            self.time_option_list.append(time_option_dict[provider_id.index(file_id[0])])
                            # print('INDEX if statement ---', index)

                    if file_id[0] in leader_id:
                        if self.input_target == "Community School Leader":
                            self.time_option_list.append(time_option_dict[leader_id.index(file_id[0])])

                    if file_id[0] in teacher_id:
                        if self.input_target == "Teacher":
                            self.time_option_list.append(time_option_dict[teacher_id.index(file_id[0])])

                    if file_id[0] in student_id:
                        if self.input_target == "Student":
                            self.time_option_list.append(time_option_dict[student_id.index(file_id[0])])


                    # print('file_id: ---', file_id[0])
                    # print('time_option_list ---', self.time_option_list)



            def change_time_frame_box():
                if self.time_option_list:
                    self.select_time_frame["values"] = self.time_option_list
                else:
                    self.select_time_frame["values"] = ["(No data available)"]

            # label
            tk.Label(self.tab_tables,
                     text= 'Select the target group and time frame',
                     font='Helvetica 12').pack(side='top',
                                                   anchor='nw',
                                                    pady=5,
                                                    padx=10)

            self.select_target = ttk.Combobox(
                self.tab_tables,
                state="readonly",
                values=["Project Provider",
                        "Community School Leader",
                        "Teacher",
                        "Student"
                        ])

            self.select_target.bind("<<ComboboxSelected>>", get_target)

            self.select_target.pack(side='top',
                                                   anchor='nw',
                                                    pady=5,
                                                    padx=10)

            self.select_time_frame = ttk.Combobox(
                self.tab_tables,
                state="readonly",
                values="",
                postcommand=change_time_frame_box)

            self.select_time_frame.pack(side='top',
                                        anchor='nw',
                                        pady=5,
                                        padx=10)

            def remap_target(target):
                if target == "Project Provider":
                    return 'provider'
                elif target == "Community School Leader":
                    return 'leader'
                elif target == "Teacher":
                    return 'teacher'
                else:
                    return 'student'

            def remap_target_sql(target):
                if target == "Project Provider":
                    return 'project_provider'
                elif target == "Community School Leader":
                    return 'community_school_leader'
                elif target == "Teacher":
                    return 'teacher'
                else:
                    return 'student'

            def remap_timeframe(time_frame):

                if time_frame == "Start of project":
                    return 'sop'
                elif time_frame == "Halfway point of project":
                    return 'hop'
                elif time_frame == "End of project":
                    return 'eop'
                else:
                    return 'yap'

            def validate_combobox_input(state):

                # print ('Timeframe: ', self.select_time_frame.get())
                # print ('Target: ', self.select_target.get())

                if self.select_time_frame.get() == '' and self.select_target.get() == '':
                    self.status_message_tables.set('Select a timeframe and target!')

                elif self.select_time_frame.get() == '' and self.select_target.get() != '':
                    self.status_message_tables.set('Select a timeframe!')

                elif self.select_time_frame.get() != '' and self.select_target.get() == '':
                    self.status_message_tables.set('Select a target!')

                else:
                    # TODO fix for later
                    input_key = remap_timeframe(self.select_time_frame.get()) + '_' + remap_target(self.select_target.get())
                    value = self.dict_paths.dc_file_paths[input_key]

                    # calculate the table based on user input
                    self.data_analysis_object.calculate_data(self.select_time_frame.get(), self.select_target.get())

                    if state == 'new':
                        self.data_analysis_object.make_table(self.tab_tables,
                                                             self.select_time_frame.get(),
                                                             self.select_target.get())

                        self.data_analysis_object.fill_table(self.data_analysis_object.tree)

                    else:
                        self.data_analysis_object.update_table(self.data_analysis_object.tree, self.tab_tables)

            create_table_button = tk.Button(self.tab_tables, text='Create table',
                      width=18, height=1,
                      command=lambda: [validate_combobox_input('new'),
                                       create_table_button.configure(command=lambda: [validate_combobox_input('update')])
                                       ])

            create_table_button.pack(side='top',
                                                   anchor='nw',
                                                    pady=5,
                                                    padx=10)

            # convert to string var and set init text
            self.status_message_tables = tk.StringVar()
            self.status_message_tables.set("")

            # status message
            tk.Label(self.tab_tables,
                     textvariable=self.status_message_tables,
                     font='Helvetica 12', foreground='red').pack(side='top',
                                                   anchor='nw',
                                                    pady=5,
                                                    padx=10)


            # -----------------
            self.visualisation_frame = ttk.Frame(self.tab_visualisations, width=1000, height=300)
            self.visualisation_frame.pack(side="bottom",
                                          pady=0, padx=(10, 20))

            self.survey_question = tk.StringVar()
            self.survey_question.set('')

            tk.Label(self.tab_visualisations,
                     textvariable=self.survey_question,
                     font='Helvetica 12',
                     foreground = 'mediumpurple').pack(side='bottom',
                                                pady=(10, 5),
                                                padx=10)

            self.vis_option_1_frame = ttk.Frame(self.tab_visualisations, width=150, height=10)
            self.vis_option_1_frame.pack(side="left", fill="both")

            self.vis_option_2_frame = ttk.Frame(self.tab_visualisations, width=150, height=10)
            self.vis_option_2_frame.pack(side="left", fill="both")

            self.vis_option_3_frame = ttk.Frame(self.tab_visualisations, width=200, height=10)
            self.vis_option_3_frame.pack(side="left", fill="both")

            self.vis_option_4_frame = ttk.Frame(self.tab_visualisations, width=150, height=10)
            self.vis_option_4_frame.pack(side="left", fill="both")

            self.metric_option_list = []

            def update_metric_list():
                time_frame_list = [var1.get(), var2.get(), var3.get(), var4.get()]

                self.metric_option_list = self.data_analysis_object.visualisation_get_metrics(self.select_target_visualisations.get(),
                                                                                              time_frame_list)
                if not self.metric_option_list:
                    self.select_metric.set("")

            def get_inputs(event):

                self.select_metric.set('')
                self.metric_option_list = []
                self.input_target_vis = event.widget.get()

                time_frame_list = [var1.get(), var2.get(), var3.get(), var4.get()]

                if self.input_target_vis and any(time_frame_list):

                    self.metric_option_list = self.data_analysis_object.visualisation_get_metrics(self.input_target_vis, time_frame_list)

            # label
            tk.Label(self.vis_option_1_frame,
                     text='Select the target group',
                     font='Helvetica 12').pack(
                                               anchor='nw',
                                               pady=(10, 5),
                                               padx=10)

            self.select_target_visualisations = ttk.Combobox(
                self.vis_option_1_frame,
                state="readonly",
                values=["Project Provider",
                        "Community School Leader",
                        "Teacher",
                        "Student"
                        ])

            self.select_target_visualisations.bind("<<ComboboxSelected>>", get_inputs)

            self.select_target_visualisations.pack(
                                                   anchor='nw',
                                                    pady=5,
                                                    padx=10)

            tk.Label(self.vis_option_2_frame,
                     text='Select the time frame(s)',
                     font='Helvetica 12').pack(
                                               anchor='nw',
                                               pady=(10, 5),
                                               padx=10)

            var1 = tk.BooleanVar()
            tk.Checkbutton(self.vis_option_2_frame,
                           text="Start of project",
                           command=lambda : [update_metric_list()],
                           variable=var1).pack(
                                               padx = 10,
                                               anchor='nw')

            var2 = tk.BooleanVar()
            tk.Checkbutton(self.vis_option_2_frame,
                           text= "Halfway point of project",
                           command=lambda : [update_metric_list()],
                           variable=var2).pack(
                                               padx = 10,
                                               anchor='nw')

            var3 = tk.BooleanVar()
            tk.Checkbutton(self.vis_option_2_frame,
                           text="End of project",
                           command=lambda : [update_metric_list()],
                           variable=var3).pack(
                                               padx = 10,
                                               anchor='nw')

            var4 = tk.BooleanVar()
            tk.Checkbutton(self.vis_option_2_frame,
                           text="Year after end of project",
                           command=lambda: [update_metric_list()],
                           variable=var4).pack(
                                               padx = 10,
                                               anchor='nw')

            tk.Label(self.vis_option_3_frame,
                     text='Select metric',
                     font='Helvetica 12').pack(
                                               anchor='nw',
                                               pady=(10, 5),
                                               padx=10)


            def change_visualisation_metric_option():

                if self.metric_option_list:
                    self.select_metric["values"] = self.metric_option_list
                else:

                    self.select_metric["values"] = ["(No data available)"]

            self.select_metric = ttk.Combobox(
                self.vis_option_3_frame,
                width=40,
                state="readonly",
                postcommand=change_visualisation_metric_option,
                values='')

            self.select_metric.pack(
                                   anchor='nw',
                                   pady=5,
                                   padx=10)

            self.status_message_vis = tk.StringVar()
            self.status_message_vis.set('')

            def validate_visualisation_options(target, point, metric, state):

                message_list = []

                def point_selected():
                    for time_point in point:
                        if time_point:
                            return True

                def status_message():
                    message_string = 'Please select '
                    for index, message in enumerate(message_list):

                        if index is not (len(message_list)-1):
                            message_string += message + ', '

                        else:
                            message_string += message

                    message_string += '!'
                    self.status_message_vis.set(message_string)

                if not target:
                    message_list.append('target group')

                if not point_selected():
                    message_list.append('time frame')

                if not metric or metric == "(No data available)" :
                    message_list.append('metric')

                # only show status message if one or more boxes are not filled in
                if not target or not point_selected() or not metric:
                    status_message()

                if not message_list:

                    sql_target = remap_target_sql(self.select_target_visualisations.get())
                    sql_metric = self.select_metric.get()

                    sql = 'select metric_question from metric where target_name = (?) and metric_name = (?)'
                    retrieve_question = self.data_object.query_with_par(sql, (sql_target, sql_metric))

                    metric_question = retrieve_question[0][0]

                    self.survey_question.set('Survey Question: ' + metric_question)
                    self.status_message_vis.set('')

                    if state == 'new':
                        self.data_analysis_object.create_visualisations(self.select_target_visualisations.get(),
                                                                        [var1.get(), var2.get(), var3.get(),
                                                                         var4.get()],
                                                                        self.select_metric.get(),
                                                                        self.visualisation_frame
                                                                        )
                    else:
                        self.visualisation_frame = self.refresh_vis_tab(self.tab_visualisations, self.visualisation_frame)

                        self.data_analysis_object.create_visualisations(self.select_target_visualisations.get(),
                                                                        [var1.get(), var2.get(), var3.get(),
                                                                         var4.get()],
                                                                        self.select_metric.get(),
                                                                        self.visualisation_frame
                                                                        )


            create_visualisations_button = tk.Button(self.vis_option_4_frame, text='Create visualisation',
                                            width=18, height=1,
                                            command=lambda: [validate_visualisation_options(self.select_target_visualisations.get(),
                                                                                            [var1.get(), var2.get(), var3.get(), var4.get()],
                                                                                            self.select_metric.get(), "new"),
                                                             create_visualisations_button.configure(command=lambda: [validate_visualisation_options(self.select_target_visualisations.get(),
                                                                                            [var1.get(), var2.get(), var3.get(), var4.get()],
                                                                                            self.select_metric.get(), "updated")])

                                                             ])

            create_visualisations_button.pack(
                                              anchor='nw',
                                              pady=(40,5),
                                              padx=10)

            tk.Label(self.vis_option_4_frame,
                     textvariable=self.status_message_vis,
                     foreground='red').pack(
                                               anchor='nw',
                                               pady=(10, 5),
                                               padx=10)

            # focus on window
            window_obj = w.Window()
            window_obj.focus_window(self.popup_window)

        else:
            self.popup_window.deiconify()

    def hide_window(self, window):

        if window == "popup":
            self.popup_window.withdraw()


    def refresh_vis_tab(self, main_frame, frame_to_delete):

        # empty out widgets in frame
        for widget in frame_to_delete.winfo_children():
            widget.destroy()


        # frame_to_delete.destroy()
        #
        # self.visualisation_frame = ttk.Frame(main_frame, width=1000, height=300)
        #
        # self.visualisation_frame.pack(side="bottom",
        #                               pady=10, padx=(100, 20))

        return frame_to_delete

class EvaluationScreen(tk.Frame):

    def __init__(self):
        tk.Frame.__init__(self)

        global popup_window_metrics
        self.popup_window_metrics = None


        # make object
        self.impact_evaluation = w.ImpactEvaluation(self)

        frame_project_docs = ttk.LabelFrame(self, text="View help documentation",
                                            width=c.Size.label_frame_width,
                                            height=80,
                                            style="Doc.TLabelframe")

        frame_project_docs.pack(padx=(10, 0), pady = (10, 0),
                                      side="top", fill="both")

        dirname = os.getcwd()
        filename_docs_evaluation = os.path.join(dirname, 'docs', 'impact_evaluation_questions.pdf')

        tk.Button(frame_project_docs,
                  text='4.1 Evaluation',
                  width=20, height=c.Size.button_height,
                  command = lambda: [webbrowser.open(filename_docs_evaluation)]).pack(padx=(10, 0), pady=(5, 15),
                                 side='top',
                                 anchor='nw',
                                 )

        self.frame_main_evaluate= ttk.LabelFrame(self, text="4.1 Evaluate metric results, goals and targets",
                                             width=c.Size.label_frame_width, height=700)

        self.frame_main_evaluate.pack(padx=(10, 0), pady = (10, 0),
                                      side="top", fill="both", expand=True)

        self.scrollable_labelframe = w.ScrollableFrame(self.frame_main_evaluate)

        show_results_button = tk.Button(self.scrollable_labelframe.scrollable_frame,
                  text='Show metric results',
                  width=20,
                  command=lambda: [self.check_if_data_loaded(0), self.check_if_data_loaded(1)])

        show_results_button.pack(padx=(10, 0), pady=(10,5),
                                 side='top',
                                 anchor='nw',
                                 )

        # convert to string var and set init text
        self.status_message_show_metrics = tk.StringVar()
        self.status_message_show_metrics.set("")

        tk.Label(self.scrollable_labelframe.scrollable_frame,
                 textvariable=self.status_message_show_metrics,
                 foreground='red').pack(padx=(10, 0),
                                         side='top',
                                         anchor='nw')

        # --------------
        # metric evaluation
        tk.Label(self.scrollable_labelframe.scrollable_frame,
                 text='Metric evaluation',
                 font='Helvetica 12').pack(padx=(10, 0),
                                         side='top',
                                         anchor='nw')

        # create frame for entry box
        self.frame_entry_box_metric = ttk.Frame(self.scrollable_labelframe.scrollable_frame,
                                                     width=20, height=20)

        self.frame_entry_box_metric.pack(padx=(10, 0), pady=5,
                                         side='top',
                                         anchor='nw')

        self.entry_box_metric = ScrolledText(self.frame_entry_box_metric,
                                             width=c.Size.txt_box_width,
                                             height=c.Size.txt_box_height)

        self.entry_box_metric.pack(padx=(10, 0), pady=5, side='top', anchor='nw')

        # -----------------
        # Target and goal evaluation
        tk.Label(self.scrollable_labelframe.scrollable_frame,
                 text='Target and goal evaluation',
                 font='Helvetica 12').pack(padx=(10, 0),
                                         side='top',
                                         anchor='nw')


        # create frame for entry box
        self.frame_entry_box_target = ttk.Frame(self.scrollable_labelframe.scrollable_frame,
                                                     width=20, height=20)

        self.frame_entry_box_target.pack(padx=(10, 0), pady=5,
                                         side='top',
                                         anchor='nw')

        self.entry_box_target = ScrolledText(self.frame_entry_box_target,
                                             width=c.Size.txt_box_width,
                                             height=c.Size.txt_box_height)

        self.entry_box_target.pack(padx=(10, 0), pady=5, side='top', anchor='nw')

        # -----------------
        # Evaluation questions
        tk.Label(self.scrollable_labelframe.scrollable_frame,
                 text='Evaluation questions',
                 font='Helvetica 12 ').pack(padx=(10, 0), pady=(30,5),
                                         side='top',
                                         anchor='nw')

        # --- Q1
        tk.Label(self.scrollable_labelframe.scrollable_frame,
                 text='Q1 - Is the impact desirable?').pack(padx=(10, 0),
                                         side='top',
                                         anchor='nw')

        # create frame for entry box
        self.frame_entry_box_question_1 = ttk.Frame(self.scrollable_labelframe.scrollable_frame,
                                                width=20, height=20)

        self.frame_entry_box_question_1.pack(padx=(10, 0), pady=5,
                                         side='top',
                                         anchor='nw')

        self.entry_box_question_1 = ScrolledText(self.frame_entry_box_question_1,
                                                 width=c.Size.txt_box_width,
                                                 height=c.Size.txt_box_height)

        self.entry_box_question_1.pack(padx=(10, 0), pady=5, side='top', anchor='nw')

        # --- Q2
        tk.Label(self.scrollable_labelframe.scrollable_frame,
                 text='Q2 - What is the time of the impact? (Short/long term?)').pack(padx=(10, 0),
                                         side='top',
                                         anchor='nw')

        self.frame_entry_box_question_2 = ttk.Frame(self.scrollable_labelframe.scrollable_frame,
                                                    width=c.Size.txt_box_width,
                                                    height=c.Size.txt_box_height)

        self.frame_entry_box_question_2.pack(padx=(10, 0), pady=5,
                                         side='top',
                                         anchor='nw')

        self.entry_box_question_2 = ScrolledText(self.frame_entry_box_question_2,
                                                 width=c.Size.txt_box_width,
                                                 height=c.Size.txt_box_height)

        self.entry_box_question_2.pack(padx=(10, 0), pady=5, side='top', anchor='nw')

        # --- Q3
        tk.Label(self.scrollable_labelframe.scrollable_frame,
                 text='Q3 - Is the impact sustainable over time?').pack(padx=(10, 0),
                                         side='top',
                                         anchor='nw')

        self.frame_entry_box_question_3 = ttk.Frame(self.scrollable_labelframe.scrollable_frame,
                                                    width=20, height=20)
        self.frame_entry_box_question_3.pack(padx=(10, 0), pady=5,
                                         side='top',
                                         anchor='nw')

        self.entry_box_question_3 = ScrolledText(self.frame_entry_box_question_3,
                                                 width=c.Size.txt_box_width,
                                                 height=c.Size.txt_box_height)

        self.entry_box_question_3.pack(padx=(10, 0), pady=5, side='top', anchor='nw')

        # --- Q4
        tk.Label(self.scrollable_labelframe.scrollable_frame,
                 text='Q4 - What is the severity of the impact?').pack(padx=(10, 0),
                                         side='top',
                                         anchor='nw')

        self.frame_entry_box_question_4 = ttk.Frame(self.scrollable_labelframe.scrollable_frame,
                                                    width=20, height=20)

        self.frame_entry_box_question_4.pack(padx=(10, 0), pady=5,
                                         side='top',
                                         anchor='nw')

        self.entry_box_question_4 = ScrolledText(self.frame_entry_box_question_4,
                                                 width=c.Size.txt_box_width,
                                                 height=c.Size.txt_box_height)

        self.entry_box_question_4.pack(padx=(10, 0), pady=5, side='top', anchor='nw')

        # --- Q5
        tk.Label(self.scrollable_labelframe.scrollable_frame,
                 text='Q5 - What is the number of beneficiaries of the impact?').pack(padx=(10, 0),
                                         side='top',
                                         anchor='nw')

        self.frame_entry_box_question_5 = ttk.Frame(self.scrollable_labelframe.scrollable_frame,
                                                    width=20, height=20)

        self.frame_entry_box_question_5.pack(padx=(10, 0), pady=5,
                                         side='top',
                                         anchor='nw')

        self.entry_box_question_5 = ScrolledText(self.frame_entry_box_question_5,
                                                 width=c.Size.txt_box_width,
                                                 height=c.Size.txt_box_height)

        self.entry_box_question_5.pack(padx=(10, 0), pady=5, side='top', anchor='nw')

        # --- Q6
        tk.Label(self.scrollable_labelframe.scrollable_frame,
                 text='Q6 - What is the level of impact on different individuals in the community?').pack(padx=(10, 0),
                                         side='top',
                                         anchor='nw')

        self.frame_entry_box_question_6 = ttk.Frame(self.scrollable_labelframe.scrollable_frame,
                                                    width=20, height=20)

        self.frame_entry_box_question_6.pack(padx=(10, 0), pady=5,
                                         side='top',
                                         anchor='nw')

        self.entry_box_question_6 = ScrolledText(self.frame_entry_box_question_6,
                                                 width=c.Size.txt_box_width,
                                                 height=c.Size.txt_box_height)

        self.entry_box_question_6.pack(padx=(10, 0), pady=5, side='top', anchor='nw')

        # --- Q7
        tk.Label(self.scrollable_labelframe.scrollable_frame,
                 text='Q7 - Is the impact in line with the goals of the development project?').pack(padx=(10, 0),
                                         side='top',
                                         anchor='nw')

        self.frame_entry_box_question_7 = ttk.Frame(self.scrollable_labelframe.scrollable_frame,
                                                    width=20, height=20)

        self.frame_entry_box_question_7.pack(padx=(10, 0), pady=5,
                                         side='top',
                                         anchor='nw')

        self.entry_box_question_7 = ScrolledText(self.frame_entry_box_question_7,
                                                 width=c.Size.txt_box_width,
                                                 height=c.Size.txt_box_height)

        self.entry_box_question_7.pack(padx=(10, 0), pady=5, side='top', anchor='nw')

        # --- pack scrollable frame
        self.scrollable_labelframe.pack(side="left", fill="both", expand=True)





    def check_if_data_loaded(self, update):

        if update:
            self.impact_evaluation.refresh_tree()

        # check if database has entries
        sql = "SELECT DISTINCT metric_id FROM metric_value"
        retrieve_sql = self.data_object.query_no_par(sql)

        if retrieve_sql:
            self.metric_results_window()
            self.status_message_show_metrics.set('')
        else:
            self.status_message_show_metrics.set('Please load data first!')

    def metric_results_window(self):

        if not self.popup_window_metrics:
            # create pop up window
            self.popup_window_metrics = tk.Toplevel()

            width = 1280
            height = 720
            position_left = 150
            position_right = 150

            self.popup_window_metrics.geometry("{}x{}+{}+{}".format(width, height, position_left, position_right))

            # set size window fixed
            self.popup_window_metrics.resizable(0, 0)

            self.popup_window_metrics.wm_title('Overview of metric results, goals and targets')

            # hide window if closed
            self.popup_window_metrics.protocol("WM_DELETE_WINDOW", lambda arg='popup': self.hide_window(arg))

            # add refresh button
            tk.Button(self.popup_window_metrics,
                      text='Refresh',
                      width=20, height=c.Size.button_height,
                      command=self.impact_evaluation.refresh_tree).pack(pady=(10,0))

            self.impact_evaluation.create_treeview(self.popup_window_metrics)

            # focus on window
            window_obj = w.Window()
            window_obj.focus_window(self.popup_window_metrics)

        else:
            self.popup_window_metrics.deiconify()

    def send_data_object(self, data):
        self.data_object = data
        self.impact_evaluation.get_data_object(self.data_object)

    def save_data(self):

        self.user_input_objects = [self.entry_box_metric.get('1.0', 'end-1c'),
                                   self.entry_box_target.get('1.0', 'end-1c'),
                                   self.entry_box_question_1.get('1.0', 'end-1c'),
                                   self.entry_box_question_2.get('1.0', 'end-1c'),
                                   self.entry_box_question_3.get('1.0', 'end-1c'),
                                   self.entry_box_question_4.get('1.0', 'end-1c'),
                                   self.entry_box_question_5.get('1.0', 'end-1c'),
                                   self.entry_box_question_6.get('1.0', 'end-1c'),
                                   self.entry_box_question_7.get('1.0', 'end-1c')]

        self.save_file_object.get_impact_evaluation(self.user_input_objects)

        for item in self.user_input_objects:
            print('Item: ', item)

    def send_save_file_object(self, data):
        self.save_file_object = data

    def hide_window(self, window):
        if window == "popup":
            self.popup_window_metrics.withdraw()

    def restore_from_save_file(self):

        self.entry_box_metric.insert('1.0', self.save_file_object.data['metric_evaluation'])
        self.entry_box_target.insert('1.0', self.save_file_object.data['target_evaluation'])
        self.entry_box_question_1.insert('1.0', self.save_file_object.data['eval_question_1'])
        self.entry_box_question_2.insert('1.0', self.save_file_object.data['eval_question_2'])
        self.entry_box_question_3.insert('1.0', self.save_file_object.data['eval_question_3'])
        self.entry_box_question_4.insert('1.0', self.save_file_object.data['eval_question_4'])
        self.entry_box_question_5.insert('1.0', self.save_file_object.data['eval_question_5'])
        self.entry_box_question_6.insert('1.0', self.save_file_object.data['eval_question_6'])
        self.entry_box_question_7.insert('1.0', self.save_file_object.data['eval_question_7'])









