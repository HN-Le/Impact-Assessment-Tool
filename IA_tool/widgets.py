
import tkinter as tk
from tkinter import ttk
from . import constants as c
from tkinter import filedialog
from . import models as m
import webbrowser

import numpy as np
import pandas as pd
import os
from varname import nameof
from . import views as v
import sys
from tkinter import font


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
        print('Selected:', filename)
        self.file_path = filename

    def get_file_name(self):

        shown_text = "Filename: " + self.file_path.split("/")[-1]
        return shown_text

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

        self.is_checked = False

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
                self.is_checked = True

            # generate button
            button_confirm = tk.Button(frame_method_fragments,
                                        text='Confirm',
                                        width=c.Size.button_width, height=c.Size.button_height,
                                        command= lambda: [select_check()])

            button_confirm.grid(row=18, column=0,
                                 padx=(10, 0),
                                 pady=2,
                                 sticky='w')

        else:
            self.selection_window.deiconify()


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

        # checkbox_1 = tk.BooleanVar()
        # tk.Checkbutton(frame_project_goals, text="male", variable=checkbox_1).grid(row=0, sticky='w')

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
                    values=retrieve_method_fragment_string)
                combobox.grid(row=0, column=(index + index +1),
                                       padx = 10, pady=(20, 10))
            else:
                # combobox: data types
                combobox_2 = ttk.Combobox(
                    self.add_metrics_frame,
                    values=retrieve_datatypes)
                combobox_2.grid(row=0, column=(index + index +1),
                                       padx = 10, pady=(20, 10))

        button_add = tk.Button(self.add_metrics_frame,
                               text='Add',
                               width=c.Size.button_width, height=c.Size.button_height,
                               command=lambda: [self.add_button(combobox, combobox_2, user_metric, user_survey_question, combobox_target),
                                                self.refresh_summary_window()])

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
            values=["Project Provider",
                    "Community School Leader",
                    "Teacher",
                    "Student"
                    ])
        combobox_target.grid(row=1, column=5,
                        padx=10, pady=(0, 20))



        # Placeholder for status message
        self.status_message_add_metric = '-- PLACEHOLDER STATUS MESSAGE --'
        ttk.Label(self.add_metrics_frame,
                  font='Helvetica 11', foreground='red',
                  text=self.status_message_add_metric).grid(row=2, column=0,
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
                                  command=lambda: [self.remove_button(user_method_remove),
                                                   self.refresh_summary_window()])

        button_remove.grid(row=0, column=4, sticky='w',
                               padx=10, pady=(20, 10))

        # Placeholder for status message
        self.status_message_remove_metric = '-- PLACEHOLDER STATUS MESSAGE --'
        ttk.Label(self.remove_frame,
                  font='Helvetica 11', foreground='red',
                  text=self.status_message_remove_metric).grid(row=1, column=0, columnspan=20,
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


        print('METRIC TEXT BOX: ', metric_input.get())
        print('METHOD FRAG BOX: ', method_frag_input.get())
        print('DATATYPE BOX: ', data_type_input.get())
        print('SURVEY QUESTION BOX: ', user_survey_question.get())

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
        method_frag_input.delete(0, 'end')
        data_type_input.delete(0, 'end')
        combobox_target.delete(0, 'end')
        metric_input.set('')
        user_survey_question.set('')




    def remove_button(self, frag_id):

        # todo link user added metric to metrics list
        # todo add validation for input boxes
        # todo show text for confirmation that metric is added

        # # empty lists
        # self.metric_list.clear()
        # self.method_frag_list.clear()

        frag_id_int_user = int((frag_id.get()),)
        frag_id_in_db = self.metric_id_list[frag_id_int_user-1]

        # print('frag_id_int_user ----------- ', frag_id_int_user)
        # print('self.metric_id_list[frag_id_int_user] ----------- ', self.metric_id_list[frag_id_int_user - 1])

        sql_check = "select user_made from metric where metric_id = ?"
        retrieve_check = self.data_object.query_with_par(sql_check, ((frag_id_in_db),))

        sql_retrieve_method_frag_id = "delete from metric where metric_id = (?)"

        # print('retrieve_check ------ ', retrieve_check[0][0])

        if retrieve_check[0][0] == False:
            print('Standard metric, do not remove ----------')
        else:
            self.data_object.delete_row_with_par(sql_retrieve_method_frag_id, frag_id_in_db)
            print('User metric, removed! ----------')

        # print('self.metric_id_list ----------- ', self.metric_id_list)

        # reset
        frag_id.set('')

    def get_target(self, event=None):
        self.input_combobox = event.widget.get()

        target_key = self.chose_target_list[self.input_combobox]

        if self.community_list is not None:
            self.community_list.delete('0', tk.END)
            print('self.community_list is not None: ----------')

        # print('get_target -- target_key ', target_key)

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

        # Listbox with all the survey questions per target group
        for index, value in enumerate(self.checkbox_list):

            # todo add demographic of interest and scope
            # retrieve method fragment id from checked methods fragments
            sql_retrieve_method_frag_id = "select method_fragment_id from method_fragment where method_fragment_name=?"
            retrieve_method_frag_id = self.data_object.query_with_par(sql_retrieve_method_frag_id, ((value),))

            # retrieve metrics from the method fragments
            sql_retrieve_metrics = "select * from metric where method_fragment_id=(?) and target_name=(?)"
            retrieve_metrics = self.data_object.query_with_par(sql_retrieve_metrics, (retrieve_method_frag_id[0][0], target_key))

            for metric_index, metric in enumerate(retrieve_metrics):

                self.community_list.insert(tk.END, ' ' + 'Survey question:   ' + str(metric[4]))
                self.community_list.insert(tk.END, '                ' + 'Metric:   ' + str(metric[1]))
                self.community_list.insert(tk.END, '                   ' + 'Type:   ' + str(metric[5]))
                self.community_list.insert(tk.END, '\n')

        button_download_all = tk.Button(self.frame_survey_questions,
                               text='Download all questions',
                               height=c.Size.button_height,
                               command='')

        button_download_all.grid(row=9, column=0,
                        padx=(10, 0),
                        sticky='w')

        button_go_to_add_metrics = tk.Button(self.frame_survey_questions,
                                        text='Add additional metrics',
                                        height=c.Size.button_height,
                                        command=lambda: [self.notebook_summary.select(0)])

        button_go_to_add_metrics.grid(row=10, column=0,
                                 padx=(10, 0),
                                 sticky='w')

    def make_summary_tabs(self):

        # make notebook
        self.notebook_summary = ttk.Notebook(self.info_window)

        # make tabs
        self.tab_metrics = ttk.Frame(self.info_window, width=1200, height=800)
        self.tab_metrics.grid(row=0, column=0,
                              padx=(10, 0),
                              sticky='nsew')

        self.tab_questions = ttk.Frame(self.info_window, width=1200, height=800)
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
                values=["Project Provider",
                        "Community School Leader",
                        "Teacher",
                        "Student"
                        ])

            self.combobox_target_survey.current(0)

            self.combobox_target_survey.grid(row=5, column=0, padx=(20, 0), pady=2,
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

    def adjust_metric_definition(self):
        # todo option to change metric descripton
        print('')

    def show_add_metric_definition_window(self):

        # make pop up window
        self.add_metric_window = tk.Toplevel()
        self.add_metric_window.wm_title('Add metric definitions')

        # set dimensions window
        width = 1200
        height = 800
        self.add_metric_window.geometry("{}x{}".format(width, height))

        # make labelframe
        # frame_add_metric = ttk.LabelFrame(self.add_metric_window, text="Add metric definitions",
        #                                         width=1200, height=800)
        # frame_add_metric.pack(fill='both')

        # make frame scrollable
        self.scrollable_add_metric_frame = ScrollableFrame(self.add_metric_window)

        metric_frame = ttk.Frame(self.add_metric_window, width=1200, height=800)

        frame_list = []

        for index, value in enumerate(self.checkbox_list):
            # print("show_summary_metrics: VALUE: ", value)
            # print("show_summary_metrics: type of VALUE: ", type(value[0]))


            # retrieve method fragment id from checked methods fragments
            sql_retrieve_method_frag_id = "select method_fragment_id from method_fragment where method_fragment_name=?"
            retrieve_method_frag_id = self.data_object.query_with_par(sql_retrieve_method_frag_id, ((value),))

            # retrieve metrics from the method fragments
            sql_retrieve_metrics = "select * from metric where method_fragment_id=?"
            retrieve_metrics = self.data_object.query_with_par(sql_retrieve_metrics, retrieve_method_frag_id[0])

            ttk.Label(self.scrollable_add_metric_frame.scrollable_frame,
                      anchor="w", justify='left',
                      font='Helvetica 12 bold',
                      text=value).pack(fill='both')

            for metric_index, metric in enumerate(retrieve_metrics):

                ttk.Label(self.scrollable_add_metric_frame.scrollable_frame,
                          anchor="w", justify='left',
                          text='    ' + 'Metric: ' +str(metric[1])).pack(fill='both')

                ttk.Label(self.scrollable_add_metric_frame.scrollable_frame,
                          anchor="w", justify='left',
                          text='    ' + 'Target group: ').pack(fill='both')

                ttk.Label(self.scrollable_add_metric_frame.scrollable_frame,
                          anchor="w", justify='left',
                          text='    ' + 'Set metric target: ').pack(fill='both')

                ttk.Label(self.scrollable_add_metric_frame.scrollable_frame,
                          anchor="w", justify='left',
                          text='    ' + 'Demographic of interest: ').pack(fill='both')

                ttk.Label(self.scrollable_add_metric_frame.scrollable_frame,
                          anchor="w", justify='left',
                          text='    ' + 'Demographic scope: ').pack(fill='both')

                ttk.Label(self.scrollable_add_metric_frame.scrollable_frame,
                          anchor="w", justify='left',
                          text='    ' + 'Metric definition: ').pack(fill='both')

                user_metric = tk.StringVar()
                ttk.Entry(self.scrollable_add_metric_frame.scrollable_frame,
                          width=15, textvariable=user_metric).pack(fill='both', padx=20)

                ttk.Label(self.scrollable_add_metric_frame.scrollable_frame,
                          text='').pack()



        # put scrollable frame in window
        self.scrollable_add_metric_frame.pack(fill="both", expand='true')







        # to add as frame : self.scrollable_add_metric_frame.scrollable_frame


        # load in metric data


    def add_metric_definition(self):
        print('add_metric_definition ----')

    def add_metric_target(self):
        print('add_metric_target ----')
        print('demographic of interest BOOL ----')
        print('demographic of interest scope text ----')


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











