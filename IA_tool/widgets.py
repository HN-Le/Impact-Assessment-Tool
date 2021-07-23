
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

            # generate button
            button_confirm = tk.Button(frame_method_fragments,
                                        text='Confirm',
                                        width=c.Size.button_width, height=c.Size.button_height,
                                        # command=self.generate_questions)
                                        command= lambda: [self.generate_questions,
                                                          # show_add_metric_frame(),
                                                          self.show_info_screen(),
                                                          self.selection_window.withdraw(),
                                                          self.delete_frame(self.scrollable_metric_frame),
                                                          self.delete_frame(self.test_frame),
                                                          self.delete_frame(self.remove_frame),
                                                          self.add_metric(),
                                                          self.show_summary_metrics()])

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

            self.make_questions()

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

        self.test_frame = ttk.LabelFrame(self.frame_metrics, text="Add metric",
                                         width=600, height=300)

        self.test_frame.pack(fill="both")

        self.remove_frame = ttk.LabelFrame(self.frame_metrics, text="Remove metric",
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
            ttk.Label(self.test_frame,
                      anchor="w", justify='left',
                      font='Helvetica 11',
                      text=value).grid(row=0, column=index + index,
                                       padx=10, pady=(20, 10))

            # input boxes
            if index == 0:
                # textbox metric
                user_metric = tk.StringVar()
                user_metric_input = ttk.Entry(self.test_frame, width=15, textvariable=user_metric)
                user_metric_input.grid(row=0, column=(index + index +1),
                                       padx = 10, pady=(20, 10))
            elif index == 1:
                # combobox: method fragment
                combobox = ttk.Combobox(
                    self.test_frame,
                    values=retrieve_method_fragment_string)
                combobox.grid(row=0, column=(index + index +1),
                                       padx = 10, pady=(20, 10))
            else:
                # combobox: data types
                combobox_2 = ttk.Combobox(
                    self.test_frame,
                    values=retrieve_datatypes)
                combobox_2.grid(row=0, column=(index + index +1),
                                       padx = 10, pady=(20, 10))

        button_add = tk.Button(self.test_frame,
                               text='Add',
                               width=c.Size.button_width, height=c.Size.button_height,
                               command=lambda: [self.add_button(combobox, combobox_2, user_metric, user_survey_question)])

        button_add.grid(row=0, column=6,
                                   padx = 10, pady=(20, 10))

        # refresh screen button
        button_add_refresh = tk.Button(self.test_frame,
                                          text='Refresh screen',
                                          command=self.refresh_summary_window)

        button_add_refresh.grid(row=0, column=7,
                                   padx = 10, pady=(20, 10))

        ttk.Label(self.test_frame,
                  anchor="w", justify='left',
                  font='Helvetica 11',
                  text='Survey question').grid(row=1, column=0,
                                   padx=10, pady=(0, 20))

        # textbox survey question
        user_survey_question = tk.StringVar()
        user_survey_question_input = ttk.Entry(self.test_frame, width=93, textvariable=user_survey_question)
        user_survey_question_input.grid(row=1, column=1, columnspan=10, sticky='w',
                               padx=10, pady=(0, 20))

        # Placeholder for status message
        self.status_message_add_metric = '-- PLACEHOLDER STATUS MESSAGE --'
        ttk.Label(self.test_frame,
                  font='Helvetica 11', foreground='red',
                  text=self.status_message_add_metric).grid(row=2, column=0,
                                                            columnspan=20,
                                                            padx=10, pady=(0, 20),
                                                            sticky='w')


        # remove metric
        ttk.Label(self.remove_frame,
                  anchor="w", justify='left',
                  font='Helvetica 11',
                  text='Enter fragment id: ').grid(row=0, column=0, sticky='w',
                               padx=10, pady=(10, 10))

        # textbox remove method fragment
        user_method_remove = tk.StringVar()
        user_method_remove_input = ttk.Entry(self.remove_frame, width=15, textvariable=user_method_remove)
        user_method_remove_input.grid(row=0, column=1, sticky='w',
                               padx=10, pady=(20, 10))

        ttk.Label(self.remove_frame,
                  anchor="w", justify='left',
                  font='Helvetica 11',
                  text='Enter method id: ').grid(row=0, column=2, sticky='w',
                               padx=10, pady=(20, 10))

        # textbox remove metric
        user_metric_remove = tk.StringVar()
        user_metric_remove_input = ttk.Entry(self.remove_frame, width=15, textvariable=user_metric_remove)
        user_metric_remove_input.grid(row=0, column=3, sticky='w',
                               padx=10, pady=(20, 10))

        # remove button
        button_remove = tk.Button(self.remove_frame,
                                  text='Remove',
                                  width=c.Size.button_width, height=c.Size.button_height,
                                  command=lambda: [self.remove_button(user_method_remove, user_metric_remove)])

        button_remove.grid(row=0, column=4, sticky='w',
                               padx=10, pady=(20, 10))

        # refresh screen button
        button_remove_refresh = tk.Button(self.remove_frame,
                                  text='Refresh screen',
                                  command=self.refresh_summary_window)

        button_remove_refresh.grid(row=0, column=5, sticky='w',
                               padx=10, pady=(20, 10))

        # Placeholder for status message
        self.status_message_remove_metric = '-- PLACEHOLDER STATUS MESSAGE --'
        ttk.Label(self.remove_frame,
                  font='Helvetica 11', foreground='red',
                  text=self.status_message_remove_metric).grid(row=1, column=0, columnspan=20,
                                                            padx=10, pady=(0, 20),
                                                               sticky='w')


    def add_button(self, combobox, combobox_2, text, user_survey_question):

        # todo link user added metric to metrics list
        # todo add validation for input boxes
        # todo show text for confirmation that metric is added

        combobox.current()
        combobox_2.current()

        combobox.get()
        combobox_2.get()

        print('METRIC TEXT BOX: ', text.get())
        print('METHOD FRAG BOX: ', combobox.get())
        print('DATATYPE BOX: ', combobox_2.get())
        print('SURVEY QUESTION BOX: ', user_survey_question.get())

        combobox.delete(0, 'end')
        combobox_2.delete(0, 'end')
        text.set('')
        user_survey_question.set('')

    def remove_button(self, frag_id, metric_id):

        # todo link user added metric to metrics list
        # todo add validation for input boxes
        # todo show text for confirmation that metric is added

        print('FRAGMENT ID TEXT BOX: ', frag_id.get())
        print('METRIC ID TEXT BOX: ', metric_id.get())

        frag_id.set('')
        metric_id.set('')

    def get_target(self, event=None):
        self.input_combobox = event.widget.get()

        target_key = self.chose_target_list[self.input_combobox]

        if self.community_list is not None:
            self.community_list.delete('0', tk.END)

        # print('get_target -- target_key ', target_key)

        self.create_list(target_key)



    def create_list(self, target_key):

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

        for line in self.checkbox_list:
            values = self.dataframe.show_relevant_fragments(self.dataframe.dataframe, line, target_key)
            metrics = values[1].values
            types = values[2].values



            for index, item in enumerate(values[0]):
                self.community_list.insert(tk.END, ' ' + 'Survey question:   ' + item)
                self.community_list.insert(tk.END, '                ' + 'Metric:   ' + metrics[index])
                self.community_list.insert(tk.END, '                   ' + 'Type:   ' + types[index])
                self.community_list.insert(tk.END, '\n')

        # print('create_list, community list:  ---', self.community_list)

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



        # make add_metric section
        # self.add_metric(self.frame_add_metric)

    def make_summary_tabs(self):
        self.notebook_summary = ttk.Notebook(self.info_window)

        self.frame_metrics = ttk.Frame(self.info_window, width=1200, height=800)
        # self.frame_metrics .grid_propagate(0)
        self.frame_metrics.grid(row=0, column=0,
                                padx=(10, 0),
                                sticky='nsew')

        self.summary_metrics = ttk.LabelFrame(self.frame_metrics, text="Summary of all metrics",
                                              width=600, height=400)

        self.summary_metrics.pack(fill="both", expand=True)

        self.test_frame = ttk.LabelFrame(self.frame_metrics, text="Add metric",
                                         width=600, height=200)

        self.test_frame.pack(fill="both")

        self.remove_frame = ttk.LabelFrame(self.frame_metrics, text="Remove metric",
                                           width=600, height=200)

        self.remove_frame.pack(fill="both")

        # frame summary_metrics scrollable
        self.scrollable_metric_frame = ScrollableFrame(self.summary_metrics)

        self.frame_questions = ttk.Frame(self.info_window, width=1200, height=800)
        self.frame_questions.grid_propagate(0)
        self.frame_questions.grid(padx=(10, 0),
                                    sticky='nsew')

        self.notebook_summary.add(self.frame_metrics, text='Metrics')
        self.notebook_summary.add(self.frame_questions, text='Survey Questions')

        self.notebook_summary.grid(row=0, column=0, sticky='E', padx=5, pady=5, ipadx=5, ipady=5)

    def make_questions(self):

        self.frame_survey_questions = ttk.LabelFrame(self.frame_questions, text="Survey questions",
                                                     width=1200, height=600)

        self.frame_survey_questions.grid_propagate(0)
        self.frame_survey_questions.grid(padx=5, pady=5,
                                         sticky='e')

        self.create_list('project_provider')

        combobox_target = ttk.Combobox(
            self.frame_survey_questions,
            values=["Project Provider",
                    "Community School Leader",
                    "Teacher",
                    "Student"
                    ])

        combobox_target.current(0)
        # -----------------------

        combobox_target.grid(row=5, column=0, padx=(20, 0), pady=2,
                             sticky='w')

        combobox_target.bind("<<ComboboxSelected>>", self.get_target)

    def show_summary_metrics(self):


        # frame summary_metrics scrollable
        self.scrollable_metric_frame = ScrollableFrame(self.summary_metrics)

        for index, value in enumerate(self.checkbox_list):
            # print("show_summary_metrics: VALUE: ", value)
            # print("show_summary_metrics: type of VALUE: ", type(value[0]))

            sql_retrieve_method_frag_id = "select method_fragment_id from method_fragment where method_fragment_name=?"
            retrieve_method_frag_id = self.data_object.query_with_par(sql_retrieve_method_frag_id, ((value),))


            sql_retrieve_metrics = "select metric_name from metric where method_fragment_id=?"
            retrieve_metrics = self.data_object.query_with_par(sql_retrieve_metrics, retrieve_method_frag_id[0])


            ttk.Label(self.scrollable_metric_frame.scrollable_frame,
                      anchor="w", justify='left',
                      font='Helvetica 10 bold',
                      text=str(index+1) + ":  " + value).pack(fill='both')

            for metric_index, metric in enumerate(retrieve_metrics):
                ttk.Label(self.scrollable_metric_frame.scrollable_frame,
                          anchor="w", justify='left',
                          text= '    ' + str(metric_index+1) + '  - ' + metric[0]).pack(fill='both')
                # print("METRIC TYPE: ", type(metric))


        self.scrollable_metric_frame.pack(side="left", fill="both", expand=True)

    def get_data_object(self, data):
        self.data_object = data

        # print("--- get_data_object - Check")

    def delete_frame(self, frame):

        if frame is not None:
            frame.pack_forget()
            frame.destroy()

    def refresh_summary_window(self):

        self.generate_questions()
        self.show_info_screen()
        self.selection_window.withdraw()
        self.delete_frame(self.scrollable_metric_frame)
        self.delete_frame(self.test_frame)
        self.delete_frame(self.remove_frame)
        self.add_metric()
        self.show_summary_metrics()
        self.notebook_summary.select(0)

        # print("REFRESH SUMMARY WINDOW ------ ")


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











