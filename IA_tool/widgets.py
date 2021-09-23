
import tkinter as tk
from tkinter import ttk
from . import constants as c
from tkinter import filedialog
from . import models as m
from . import views as v
import webbrowser
from functools import partial
import csv

class FileOpener(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        global file_path
        file_path = ''
        self.file_path = file_path

    def show_project_goals(self):
        webbrowser.open(self.file_path)

    def get_file_path(self):
        filename = filedialog.askopenfilename()
        # print('Selected:', filename)
        self.file_path = filename

    def return_file_name(self):
        shown_text = "Filename: " + self.file_path.split("/")[-1]
        return shown_text

    def is_csv(self):
        if self.file_path.endswith('.csv'):
            return True
        else:
            return False

class FilePaths(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

    def get_dict(self, path_file):
        self.file_path_dict = path_file


class MethodFragmentSelection(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        self.mandatory_list = {'General project': True,
                               'General national': True,
                               'Demographic': True,
                               'General regional': True}

        self.chose_target_list = {'Student': 'student',
                             'Community School Leader': 'community_school_leader',
                             'Teacher': 'teacher',
                             'Project Provider': 'project_provider',
                             }

        self.checkbox_list = {}
        self.input_combobox = {}

        global selection_window
        self.selection_window = None

        global info_window
        self.info_window = None

        self.methode_frags_selected = False

    def show_selection_screen(self):

        if not self.selection_window:

            self.selection_window = tk.Toplevel()
            self.selection_window.wm_title('Select Method Fragments')

            width =  self.selection_window.winfo_screenwidth()
            height =  self.selection_window.winfo_screenheight()

            # self.selection_window.geometry('%sx%s' % (int(width-100), int(height)))

            self.selection_window.protocol("WM_DELETE_WINDOW", lambda arg='method_fragment': self.hide_window(arg))

            frame_method_fragments= ttk.LabelFrame( self.selection_window, text="1.3 - Select method fragments",
                                                 width=1200, height=400)
            frame_method_fragments.grid_propagate(0)
            frame_method_fragments.grid(padx=(10, 0),
                                     sticky='nsew')

            dataframe_object = m.surveyModel()
            dataframe = dataframe_object.dataframe

            # remove dataframe from function ?
            self.make_checkboxes(dataframe, frame_method_fragments)

            def select_check():
                self.generate_questions,
                self.show_info_screen(),
                self.selection_window.withdraw(),
                self.delete_frame(self.scrollable_metric_frame),
                self.delete_frame(self.add_metrics_frame),
                self.delete_frame(self.remove_frame),
                self.add_metric(),
                self.show_summary_metrics()
                self.methode_frags_selected = True

            # generate button
            button_confirm = tk.Button(frame_method_fragments,
                                        text='Confirm',
                                        width=c.Size.button_width, height=c.Size.button_height,
                                        command= lambda: [select_check(), self.reset_status_message()])

            button_confirm.grid(row=18, column=0,
                                 padx=(10, 0),
                                 pady=2,
                                 sticky='w')

        else:
            self.selection_window.deiconify()

    def send_status_message(self, message_1, message_2):
        self.reset_message_1 = message_1
        self.reset_message_2 = message_2

        print('send_status_message ------')

    def reset_status_message(self):
        self.reset_message_1['text'] = ''
        self.reset_message_2['text'] = ''

    def show_info_screen(self):

        if not self.info_window:
            self.info_window = tk.Toplevel()
            self.info_window.wm_title('Summary')

            width = self.info_window.winfo_screenwidth()
            height = self.info_window.winfo_screenheight()

            # self.info_window.geometry('%sx%s' % (int(width-100), int(height)))

            self.info_window.protocol("WM_DELETE_WINDOW", lambda arg='summary': self.hide_window(arg))

            self.make_summary_tabs()

            self.make_questions(refresh=False)

            # go to metric tab
            self.notebook_summary.select(0)


        else:
            self.notebook_summary.select(0)
            self.info_window.deiconify()

    def make_checkboxes(self, dataframe, frame):

        self.unique_values = dataframe.category.unique()

        amount_values = len(self.unique_values)

        counter = 0

        self.checkbox = dict()

        for item in self.unique_values:

            self.checkbox[item] = tk.Checkbutton(frame, text=item, onvalue=True, offvalue =False)
            self.checkbox[item].var = tk.BooleanVar()
            self.checkbox[item]['variable'] = self.checkbox[item].var

            if self.checkbox[item]['text'] in self.mandatory_list:
                self.checkbox[item]['variable'] = True
                self.checkbox[item].select()
                self.checkbox[item].config(state='disabled')

            if counter < int(amount_values/3):
                # print('Unique item: ', item)
                counter += 1
                self.checkbox[item].grid(row=counter, sticky='w')

            elif counter < int(amount_values/3 * 2):
                counter += 1
                self.checkbox[item].grid(row=counter - int(amount_values/3), column=1 , sticky='w')
            else:
                counter += 1
                self.checkbox[item].grid(row=(counter - int(amount_values/3 * 2)), column=2, sticky='w')

            self.checkbox[item]['command'] = lambda w=self.checkbox[item]: self.send_category_object(w['text'], w.var.get())


        # set mandatory fragments as always true
        for item in self.mandatory_list:
            self.append_value(self.checkbox_list, item, True)

    def selected_method_fragments(self, checkbox_state, checkbox_name):

        self.append_value(self.checkbox_list, checkbox_name, checkbox_state)

    def append_value(self, dict_object, key, value):
        # Check if key exist in dict or not
        if key in dict_object:
            # Key exist in dict.
            # Check if type of value of key is list or not
            if not isinstance(dict_object[key], list):
                # if key in list, only change value
                dict_object[key] = value
                if dict_object[key] == False:
                    dict_object.pop(key)

        else:
            # As key is not in dict,
            # so, add key-value pair
            dict_object[key] = value

    def send_category_object(self, key, value):
        self.key = key
        self.value = value

        self.selected_method_fragments(self.value, self.key)

    def generate_questions(self):
        # hide select method fragment screen to show questions
        self.hide_window('method_fragment')

    def retrieve_frame(self, frame):
        self.frame = frame

    def hide_window(self, window):

        if window == "method_fragment":
            self.selection_window.withdraw()
        elif window == "summary":
            self.info_window.withdraw()

    def add_metric(self):

        # todo add input validation to the metric entry field and combo boxes
        # todo add input validation to the remove metric for enter frag id and enter metric id and combo boxes

        self.add_metrics_frame = ttk.LabelFrame(self.tab_metrics, text="Add metric",
                                                width=600, height=300)

        self.add_metrics_frame.pack(fill="both")

        self.remove_frame = ttk.LabelFrame(self.tab_metrics, text="Remove metric",
                                           width=600, height=300)

        self.remove_frame.pack(fill="both")


        labels = ['Metric', 'Method fragment', 'Data type']

        check_list = list(self.checkbox_list.keys())
        # print(("check_box_list ----- ", check_list))

        # only retrieve the method fragments that were checked (to show in the combobox)
        sql = "select method_fragment_name from method_fragment where method_fragment_name in ({seq})".format(
            seq=','.join(['?'] * len(check_list)))



        retrieve_method_fragment = self.data_object.query_with_par(sql, check_list)
        retrieve_method_fragment_string = []

        retrieve_datatypes = self.data_object.query_no_par(
            "SELECT DISTINCT metric_value_type FROM metric ORDER BY metric_value_type")

        # turn tuple into string to put in combo list
        def retrieve_method_fragment_str():
            for value in retrieve_method_fragment:
                retrieve_method_fragment_string.append(value[0])

        retrieve_method_fragment_str()

        # make labels and input boxes for metric, method fragment and data type
        for index, value in enumerate(labels):
            ttk.Label(self.add_metrics_frame,
                      anchor="w", justify='left',
                      font='Helvetica 11',
                      text=value).grid(row=0, column=index + index,
                                       padx=10, pady=(20, 10))

            # input boxes
            if index == 0:
                # textbox metric
                user_metric = tk.StringVar()
                user_metric_input = ttk.Entry(self.add_metrics_frame, width=15, textvariable=user_metric)
                user_metric_input.grid(row=0, column=(index + index +1),
                                       padx = 10, pady=(20, 10))
            elif index == 1:
                # combobox: method fragment
                combobox = ttk.Combobox(
                    self.add_metrics_frame,
                    state="readonly",
                    values=retrieve_method_fragment_string)
                combobox.grid(row=0, column=(index + index +1),
                                       padx = 10, pady=(20, 10))
            else:
                # combobox: data types
                combobox_2 = ttk.Combobox(
                    self.add_metrics_frame,
                    state="readonly",
                    values=retrieve_datatypes)
                combobox_2.grid(row=0, column=(index + index +1),
                                       padx = 10, pady=(20, 10))

        button_add = tk.Button(self.add_metrics_frame,
                               text='Add',
                               width=c.Size.button_width, height=c.Size.button_height,
                               command=lambda: [self.add_button(combobox, combobox_2, user_metric, user_survey_question, combobox_target)])

        button_add.grid(row=0, column=6,
                                   padx = 10, pady=(20, 10))

        ttk.Label(self.add_metrics_frame,
                  anchor="w", justify='left',
                  font='Helvetica 11',
                  text='Survey question').grid(row=1, column=0,
                                   padx=10, pady=(0, 20))

        # textbox survey question
        user_survey_question = tk.StringVar()
        user_survey_question_input = ttk.Entry(self.add_metrics_frame, width=57, textvariable=user_survey_question)
        user_survey_question_input.grid(row=1, column=1, columnspan=5, sticky='w',
                               padx=10, pady=(0, 20))

        # label for target to ask to
        ttk.Label(self.add_metrics_frame,
                  font='Helvetica 11',
                  text='Ask to: ').grid(row=1, column=4,
                                        columnspan=20,
                                        padx=10, pady=(0, 20),
                                        sticky='w')

        # combobox: Ask to
        combobox_target = ttk.Combobox(
            self.add_metrics_frame,
            state="readonly",
            values=["Project Provider",
                    "Community School Leader",
                    "Teacher",
                    "Student"
                    ])
        combobox_target.grid(row=1, column=5,
                        padx=10, pady=(0, 20))

        # Placeholder for status message
        self.status_message_add_metric = tk.StringVar()
        self.status_message_add_metric.set("")

        self.status_message_label = ttk.Label(self.add_metrics_frame,
                  font='Helvetica 11', foreground='red',
                  textvariable=self.status_message_add_metric)

        self.status_message_label.grid(row=2, column=0,
                                                            columnspan=20,
                                                            padx=10, pady=(0, 20),
                                                            sticky='w')

        # remove metric

        # todo popup window for removal of metric
        ttk.Label(self.remove_frame,
                  anchor="w", justify='left',
                  font='Helvetica 11',
                  text='Enter metric id: ').grid(row=0, column=0, sticky='w',
                               padx=10, pady=(10, 10))

        # textbox remove method fragment
        user_method_remove = tk.StringVar()
        user_method_remove_input = ttk.Entry(self.remove_frame, width=15, textvariable=user_method_remove)
        user_method_remove_input.grid(row=0, column=1, sticky='w',
                               padx=10, pady=(20, 10))

        # remove button
        button_remove = tk.Button(self.remove_frame,
                                  text='Remove',
                                  width=c.Size.button_width, height=c.Size.button_height,
                                  command=lambda: [self.remove_button(user_method_remove)])

        button_remove.grid(row=0, column=4, sticky='w',
                               padx=10, pady=(20, 10))

        # Placeholder for status message
        self.status_message_remove_metric = tk.StringVar()
        self.status_message_remove_metric.set("")
        self.remove_label = ttk.Label(self.remove_frame,
                  font='Helvetica 11', foreground='red',
                  textvariable=self.status_message_remove_metric)

        self.remove_label.grid(row=1, column=0, columnspan=20,
                                                            padx=10, pady=(0, 20),
                                                               sticky='w')

    def add_button(self, method_frag_input, data_type_input, metric_input, user_survey_question, combobox_target):

        # todo link user added metric to metrics list
        # todo add validation for input boxes
        # todo show text for confirmation that metric is added

        method_frag_input.current()
        data_type_input.current()
        combobox_target.current()

        method_frag_input.get()
        data_type_input.get()
        combobox_target.get()

        # print('METRIC TEXT BOX: ', metric_input.get())
        # print('METHOD FRAG BOX: ', method_frag_input.get())
        # print('DATATYPE BOX: ', data_type_input.get())
        # print('SURVEY QUESTION BOX: ', user_survey_question.get())

        if metric_input.get() and method_frag_input.get() and data_type_input.get() and user_survey_question.get():

            sql_retrieve_method_frag_id = "select method_fragment_id from method_fragment where method_fragment_name=?"
            retrieve_method_frag_id = self.data_object.query_with_par(sql_retrieve_method_frag_id, ((method_frag_input.get()),))

            metric_name = metric_input.get()
            method_fragment_id = retrieve_method_frag_id[0][0]
            metric_definition = None
            metric_question = user_survey_question.get()
            metric_value_type = data_type_input.get()
            multiple_answers = None
            answer_options = None
            target_name = self.chose_target_list[combobox_target.get()]
            user_made = True

            metric = (metric_name, method_fragment_id, metric_definition, metric_question, metric_value_type, multiple_answers, answer_options, target_name, user_made)

            # print('Metric_name ---------', metric)

            self.data_object.create_metric(metric)

            # reset input boxes
            method_frag_input.set('')
            data_type_input.set('')
            combobox_target.set('')

            metric_input.set('')
            user_survey_question.set('')

            self.status_message_label.config(foreground='green')
            self.status_message_add_metric.set("Metric " + metric_name + ' added!')

            # update frame to show status message
            self.add_metrics_frame.update()
            self.add_metrics_frame.update()

            # after 1 sec refresh screen
            self.status_message_label.after(1500, self.refresh_summary_window())


        else:
            self.status_message_add_metric.set("Please fill in every box!")

    def remove_button(self, frag_id):

        # todo link user added metric to metrics list
        # todo add validation for input boxes
        # todo show text for confirmation that metric is added

        if frag_id.get():

            try:
                frag_id_int = int(frag_id.get())

            except ValueError:
                self.status_message_remove_metric.set("Please only fill in numbers!")
                return

            if frag_id_int <= self.total_amount:

                frag_id_int_user = int((frag_id.get()),)
                frag_id_in_db = self.metric_id_list[frag_id_int_user-1]

                # print('frag_id_int_user ----------- ', frag_id_int_user)
                # print('self.metric_id_list[frag_id_int_user] ----------- ', self.metric_id_list[frag_id_int_user - 1])

                sql_check = "select user_made from metric where metric_id = ?"
                retrieve_check = self.data_object.query_with_par(sql_check, ((frag_id_in_db),))

                sql_delete_metric = "delete from metric where metric_id = ?"

                # print('retrieve_check ------ ', retrieve_check[0][0])

                if retrieve_check[0][0] == False:
                    print('Standard metric, do not remove ----------')

                else:

                    # try
                    try:
                        # remove metric target
                        sql_target_check = "select metric_id from metric_target where metric_id = ?"

                        self.data_object.query_with_par(sql_target_check, ((frag_id_in_db),))

                        sql_target_delete = "delete from metric_target where metric_id = ?"

                        self.data_object.delete_row_with_par(sql_target_delete, frag_id_in_db)

                    except:
                        print('Metric target not found')

                    # if metric target is already gone/non existant, remove metric
                    self.data_object.delete_row_with_par(sql_delete_metric, frag_id_in_db)
                    print('User metric, removed! ----------')

                # print('self.metric_id_list ----------- ', self.metric_id_list)

                # reset
                frag_id.set('')

                self.remove_label.config(foreground='green')
                self.status_message_remove_metric.set("Metric removed!")

                self.remove_frame.update()

                self.remove_frame.after(1000, self.refresh_summary_window())

            else:
                self.status_message_remove_metric.set("Please fill in an existing ID!")

        else:
            self.status_message_remove_metric.set("Please fill in an ID!")

    def get_target(self, event=None):
        self.input_combobox = event.widget.get()

        target_key = self.chose_target_list[self.input_combobox]

        if self.community_list is not None:
            self.community_list.delete('0', tk.END)
            self.metric_counter_label.set('')

        self.create_list(target_key)

    def create_list(self, target_key):

        # todo rewrite to link with db
        self.dataframe = m.surveyModel()

        label_survey_questions_community = tk.Label(self.frame_survey_questions,
                                                    text='Generated questions for: ')

        label_survey_questions_community.grid(row=4, column=0,
                                              padx=(20, 0),
                                              pady=(10, 0),
                                              sticky='w')

        scrollbar_v_community_list = tk.Scrollbar(self.frame_survey_questions)
        scrollbar_h_community_list = tk.Scrollbar(self.frame_survey_questions)

        self.community_list = tk.Listbox(self.frame_survey_questions, yscrollcommand=scrollbar_v_community_list.set,
                                         xscrollcommand=scrollbar_h_community_list.set,
                                         width=140, height=15)

        scrollbar_v_community_list.grid(row=6, column=1, sticky='ns')
        scrollbar_h_community_list.grid(row=7, column=0, sticky='we')

        self.community_list.grid(row=6, column=0,
                                 padx=(10, 0),
                                 pady=2,
                                 sticky='nswe')

        scrollbar_v_community_list.config(command=self.community_list.yview)
        scrollbar_h_community_list.config(command=self.community_list.xview)

        metric_counter = 0
        self.metric_counter_label = tk.StringVar()
        self.metric_counter_label.set('')

        # Listbox with all the survey questions per target group
        for index, value in enumerate(self.checkbox_list):

            # todo add demographic of interest and scope
            # retrieve method fragment id from checked methods fragments
            sql_retrieve_method_frag_id = "select method_fragment_id from method_fragment where method_fragment_name=?"
            retrieve_method_frag_id = self.data_object.query_with_par(sql_retrieve_method_frag_id, ((value),))

            # retrieve metrics from the method fragments
            sql_retrieve_metrics = "select * from metric where method_fragment_id=(?) and target_name=(?)"
            retrieve_metrics = self.data_object.query_with_par(sql_retrieve_metrics, (retrieve_method_frag_id[0][0], target_key))

            # provider_metric_counter =
            # leader_metric_counter =
            # teacher_metric_counter =
            # student_metric_counter =

            metric_counter = metric_counter + len(retrieve_metrics)

            print('metric_counter ------ ', metric_counter)

            for metric_index, metric in enumerate(retrieve_metrics):

                self.community_list.insert(tk.END, ' ' + 'Survey question:   ' + str(metric[4]))
                self.community_list.insert(tk.END, '                ' + 'Metric:   ' + str(metric[1]))
                self.community_list.insert(tk.END, '                   ' + 'Type:   ' + str(metric[5]))
                self.community_list.insert(tk.END, '                   ' + 'Code:   ' + str(metric[2]))
                self.community_list.insert(tk.END, '\n')

        self.metric_counter_label.set("Amount of questions:  " + str(metric_counter))

        tk.Label(self.frame_survey_questions,
                 textvariable= self.metric_counter_label,
                 font='Helvetica 11').grid(row=10, column=0,
                                               padx=(20, 0),
                                               pady=(0,10),
                                               sticky='w')

        button_go_to_add_metrics = tk.Button(self.frame_survey_questions,
                                        text='Add additional metrics',
                                        height=c.Size.button_height,
                                        command=lambda: [self.notebook_summary.select(0)])

        button_go_to_add_metrics.grid(row=11, column=0,
                                 padx=(10, 0),
                                 sticky='w')

    def make_summary_tabs(self):

        # make notebook
        self.notebook_summary = ttk.Notebook(self.info_window)

        # make tabs
        self.tab_metrics = ttk.Frame(self.info_window, width=1200, height=600)
        self.tab_metrics.grid(row=0, column=0,
                              padx=(10, 0),
                              sticky='nsew')

        self.tab_questions = ttk.Frame(self.info_window, width=1200, height=600)
        self.tab_questions.grid_propagate(0)
        self.tab_questions.grid(padx=(10, 0),
                                sticky='nsew')

        # self.tab_metric_definition = ttk.Frame(self.info_window, width=1200, height=800)
        # self.tab_metric_definition.grid_propagate(0)
        # self.tab_metric_definition.grid(padx=(10, 0),
        #                         sticky='nsew')

        # make label frames
        self.summary_metrics = ttk.LabelFrame(self.tab_metrics,
                                              text="Summary of all metrics",
                                              width=600, height=400)
        self.summary_metrics.pack(fill="both", expand=True)

        self.add_metrics_frame = ttk.LabelFrame(self.tab_metrics,
                                                text="Add metric",
                                                width=600, height=200)
        self.add_metrics_frame.pack(fill="both")

        self.remove_frame = ttk.LabelFrame(self.tab_metrics, text="Remove metric",
                                           width=600, height=200)
        self.remove_frame.pack(fill="both")

        # initiate summary_metrics scrollable
        self.scrollable_metric_frame = ScrollableFrame(self.summary_metrics)

        # add tabs to notebook
        self.notebook_summary.add(self.tab_metrics, text='Metrics')
        # self.notebook_summary.add(self.tab_metric_definition, text='Metric Definitions')
        self.notebook_summary.add(self.tab_questions, text='Survey Questions')
        self.notebook_summary.grid(row=0, column=0, sticky='E', padx=5, pady=5, ipadx=5, ipady=5)

    def make_questions(self, refresh):

        if refresh == False:
            self.frame_survey_questions = ttk.LabelFrame(self.tab_questions, text="Survey questions",
                                                         width=1200, height=600)

            self.frame_survey_questions.grid_propagate(0)
            self.frame_survey_questions.grid(padx=5, pady=5,
                                             sticky='e')


            self.create_list('project_provider')

            self.combobox_target_survey = ttk.Combobox(
                self.frame_survey_questions,
                state="readonly",
                values=["Project Provider",
                        "Community School Leader",
                        "Teacher",
                        "Student"
                        ])

            self.combobox_target_survey.current(0)

            self.combobox_target_survey.grid(row=5, column=0, padx=(20, 0), pady=(0,10),
                                             sticky='w')

            self.combobox_target_survey.bind("<<ComboboxSelected>>", self.get_target)
        else:
            self.create_list('')


    def show_summary_metrics(self):

        # frame summary_metrics scrollable
        self.scrollable_metric_frame = ScrollableFrame(self.summary_metrics)

        self.metric_id_list = []

        amount_of_frags = len(self.checkbox_list)
        amount_of_metrics = 0
        counter = 0

        stat_label_frags = ttk.Label(self.scrollable_metric_frame.scrollable_frame,
                               anchor="w", justify='left',
                               font='Helvetica 11 ',
                               text='Total amount of method fragments:   ' + str(
                                   amount_of_frags))

        stat_label_frags.pack(fill='both', pady=(10, 0))

        stat_label_metric = ttk.Label(self.scrollable_metric_frame.scrollable_frame,
                               anchor="w", justify='left',
                               font='Helvetica 11 ',
                               text='Total amount of metrics:   ' + str(
                                   amount_of_metrics))

        stat_label_metric.pack(fill='both', pady=(0, 10))

        for index, value in enumerate(self.checkbox_list):
            # print("show_summary_metrics: VALUE: ", value)
            # print("show_summary_metrics: type of VALUE: ", type(value[0]))

            # retrieve method fragment id from checked methods fragments
            sql_retrieve_method_frag_id = "select method_fragment_id from method_fragment where method_fragment_name=?"
            retrieve_method_frag_id = self.data_object.query_with_par(sql_retrieve_method_frag_id, ((value),))

            # retrieve metrics from the method fragments
            sql_retrieve_metrics = "select * from metric where method_fragment_id=?"
            retrieve_metrics = self.data_object.query_with_par(sql_retrieve_metrics, retrieve_method_frag_id[0])

            amount_of_metrics += len(retrieve_metrics)

            if index == (len(self.checkbox_list) - 1):
                stat_label_frags['text'] = 'Total amount of method fragments: ' + str(
                                   amount_of_frags)
                stat_label_metric['text'] = 'Total amount of metrics:   ' + str(
                                   amount_of_metrics)

                self.total_amount = amount_of_metrics

            ttk.Label(self.scrollable_metric_frame.scrollable_frame,
                      anchor="w", justify='left',
                      font='Helvetica 10 bold',
                      text=value).pack(fill='both')

            for metric_index, metric in enumerate(retrieve_metrics):

                ttk.Label(self.scrollable_metric_frame.scrollable_frame,
                          anchor="w", justify='left',
                          text= '    ' + str(counter+1) + '  - ' + str(metric[1])).pack(fill='both')
                counter += 1

                # print('ID ------', metric[0])
                self.metric_id_list.append(metric[0])

        self.scrollable_metric_frame.pack(side="left", fill="both", expand=True)


    def get_data_object(self, data):
        self.data_object = data

        # print("--- get_data_object - Check")

    def delete_frame(self, frame):

        if frame is not None:
            frame.pack_forget()
            frame.destroy()

    def refresh_summary_window(self):

        self.combobox_target_survey.delete(0, 'end')
        self.make_questions(refresh=True)
        self.generate_questions()
        self.show_info_screen()
        self.selection_window.withdraw()
        self.delete_frame(self.scrollable_metric_frame)
        self.delete_frame(self.add_metrics_frame)
        self.delete_frame(self.remove_frame)
        self.add_metric()
        self.show_summary_metrics()
        self.notebook_summary.select(0)

        # print("REFRESH SUMMARY WINDOW ------ ")

    def show_add_metric_definition_window(self):

        # make pop up window
        self.add_metric_window = tk.Toplevel()
        self.add_metric_window.wm_title('Add metric definitions')

        # set dimensions window
        width = 1200
        height = 800
        self.add_metric_window.geometry("{}x{}".format(width, height))

        # make frame scrollable
        self.scrollable_add_metric_frame = ScrollableFrame(self.add_metric_window)

        self.metric_id_list = []
        self.button_id_list = []
        self.user_metric_defintion_text_widget = []
        self.user_metric_defintion_text = []
        self.checkbox_demographic = []
        self.checkbox_demographic_var = []
        self.metric_id_holder = []

        self.demo_scope_list = []
        self.metric_target_list = []
        self.if_increase_list = []

        self.status_message_list = []

        counter = 0

        for index, value in enumerate(self.checkbox_list):
            # print("show_summary_metrics: VALUE: ", value)
            # print("show_summary_metrics: type of VALUE: ", type(value[0]))

            # make frame
            metric_frame = ttk.Frame(self.scrollable_add_metric_frame.scrollable_frame, width=1200, height=800)

            # retrieve method fragment id from checked methods fragments
            sql_retrieve_method_frag_id = "select method_fragment_id from method_fragment where method_fragment_name=?"
            retrieve_method_frag_id = self.data_object.query_with_par(sql_retrieve_method_frag_id, ((value),))

            # retrieve metrics from the method fragments
            sql_retrieve_metrics = "select * from metric where method_fragment_id=?"
            retrieve_metrics = self.data_object.query_with_par(sql_retrieve_metrics, retrieve_method_frag_id[0])

            # for metric in retrieve_metrics:
            #     print(' ID: retrieve_metrics[0] -------------- ', metric[0][metric_index])
            #     print(' Name: retrieve_metrics[1] -------------- ', metric[1][metric_index])

            ttk.Label(metric_frame,
                      anchor="w", justify='left',
                      font='Helvetica 14', foreground='blue',
                      text=value).pack(fill='both', pady=10)

            for metric_index, metric in enumerate(retrieve_metrics):

                # print(' ID: retrieve_metrics[0] -------------- ', metric[0])
                # print(' ID: retrieve_metrics[0] -------------- ', metric[0][metric_index])
                # print(' Name: retrieve_metrics[1] -------------- ', metric[1][metric_index])

                # print('retrieve_metric_target ------', metric[0])


                ttk.Label(metric_frame,
                          anchor="w", justify='left',
                          font='Helvetica 10 bold',
                          text='    ' + 'Metric: ').pack(fill='both')

                ttk.Label(metric_frame,
                          anchor="w", justify='left',
                          text=str(metric[1])).pack(anchor='w', padx=(40,0))

                self.metric_id_holder.append(metric[1])

                ttk.Label(metric_frame,
                          anchor="w", justify='left',
                          font='Helvetica 10 bold',
                          text='    ' + 'Target group: ').pack(fill='both')

                ttk.Label(metric_frame,
                          anchor="w", justify='left',
                          text=str(metric[8])).pack(anchor='w', padx=(40, 0))

                ttk.Label(metric_frame,
                          anchor="w", justify='left',
                          font='Helvetica 10 bold',
                          text='    ' + 'Metric definition: ').pack(fill='both', pady=(0, 5))

                user_metric_definition_input = tk.StringVar()
                user_metric_definition = ttk.Entry(metric_frame,
                                                   width=15,
                                                   textvariable=user_metric_definition_input).pack(fill='both', padx=(40,0), pady=(0, 5))
                if metric[3] is not None:
                    user_metric_definition_input.set(str(metric[3]))

                # todo rewrite to only show when metric_definition is not None

                button_reset = tk.Button(metric_frame,
                                   text='Reset metric definition',
                                   state = 'disabled',
                                   height=1,
                                   command=partial(self.reset_user_def, counter))

                button_reset.pack(pady=(0), anchor="e", padx=(20, 0))

                ttk.Label(metric_frame,
                          anchor="w", justify='left',
                          font='Helvetica 10 bold',
                          text='    ' + 'Set metric target in %: ').pack(fill='both', pady=(0, 5))

                user_target_input = tk.StringVar()
                user_target = ttk.Entry(metric_frame,
                                            width=10,
                                            textvariable=user_target_input).pack(anchor='w', padx=(40,0), pady=(0, 5))

                ttk.Label(metric_frame,
                          anchor="w", justify='left',
                          font='Helvetica 10 bold',
                          text='    ' + 'Target increase or decrease: ').pack(fill='both', pady=(0, 5))

                combobox = ttk.Combobox(
                    metric_frame,
                    width=15,
                    state="readonly",
                    values=["Increase",
                            "Decrease"
                            ])

                combobox.pack(anchor='w', pady=(0, 5), padx=(40,0))

                self.metric_id_holder[counter] = tk.BooleanVar()
                checkbox_demographic = ttk.Checkbutton(metric_frame,
                                           text='Demographic of interest',
                                           variable=self.metric_id_holder[counter],
                                           onvalue=True, offvalue=False)

                checkbox_demographic.pack(anchor="w", padx=(10,0), pady=(0, 5))

                self.checkbox_demographic.append(self.metric_id_holder[counter])

                ttk.Label(metric_frame,
                          anchor="w", justify='left',
                          font='Helvetica 10 bold',
                          text='    ' + 'Demographic scope: ').pack(fill='both', pady=(0, 5))

                user_demo_scope_input = tk.StringVar()
                user_demo_scope = ttk.Entry(metric_frame,
                                                   width=15,
                                                   textvariable=user_demo_scope_input).pack(fill='both', padx=(40,0), pady=(0, 5))

                status_message = tk.StringVar()
                ttk.Label(metric_frame,
                          anchor="w", justify='left',
                          font='Helvetica 10 bold', foreground='red',
                          textvariable=status_message).pack(fill='both', padx=(40,0), pady=(0, 5))

                button = tk.Button(metric_frame,
                                   text='Save',
                                   width=c.Size.button_width, height=c.Size.button_height,
                                   command=partial(self.save_metric_stats, counter)).pack(pady=(10,0), anchor="w", padx=(20,0))

                # retrieve method fragment id from checked methods fragments
                sql_retrieve_metric_target = "select * from metric_target where metric_id = (?)"
                retrieve_metric_target = self.data_object.query_with_par(sql_retrieve_metric_target, [metric[0]])

                # check if array is not empty
                if retrieve_metric_target:
                    print('retrieve_metric_target| ALL ------', retrieve_metric_target)
                    print('retrieve_metric_target| if_increased ------', retrieve_metric_target[0][1])
                    print('retrieve_metric_target| metric_target_value ------', retrieve_metric_target[0][2])
                    print('retrieve_metric_target| if_interest_demographic ------', retrieve_metric_target[0][3])
                    print('retrieve_metric_target| interest_scope ------', retrieve_metric_target[0][4])

                    button_reset['state'] = 'active'

                    # if in database pre fill the fields
                    user_target_input.set(str(retrieve_metric_target[0][2]))

                    if retrieve_metric_target[0][1]:
                        combobox.current(1)

                    if retrieve_metric_target[0][3]:
                        self.metric_id_holder[counter].set(True)

                    user_demo_scope_input.set(str(retrieve_metric_target[0][4]))

                self.metric_id_list.append(metric[0])
                self.button_id_list.append(button)
                self.user_metric_defintion_text.append(user_metric_definition_input)
                self.demo_scope_list.append(user_demo_scope_input)
                self.metric_target_list.append(user_target_input)
                self.if_increase_list.append(combobox)
                self.status_message_list.append(status_message)

                counter += 1

                # white line
                ttk.Label(metric_frame, text='').pack()

            metric_frame.pack(fill='both')

        # print('button_id_list ---------- ', len(self.button_id_list))
        # print('METRIC ITEM LIST', self.metric_id_list)

        # put scrollable frame in window
        self.scrollable_add_metric_frame.pack(fill="both", expand='true')

    def reset_user_def(self, index):

        self.user_metric_defintion_text[index].set('')
        reset_def = None

        sql_update_definition = "update metric set metric_definition = (?) where metric_id = (?)"
        self.data_object.update_row_with_par(sql_update_definition, (reset_def,
                                                                     self.metric_id_list[index]))

    def save_metric_stats(self, index):

        # todo remove project id hardcode

        self.if_increase_list[index].current()

        self.data_object.send_parameter((self.metric_target_list[index].get(),
                                        self.if_increase_list[index].get(),
                                        self.checkbox_demographic[index].get(),
                                        self.demo_scope_list[index].get(),
                                        self.metric_id_list[index]))

        # update metric target if there is input
        if self.metric_target_list[index].get() != '' and self.if_increase_list[index].get() != '':

            try:
                metric_target_int = int(self.metric_target_list[index].get())
                print('Metric target ------ ', metric_target_int)

            except ValueError:
                # self.status_message_remove_metric.set("Please only fill in numbers!")
                self.status_message_list[index].set('Error, please only fill in numbers for metric target!')
                return

            if self.if_increase_list[index].get() == "Incease":
                isIncrease = True
            else:
                isIncrease = False

            # update metric_def if there is user_input
            if self.user_metric_defintion_text[index].get() != '':
                sql_update_definition = "update metric set metric_definition = (?) where metric_id = (?)"

                self.data_object.update_row_with_par(sql_update_definition,
                                                     (self.user_metric_defintion_text[index].get(),
                                                      self.metric_id_list[index]))


            metric_target = int(self.metric_target_list[index].get())
            metric_id = self.metric_id_list[index]

            interest_demographic = self.checkbox_demographic[index].get()
            interest_scope = self.demo_scope_list[index].get()

            if interest_demographic == '':
                interest_scope = None

            # un hardcode project_id !
            target = (isIncrease, metric_target, interest_demographic, interest_scope, 1, metric_id)
            self.data_object.create_metric_target(target)
            self.status_message_list[index].set('')

        else:
            self.status_message_list[index].set('Error, please fill both the metric target and target increase/decrease in!')

        # print('save_metric_stats| button index ---- ', index)
        # print('save_metric_stats| metric definition ---- ', self.user_metric_defintion_text[index].get())
        # print('save_metric_stats| metric_id ---- ', self.metric_id_list[index])
        # print('save_metric_stats| checkbox ---- ', self.checkbox_demographic[index].get())
        # print('save_metric_stats| demographic scope ---- ', self.demo_scope_list[index].get())
        # print('save_metric_stats| target ---- ', self.metric_target_list[index].get())
        # print('save_metric_stats| if increase ---- ', self.if_increase_list[index].get())

class DataCollection(tk.Frame):

    # get the dict with paths
    def get_dict_paths(self, data):
        self.dict_paths = data


class DataAnalysis(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

    # get data
    def get_data_object(self, data):
        self.data_object = data

    def get_paths_dict(self, dict):
        self.paths_dict = dict

    def load_in_paths(self, dict):
        self.paths = dict

    def load_into_database(self, dict):


        counter = 0

        # check in the dict what the target is for each item
        def target_check(item):
            if item.endswith('provider'):
                return 'project_provider'

            elif item.endswith('leader'):
                return 'community_school_leader'

            elif item.endswith('teacher'):
                return 'teacher'

            else:
                return 'student'

        def data_type_check(value):

            if isinstance(value, int) or isinstance(value, float):
                return value

            elif isinstance(value, str):
                cleaned_value = (value.lower()).strip()
                return cleaned_value

        # loop through dict and extract the data from the valid paths
        for id, item in enumerate(dict):
            # print('Key: ', path)
            # print('Value: ',dict[path])

            # variables for the SQL query
            measuring_point_id = None
            metric_id = None
            file_id = id
            data_bool = None
            data_str = None
            data_int = None
            data_float = None

            target = None

            # non valid paths
            if dict[item] == '':
                print(item, ': No path')

            else:
                # check which target group the file is for
                target = target_check(item)

                # extract the measuring point
                if item.startswith('sop'):
                    measuring_point_id = 0

                elif item.startswith('hop'):
                    measuring_point_id = 1

                elif item.startswith('eop'):
                    measuring_point_id = 2

                else:
                    measuring_point_id = 3

                # print('file ID = ', file_id)
                # print('Target: ', item)
                # print('Path: ', dict[item])

                # open the valid paths and extract the data
                with open(dict[item], newline='\n') as f:

                    reader = csv.DictReader(f, delimiter=',')

                    # get header names
                    metric_list = reader.fieldnames

                    print('Metric List: ', metric_list)

                    # each survey in the csv file (1 row = 1 survey)
                    for index, row in enumerate(reader):

                        # print("ROWWW -- ",row)
                        # print('Index: ', index)
                        # print('-----')

                        # loop through the non-header rows
                        for metric_index, item in enumerate(row):

                            # skip non relevant headers
                            if metric_index in range(0,10):
                                continue

                            # extract relevant data and save in database
                            else:

                                metric_name = ((metric_list[metric_index]).lower()).strip()
                                target_name = (target.lower()).strip()

                                # TODO check if it works with strings!
                                metric_value_data = data_type_check(row[metric_list[metric_index]])

                                print('-----')
                                print('Metric: ', metric_name)
                                print('Metric Value: ', metric_value_data)
                                print('Target Name: ', target_name)

                                sql_metrics = "select * from metric where lower(metric_name) = (?) and lower(target_name) = (?)"
                                retrieve_metrics = self.data_object.query_with_par(sql_metrics, (metric_name, target_name))

                                for metric_item in retrieve_metrics:
                                    counter += 1
                                    metric_id = metric_item[0]

                                    metric_data_type = ((metric_item[5]).lower()).strip()

                                    print(metric_data_type)

                                metric_value = (measuring_point_id,
                                                metric_id,
                                                file_id,
                                                data_bool,
                                                data_str,
                                                data_int,
                                                data_float)

                                print('Metric_value DATABASE', metric_value)
                                print('-----')
        print(counter)



                #
                #     # print('Metric ID: --- ', metric_id)
                #     # print('Metric Name: --- ', metric_name)

    def make_table(self, frame, timeframe, target):

        print('Paths --- ', self.paths_dict.file_path_dict)


        #TODO unhardcode path
        hardcoded_file_path = 'C:/Users/Tiny/Desktop/test 1 - csv.csv'

        #TODO only execute once

        # make treeview frame
        TableMargin = tk.Frame(frame, width=1200, height=500)
        TableMargin.pack(side="top", fill="both", expand='True')

        self.scrollbary = tk.Scrollbar(TableMargin, orient='vertical')
        self.scrollbarx = tk.Scrollbar(TableMargin, orient='horizontal')

        # make tree
        self.tree = ttk.Treeview(TableMargin,
                                 columns=("Metric ID", "Metric Name", "Method ID"),
                                 selectmode="extended",
                                 yscrollcommand=self.scrollbary.set,
                                 xscrollcommand=self.scrollbarx.set,
                                 height=400)

        self.scrollbary.config(command=self.tree.yview)
        self.scrollbary.pack(side="right", fill="y")

        self.scrollbarx.config(command=self.tree.xview)
        self.scrollbarx.pack(side="bottom", fill="both", expand='True')

        # make tree headings
        self.tree.heading('Metric ID', text="Metric ID", anchor='w')
        self.tree.heading('Metric Name', text="Metric Name", anchor='w')
        self.tree.heading('Method ID', text="Method ID", anchor='w')

        # make tree columns
        self.tree.column('#0', stretch='no', minwidth=0, width=0)
        self.tree.column('#1', stretch='no', minwidth=0, width=400)
        self.tree.column('#2', stretch='no', minwidth=0, width=400)

        # place tree
        self.tree.pack(fill='both',
                       padx=10)

        # open CSV and load in headers
        with open(hardcoded_file_path, "rt") as f:
            reader = csv.reader(f)
            header = next(reader)
            # print(header)

        # clean column names
        column_names = []

        header_list = list(header)
        # print('header list ---', header_list)


        # for export_code in header_list:
        #     column_names.append(export_code.replace("\n", '-'))

        # print('Column Names --- ',column_names[0])

        # load csv into database

        # extract export code

        # clean column name, Survey question: , lower/upper case, spacebars, dots

        #         for index, value in enumerate(labels):
        counter_test = 0

        # test with metric table, show metric_id, metric_name and method_fragment_id
        sql_metrics = "select * from metric"
        retrieve_metrics = self.data_object.query_no_par(sql_metrics)

        for metric in retrieve_metrics:
            metric_id = metric[0]
            metric_name = metric[1]
            method_id = metric[2]

            self.tree.insert("", tk.END, values=(metric_id, metric_name, method_id))

        # with open(hardcoded_file_path, newline='\n') as f:
        #
        #     reader = csv.DictReader(f, delimiter=',')
        #
        #     for index, row in enumerate(reader):
        #
        #         # print("ROWWW -- ",row)
        #         # print('Index: ', index)
        #         # print('-----')
        #
        #         for metric_index, item in enumerate(row):
        #
        #             # print('metric_index: ', metric_index)
        #             # print('modulo index metric: ', metric_index % len(column_names))
        #             # print('modulo index value: ', (metric_index + 10) % len(header_list))
        #
        #             # skip non relevant headers
        #             if metric_index in range(0,10):
        #                 continue
        #
        #             else:
        #                 metric = header_list[metric_index]
        #                 value = row[header_list[metric_index]]
        #
        #                 counter_test += 1
        #
        #                 # print('metric_index: ', metric_index)
        #                 # print('Metric: ', metric)
        #                 # print('Value: ', value)
        #                 # print('-----')
        #
        #
        #                 # measuring_point_id =
        #                 # metric_id =
        #                 # file_id =
        #                 # data_bool =
        #                 # data_str =
        #                 # data_int =
        #                 # data_float =
        #                 #
        #                 # metric_value = (measuring_point_id,
        #                 #                 metric_id,
        #                 #                 file_id,
        #                 #                 data_bool,
        #                 #                 data_str,
        #                 #                 data_int,
        #                 #                 data_float)
        #                 #
        #                 #
        #                 #
        #                 # self.data_object.create_metric_value()
        #
        #
        #
        #
        #                 self.tree.insert("", tk.END, values=(metric, value))




# ref: https://blog.teclado.com/tkinter-scrollable-frames/
class ScrollableFrame(ttk.Frame):

    # todo fix the scroll function
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)

        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)

        scrollbar.pack(side="right", fill="y")
