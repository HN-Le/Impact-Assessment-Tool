
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkFont
from . import constants as c
from tkinter import filedialog
from . import models as m
from . import views as v
import webbrowser
from functools import partial
import csv
import statistics
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)
import pyperclip

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
        return filename

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

class Window(tk.Frame):

    def focus_window(self, window):
        window.lift()
        window.focus_force()
        window.grab_set()
        window.grab_release()

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

            width = 720
            height = 400
            position_left = 150
            position_right = 150

            self.selection_window.geometry("{}x{}+{}+{}".format(width, height, position_left, position_right))

            # set size window fixed
            self.selection_window.resizable(0, 0)

            # self.selection_window.geometry('%sx%s' % (int(width-100), int(height)))

            self.selection_window.protocol("WM_DELETE_WINDOW", lambda arg='method_fragment': self.hide_window(arg))

            frame_method_fragments= ttk.LabelFrame( self.selection_window, text="1.3 - Select method fragments",
                                                 width=700, height=380)

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

            # focus on window
            window_obj = Window()
            window_obj.focus_window(self.selection_window)

        else:
            self.selection_window.deiconify()

    def send_status_message(self, message_1, message_2):
        self.reset_message_1 = message_1
        self.reset_message_2 = message_2

    def reset_status_message(self):
        self.reset_message_1['text'] = ''
        self.reset_message_2['text'] = ''

    def show_info_screen(self):

        if not self.info_window:
            self.info_window = tk.Toplevel()
            self.info_window.wm_title('Summary')

            width = 1280
            height = 700
            position_left = 150
            position_right = 150

            self.info_window.geometry("{}x{}+{}+{}".format(width, height, position_left, position_right))

            # set size window fixed
            self.info_window.resizable(0, 0)

            # self.info_window.geometry('%sx%s' % (int(width-100), int(height)))

            self.info_window.protocol("WM_DELETE_WINDOW", lambda arg='summary': self.hide_window(arg))

            self.make_summary_tabs()

            self.make_questions(refresh=False)

            # go to metric tab
            self.notebook_summary.select(0)

            # focus on window
            window_obj = Window()
            window_obj.focus_window(self.info_window)


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


        labels = ['Metric', 'Method fragment', 'Question type']

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
                      text=value).grid(row=0, column=index + index, sticky='e',
                                       padx=10, pady=(20, 10))

            # input boxes
            if index == 0:
                # textbox metric
                user_metric = tk.StringVar()
                user_metric_input = ttk.Entry(self.add_metrics_frame, width=50, textvariable=user_metric)
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
                combobox_2.grid(row=0, column=(index + index + 1),
                                padx=10, pady=(20, 10))



        button_add = tk.Button(self.add_metrics_frame,
                               text='Add',
                               width=c.Size.button_width, height=c.Size.button_height,
                               command=lambda: [self.add_button(combobox,
                                                                combobox_2,
                                                                user_metric,
                                                                user_survey_question,
                                                                combobox_target,
                                                                combobox_3,
                                                                user_answer_options
                                                                )])

        button_add.grid(row=2, column=2)

        ttk.Label(self.add_metrics_frame,
                  anchor="w", justify='left',
                  font='Helvetica 11',
                  text='Survey question').grid(row=1, column=0, sticky='e',
                                   padx=10, pady=(0, 10))

        # textbox survey question
        user_survey_question = tk.StringVar()
        user_survey_question_input = ttk.Entry(self.add_metrics_frame, width=50, textvariable=user_survey_question)
        user_survey_question_input.grid(row=1, column=1, columnspan=5, sticky='w',
                               padx=(10,0), pady=(0, 10))

        # label for target to ask to
        ttk.Label(self.add_metrics_frame,
                  font='Helvetica 11',
                  text='Ask to: ').grid(row=1, column=2,
                                        columnspan=20,
                                        padx=(10,0), pady=(0, 10),
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
        combobox_target.grid(row=1, column=3,
                        padx=10, pady=(0, 20))

        ttk.Label(self.add_metrics_frame,
                  font='Helvetica 11',
                  text='Data type: ').grid(row=1, column=4,
                                        columnspan=20,
                                        padx=(10, 0), pady=(0, 10),
                                        sticky='w')

        data_type_list = ["Whole number", "Decimal", "Boolean", "String"]

        combobox_3 = ttk.Combobox(
            self.add_metrics_frame,
            state="readonly",
            values=data_type_list)
        combobox_3.grid(row=1, column=5,
                        padx=10, pady=(0, 20))

        ttk.Label(self.add_metrics_frame,
                  anchor="w", justify='left',
                  font='Helvetica 11',
                  text='          Answer options \nseperate options with ;').grid(row=2, column=0, sticky='e',
                                               padx=10)

        user_answer_options = tk.StringVar()
        user_answer_options_input = ttk.Entry(self.add_metrics_frame, width=50, textvariable=user_answer_options)
        user_answer_options_input.grid(row=2, column=1,
                               padx=(0))

        # Placeholder for status message
        self.status_message_add_metric = tk.StringVar()
        self.status_message_add_metric.set("")

        self.status_message_label = ttk.Label(self.add_metrics_frame,
                  font='Helvetica 11', foreground='red',
                  textvariable=self.status_message_add_metric)

        self.status_message_label.grid(row=3, column=0,
                                                            columnspan=20,
                                                            padx=10, pady=10,
                                                            sticky='w')

        # remove metric

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

    def add_button(self, method_frag_input, question_type_input, metric_input,
                   user_survey_question, combobox_target, combobox_data_type, answer_options_box):

        # todo link user added metric to metrics list
        # todo add validation for input boxes
        # todo show text for confirmation that metric is added

        method_frag_input.current()
        question_type_input.current()
        combobox_target.current()
        combobox_data_type.current()

        method_frag_input.get()
        question_type_input.get()
        combobox_target.get()
        combobox_data_type.get()

        def remap_data_type(data_type):
            if data_type == "Whole number":
                return "int"
            elif data_type == "Decimal":
                return "float"
            elif data_type == "Boolean":
                return "bool"
            else:
                return "string"

        # print('METRIC TEXT BOX: ', metric_input.get())
        # print('METHOD FRAG BOX: ', method_frag_input.get())
        # print('DATATYPE BOX: ', data_type_input.get())
        # print('SURVEY QUESTION BOX: ', user_survey_question.get())

        if metric_input.get() and method_frag_input.get() and \
                question_type_input.get() and user_survey_question.get() and \
                combobox_target.get() and combobox_data_type.get():

            if question_type_input.get() == "Multiple_choice" or question_type_input.get() == "Scale":
                if not answer_options_box.get():
                    self.status_message_add_metric.set("Please fill in the answer options!")

            else:
                sql_retrieve_method_frag_id = "select method_fragment_id from method_fragment where method_fragment_name=?"
                retrieve_method_frag_id = self.data_object.query_with_par(sql_retrieve_method_frag_id, ((method_frag_input.get()),))

                metric_name = metric_input.get()
                method_fragment_id = retrieve_method_frag_id[0][0]
                metric_definition = None
                metric_question = user_survey_question.get()
                metric_value_type = question_type_input.get()
                multiple_answers = None
                answer_options = None
                target_name = self.chose_target_list[combobox_target.get()]
                user_made = True
                data_type = remap_data_type(combobox_data_type.get())

                if question_type_input.get() == "Multiple_choice" or question_type_input.get() == "Scale":
                    answer_options == (answer_options_box.get()).strip()

                metric = ((metric_name).strip(), method_fragment_id,
                          metric_definition, (metric_question.strip()),
                          metric_value_type, multiple_answers,
                          answer_options, target_name, user_made, data_type)

                # print('Metric_name ---------', metric)

                self.data_object.create_metric(metric)

                # reset input boxes
                method_frag_input.set('')
                question_type_input.set('')
                combobox_target.set('')

                metric_input.set('')
                user_survey_question.set('')
                combobox_data_type.set('')
                answer_options_box.set('')

                self.status_message_label.config(foreground='green')
                self.status_message_add_metric.set("Metric " + metric_name + ' added!')

                # update frame to show status message
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
                    self.status_message_remove_metric.set("Cannot remove standard metrics! (only metrics added by user)")

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

                    # reset
                    frag_id.set('')

                    self.remove_label.config(foreground='green')
                    self.status_message_remove_metric.set("Metric removed!")
                    self.remove_frame.update()
                    self.remove_frame.after(1000, self.refresh_summary_window())

                # print('self.metric_id_list ----------- ', self.metric_id_list)

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

    # Copy paste a cleaned line from the listbox
    def copy_from_listbox(self, listbox, event):

        # self.info_window.clipboard_clear()

        selection = listbox.curselection()
        text_selection = listbox.get(selection)

        cleaned_selection = [x.strip() for x in text_selection.split(':')]
        value = cleaned_selection[1]

        pyperclip.copy(value)
        pyperclip.paste()

        print("Value: ", pyperclip.paste())

        # self.info_window.clipboard_append('CLIPBOARD')
        #
        # print("Clipboard: ", self.info_window.clipboard_get())
        # self.info_window.update()
        #

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
                                         activestyle='none',
                                         width=140, height=15)

        # bind copy past function to listbox
        self.community_list.bind("<Control-Key-q>", lambda x: self.copy_from_listbox(self.community_list, x))

        scrollbar_v_community_list.grid(row=7, column=1, sticky='ns')
        scrollbar_h_community_list.grid(row=8, column=0, sticky='we')

        self.community_list.grid(row=7, column=0,
                                 padx=(10, 0),
                                 pady=2,
                                 sticky='nswe')

        scrollbar_v_community_list.config(command=self.community_list.yview)
        scrollbar_h_community_list.config(command=self.community_list.xview)

        metric_counter = 0
        self.metric_counter_label = tk.StringVar()
        self.metric_counter_label.set('')

        # ---------------- txt
        # 10 , 30
        txt_metric = 'Metric:'
        txt_question = 'Survey question:'
        txt_type = 'Question type (for mWater):'
        txt_items = 'Question items (for mWater):'
        txt_choices = 'Question choices (for mWater):'
        txt_format = 'Answer format (for mWater):'

        pre_pad = ' ' * 5
        txt_list = [txt_metric, txt_question, txt_type, txt_items, txt_choices, txt_format]

        # Get the listbox font
        listFont = tkFont.Font(font=self.community_list.cget("font"))
        spaceLength = listFont.measure(" ")
        spacing = 15 * spaceLength

        len_txt = [listFont.measure(s) for s in txt_list]
        longestLength = max(len_txt)

        spacesToAdd_list = []
        for item in len_txt:
            neededSpacing = longestLength + spacing - item
            spacesToAdd = int(round(neededSpacing / spaceLength))
            spacesToAdd_list.append(spacesToAdd)

        # Listbox with all the survey questions per target group
        for index, value in enumerate(self.checkbox_list):

            # todo add demographic of interest and scope
            # retrieve method fragment id from checked methods fragments
            sql_retrieve_method_frag_id = "select method_fragment_id from method_fragment where method_fragment_name=?"
            retrieve_method_frag_id = self.data_object.query_with_par(sql_retrieve_method_frag_id, ((value),))

            # retrieve metrics from the method fragments
            sql_retrieve_metrics = "select * from metric where method_fragment_id=(?) and target_name=(?)"
            retrieve_metrics = self.data_object.query_with_par(sql_retrieve_metrics, (retrieve_method_frag_id[0][0], target_key))

            metric_counter = metric_counter + len(retrieve_metrics)

            # TODO sort based on question type (likert/num/bool)



            for metric_index, metric in enumerate(retrieve_metrics):

                metric_name = metric[1]
                question = metric[4]
                multiple_answers = metric[6]
                question_type = metric[5].lower()
                data_type = metric[10]
                items_list = []

                if multiple_answers:
                    type = c.DataTypes.mWater_types['multiple_choice_multi']
                else:
                    type = c.DataTypes.mWater_types[question_type]

                choices_all = metric[7]
                if choices_all:
                    choices = [x.strip() for x in choices_all.split(';')]
                    items = len(choices)
                    items_list = []
                    for item in range(items):
                        items_list.append(item)


                if data_type == 'float' or data_type == 'int':
                    format = c.DataTypes.mWater_formats[data_type]

                elif question_type == 'string':
                    format = c.DataTypes.mWater_formats[data_type]

                # if metric_index == 0:
                #     self.community_list.insert(tk.END, '\n')

                self.community_list.insert(tk.END, pre_pad + txt_metric + spacesToAdd_list[0] * " " + str(metric_name))
                self.community_list.insert(tk.END, pre_pad + txt_question + spacesToAdd_list[1] * " " + str(question))
                self.community_list.insert(tk.END, pre_pad + txt_type + spacesToAdd_list[2] * " " + str(type))

                if question_type == 'scale':
                    self.community_list.insert(tk.END, pre_pad + txt_items + spacesToAdd_list[3] * " " + str(';   '.join(map(str,items_list))))

                if choices_all:
                    self.community_list.insert(tk.END, pre_pad + txt_choices + spacesToAdd_list[4] * " " + str(';   '.join(map(str,choices))))

                # also if text question
                if question_type == 'numerical':
                    self.community_list.insert(tk.END, pre_pad + txt_format + spacesToAdd_list[5] * " " + str(format))

                self.community_list.insert(tk.END, '\n')


        self.metric_counter_label.set("Amount of questions:  " + str(metric_counter))

        tk.Label(self.frame_survey_questions,
                 textvariable= self.metric_counter_label,
                 font='Helvetica 11').grid(row=11, column=0,
                                               padx=(20, 0),
                                               pady=(0,10),
                                               sticky='w')

        button_go_to_add_metrics = tk.Button(self.frame_survey_questions,
                                        text='Add additional metrics',
                                        height=c.Size.button_height,
                                        command=lambda: [self.notebook_summary.select(0)])

        button_go_to_add_metrics.grid(row=12, column=0,
                                      padx=(20, 0),
                                      pady=(5,10),
                                      sticky='w')

    def make_summary_tabs(self):

        # make notebook
        self.notebook_summary = ttk.Notebook(self.info_window)

        # make tabs
        self.tab_metrics = ttk.Frame(self.info_window, width=1200, height=720)
        self.tab_metrics.grid(row=0, column=0,
                              padx=(10, 0),
                              sticky='nsew')

        self.tab_questions = ttk.Frame(self.info_window, width=1200, height=720)
        self.tab_questions.grid(padx=(10, 0),
                                sticky='nsew')

        # self.tab_metric_definition = ttk.Frame(self.info_window, width=1200, height=800)
        # self.tab_metric_definition.grid_propagate(0)
        # self.tab_metric_definition.grid(padx=(10, 0),
        #                         sticky='nsew')

        # make label frames
        self.summary_metrics = ttk.LabelFrame(self.tab_metrics,
                                              text="Summary of all metrics",
                                              width=600, height=300)
        self.summary_metrics.pack(side='top', fill="both")

        self.add_metrics_frame = ttk.LabelFrame(self.tab_metrics,
                                                text="Add metric",
                                                width=600, height=300)
        self.add_metrics_frame.pack(side='top', fill="both")

        self.remove_frame = ttk.LabelFrame(self.tab_metrics, text="Remove metric",
                                           width=600, height=200)
        self.remove_frame.pack(side='top', fill="both")

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
                                                         width=1200, height=720)

            # self.frame_survey_questions.grid_propagate(0)
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

            self.combobox_target_survey.grid(row=5, column=0, padx=(20, 0),
                                             sticky='w')

            self.combobox_target_survey.bind("<<ComboboxSelected>>", self.get_target)

            tk.Label(self.frame_survey_questions,
                     text='To copy the value:     ctrl + q\nTo paste the value:    ctrl + v',
                     foreground="#234987").grid(row=6, column=0,
                                                padx=10,
                                                pady=5,
                                                sticky='w')

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

        width = 900
        height = 720
        position_left = 150
        position_right = 150

        self.add_metric_window.geometry("{}x{}+{}+{}".format(width, height, position_left, position_right))

        # set size window fixed
        self.add_metric_window.resizable(0, 0)

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
            metric_frame = ttk.Frame(self.scrollable_add_metric_frame.scrollable_frame, width=width, height=height)

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
                          text='    ' + 'Set metric target: (must be >0 !)').pack(fill='both', pady=(0, 5))

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
                self.metric_target_list.append(user_target_input)
                self.if_increase_list.append(combobox)
                self.status_message_list.append(status_message)

                if user_metric_definition_input:
                    self.user_metric_defintion_text.append(str(user_metric_definition_input).strip())
                    self.demo_scope_list.append(str(user_demo_scope_input).strip())
                else:
                    self.user_metric_defintion_text.append(user_metric_definition_input)
                    self.demo_scope_list.append(user_demo_scope_input)


                counter += 1

                # white line
                ttk.Label(metric_frame, text='').pack()

            metric_frame.pack(fill='both')

        # print('button_id_list ---------- ', len(self.button_id_list))
        # print('METRIC ITEM LIST', self.metric_id_list)

        # put scrollable frame in window
        self.scrollable_add_metric_frame.pack(fill="both", expand='true')

        # focus on window
        window_obj = Window()
        window_obj.focus_window(self.add_metric_window)

    def reset_user_def(self, index):

        self.user_metric_defintion_text[index].set('')
        reset_def = None

        sql_update_definition = "update metric set metric_definition = (?) where metric_id = (?)"
        self.data_object.update_row_with_par(sql_update_definition, (reset_def,
                                                                     self.metric_id_list[index]))

    def save_metric_stats(self, index):

        # todo remove project id hardcode

        self.if_increase_list[index].current()
        self.isIncrease = None

        # update metric target if there is input
        if self.metric_target_list[index].get() != '' and self.if_increase_list[index].get() != '':

            try:

                metric_target_int = int(self.metric_target_list[index].get())

                if self.if_increase_list[index].get() == "Increase":
                    self.isIncrease = True
                else:
                    self.isIncrease = False

                self.data_object.send_parameter((self.metric_target_list[index].get(),
                                                 self.isIncrease,
                                                 self.checkbox_demographic[index].get(),
                                                 self.demo_scope_list[index].get(),
                                                 self.metric_id_list[index]))

                if metric_target_int < 0:
                    self.status_message_list[index].set('Error, please only fill in numbers >0 for metric target!')

            except ValueError:
                # self.status_message_remove_metric.set("Please only fill in numbers!")
                self.status_message_list[index].set('Error, please only fill in numbers for metric target!')
                return

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

            # TODO un hardcode project_id !
            target = (self.isIncrease, metric_target, interest_demographic, interest_scope, 1, metric_id)
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

        # list to hold data
        self.data_list = []
        self.unique_metrics = []
        self.selected_file_counter = 0

    # get data
    def get_data_object(self, data):
        self.data_object = data

    def get_paths_dict(self, dict):
        self.paths_dict = dict

    def load_in_paths(self, dict):
        self.paths = dict

    def load_into_database(self, dict, frame):

        # delete all rows in metric_values table
        self.data_object.empty_table()

        # txt variable to display statusmessage
        self.status_load_data = tk.StringVar()
        self.status_load_data.set("")

        self.selected_file_counter = 0

        # variables for the SQL query
        self.measuring_point_id = None
        self.metric_id = None
        self.data_bool = None
        self.data_str = None
        self.data_int = None
        self.data_float = None
        self.target = None

        # function to check in the dict what the target is for each item
        def target_check(item):
            if item.endswith('provider'):
                return 'project_provider'
            elif item.endswith('leader'):
                return 'community_school_leader'
            elif item.endswith('teacher'):
                return 'teacher'
            else:
                return 'student'

        # function to check datatype and clean accordingly
        def data_type_check(value):

            if isinstance(value, int) or isinstance(value, float):
                return value
            elif isinstance(value, str):
                cleaned_value = (value.lower()).strip()
                return cleaned_value

        # reset all data values to None except the file in csv
        def reset_data(type):
            if type == 'data_int':
                self.data_bool = None
                self.data_str = None
                self.data_float = None

            elif type == 'data_bool':
                self.data_str = None
                self.data_float = None
                self.data_int = None

            elif type == 'data_float':
                self.data_str = None
                self.data_bool = None
                self.data_int = None

            else:
                self.data_float = None
                self.data_bool = None
                self.data_int = None

        # loop through dict and extract the data from the valid paths
        for id, item in enumerate(dict):

            # print('Key: ', item)
            # print('Value: ', dict[item])

            # variables for the SQL query
            self.file_id = id

            # non valid paths
            if dict[item] == '':
                continue
                # print(item, ': No path selected')

            else:
                # check which target group the file is for
                self.target = target_check(item)

                # extract the measuring point
                if item.startswith('sop'):
                    self.measuring_point_id = 1

                elif item.startswith('hop'):
                    self.measuring_point_id = 2

                elif item.startswith('eop'):
                    self.measuring_point_id = 3

                else:
                    self.measuring_point_id = 4

                # print('file ID = ', self.file_id)
                # print('Target: ', item)
                # print('Path: ', dict[item])

                # open the valid paths and extract the data
                with open(dict[item], newline='\n') as f:

                    reader = csv.DictReader(f, delimiter=',')

                    self.selected_file_counter += 1

                    # get header names
                    metric_list = reader.fieldnames

                    # each survey in the csv file (1 row = 1 survey)
                    for index, row in enumerate(reader):

                        # print("ROWWW -- ",row)
                        # print('Index: ', index)
                        # print('-----')

                        # loop through the non-header rows
                        for metric_index, new_item in enumerate(row):

                            # skip non relevant headers
                            if metric_index in range(0,10):
                                continue

                            # extract relevant data and save in database
                            else:
                                self.metric_question = ((metric_list[metric_index]).lower()).strip()
                                self.target_name = (self.target.lower()).strip()


                                # TODO check if it works with strings!
                                self.metric_value_data = data_type_check(row[metric_list[metric_index]])

                                # print(" METRIC NAME ", self.metric_name)
                                # print(" METRIC VALUE DATA ",self.metric_value_data)
                                # print("")

                                # print('-----')
                                # print('Metric: ', self.metric_name)
                                # print('Metric Value: ', self.metric_value_data)
                                # print('Target Name: ', self.target_name)


                                if ": " in self.metric_question:
                                    self.trimmed_value = self.metric_question.split(": ")
                                    if len(self.trimmed_value[1]) > 3:
                                        self.metric_question = self.trimmed_value[1]
                                        # print("Metric question ---", self.metric_question)
                                        # print("Metric question trimmed ---", self.trimmed_value[1])


                                sql_metrics = "select * from metric where lower(metric_question) = (?) and lower(target_name) = (?)"
                                retrieve_metrics = self.data_object.query_with_par(sql_metrics, (self.metric_question, self.target_name))

                                for metric_item in retrieve_metrics:
                                    self.metric_id = metric_item[0]
                                    self.metric_data_type = metric_item[10]

                                    # TODO change name in tool (Whole number, decimal, etc..)
                                    if self.metric_data_type == 'int' :
                                        self.data_int = int(self.metric_value_data)
                                        reset_data('data_int')

                                    elif self.metric_data_type == 'bool' :
                                        self.data_bool = self.metric_value_data
                                        reset_data('data_bool')

                                    elif self.metric_data_type == 'float' :
                                        if isinstance(self.metric_value_data, str):
                                            self.metric_value_data = self.metric_value_data.replace(',', '')

                                        self.data_float = float(self.metric_value_data)
                                        reset_data('data_float')

                                    else:
                                        self.data_str = self.metric_value_data
                                        reset_data('data_string')


                                    metric_value = (self.measuring_point_id,
                                                    self.metric_id,
                                                    self.file_id,
                                                    self.data_bool,
                                                    self.data_str,
                                                    self.data_int,
                                                    self.data_float)

                                    # Load into database
                                    self.data_object.create_metric_value(metric_value)

                                # print('Metric_value DATABASE', metric_value)
                                # print('-----')

        # retrieve metrics and answer options from database
        sql_test = "select * from metric"
        test_sql_object = self.data_object.query_no_par(sql_test)

        # extract answer options and clean data
        for item in test_sql_object:
            options = item[7]
            if options is not None:
                option_list = options.split(";")
                stripped_option_list = [s.strip() for s in option_list]
                # print(stripped_option_list)

        # status message
        tk.Label(frame,
                 textvariable=self.status_load_data,
                 font='Helvetica 12', foreground='red').grid(row=3, column=0,
                                                             padx=(10, 0), pady=5,
                                                             sticky='w')

        self.status_load_data.set(str(self.selected_file_counter) + " file(s) were loaded in.")


    def fill_table(self, tree):

        def replace_none_values(value):
            if value:
                return value
            else:
                return ""

        for metric in self.data_list:
            metric_name = replace_none_values(metric[0])
            amount = replace_none_values(metric[1])
            value_min = replace_none_values(metric[2])
            value_max = replace_none_values(metric[3])
            value_mean = replace_none_values(metric[4])
            value_modus = replace_none_values(metric[5])
            value_median = replace_none_values(metric[6])

            if isinstance(value_modus, list):
                temp_list = ''
                for item in value_modus:
                    if temp_list:
                        temp_list += ' - ' + str(item)
                    else:
                        temp_list = str(item)
                value_modus = temp_list


            self.tree.insert("", tk.END, values=(metric_name, amount,
                                                 value_min, value_max,
                                                 value_mean, value_modus, value_median))

    def update_table(self, tree, frame):

        # empty treeview
        for i in tree.get_children():
            tree.delete(i)

        # empty in database !
        frame.update()

        # refill with updated data
        self.fill_table(tree)

    # def validate_vis_inputs(self, target, time_frame):
    #
    #     print("target: ---", target)
    #     print("time_frame: ---", time_frame)
    #
    #     if target and time_frame:
    #         self.visualisation_get_metrics(target, time_frame)


    def visualisation_get_metrics(self, target, time_frame):

        def remap_target(target):

            if target == "Project Provider":
                return 'project_provider'
            elif target == "Community School Leader":
                return 'community_school_leader'
            elif target == "Teacher":
                return 'teacher'
            else:
                return 'student'

        unique_metric_ids = []
        metrics_target = []
        time_list = []

        for index, time in enumerate(time_frame):
            if time:
                time_list.append(index + 1)

        if time_list:

            # select the unique metrics from metric_value database
            sql_unique = "select distinct metric_id from metric_value where measuring_point_id in ({seq})".format(seq=','.join(['?'] * len(time_list)))
            retrieve_unique_metrics = self.data_object.query_with_par(sql_unique, time_list)

            for metric in retrieve_unique_metrics:
                metric_id = metric[0]
                unique_metric_ids.append(metric_id)

            # retrieve from db if unique metric is in metric database
            sql_metrics_id = "select * from metric where metric_id in ({seq})".format(seq=','.join(['?'] * len(unique_metric_ids)))
            retrieve_metrics_target = self.data_object.query_with_par(sql_metrics_id, unique_metric_ids)

            for metric in retrieve_metrics_target:
                metric_id = metric[0]
                metric_target = metric[8]
                metric_name = metric[1]
                metric_data_type = metric[5]

                if metric_target == remap_target(target) and metric_data_type != 'String':
                    metrics_target.append(metric_name)

            # print('metrics_target ', metrics_target)
            return metrics_target

    def remap_target(self, target):

        if target == "Project Provider":
            return 'project_provider'
        elif target == "Community School Leader":
            return 'community_school_leader'
        elif target == "Teacher":
            return 'teacher'
        else:
            return 'student'

    def calculate_data(self, time_frame, target):

        self.data_list = []
        self.unique_metrics = []

        def remap_timeframe(time_frame):

            if time_frame == "Start of project":
                return 1
            elif time_frame == "Halfway point of project":
                return 2
            elif time_frame == "End of project":
                return 3
            else:
                return 4

        user_target = self.remap_target(target)
        user_time_frame = remap_timeframe(time_frame)

        def create_table_row(metric_name, metric_entries, values_list, metric_type, data_type, data_list):

            metric_min = None
            metric_max = None
            metric_average = None
            metric_modus = None
            metric_median = None

            def caluculate_modus(value_list):
                c = Counter(value_list)
                return [k for k, v in c.items() if v == c.most_common(1)[0][1]]

            if data_type == 'int' or data_type == 'float':
                metric_min = min(values_list)
                metric_max = max(values_list)
                metric_average = round(statistics.mean(values_list),1)
                metric_modus = caluculate_modus(values_list)
                metric_median = round(statistics.median(values_list),1)

            if data_type == 'string':
                metric_modus = caluculate_modus(values_list)

                # print('min: ', metric_min)
                # print('max: ', metric_max)
                # print('mean: ', metric_average)
                # print('modus: ', metric_modus)
                # print('median: ', metric_median)
                # print('')

            calculated_row = [metric_name, metric_entries, metric_min,
                              metric_max, metric_average, metric_modus, metric_median]

            # print('TO BE INSERTED ROW: ', calculated_row)
            # print('')
            self.data_list.append(calculated_row)

        def data_type_index(data_type):
            if data_type == 'bool':
                return 4

            elif data_type == 'int':
                return 6

            elif data_type == 'float':
                return 7

            else:
                return 5


        metric_entries = 0

        # select the unique metrics from metric_value database
        sql_unique = "select distinct metric_id from metric_value"
        retrieve_unique_metrics = self.data_object.query_no_par(sql_unique)

        # loop through the unique metrics
        for unique_metric in retrieve_unique_metrics:


            metric_id = unique_metric[0]

            # retrieve metric_name
            sql_metric_name = "select * from metric where metric_id = (?)"
            retrieve_metric_name = self.data_object.query_with_par(sql_metric_name, ((metric_id),))

            metric_target_check = ((retrieve_metric_name[0][8]).lower()).strip()

            if metric_target_check == user_target:

                metric_name = ((retrieve_metric_name[0][1]).lower()).strip()
                metric_type = ((retrieve_metric_name[0][5]).lower()).strip()
                data_type = retrieve_metric_name[0][10]

                # add unique metrics in metrics_value db to list
                self.unique_metrics.append((metric_name, metric_id, data_type, metric_type))

                # print('---Unique Metrics---')
                # print('Metric ID: ', metric_id)
                # print('Metric Name: ', metric_name)
                # print('Metric Type: ', metric_type )
                # print('Data Type: ', data_type)
                #
                # print('METRIC ID? ', ((metric_id),)[0])
                # print('USER TIME FRAME? ', ((user_time_frame),)[0] )

            else:
                continue

        for metric in self.unique_metrics:

            values_list = []
            unique_metric_id = metric[1]

            # print ('METRIC: ', metric)
            # retrieve the rows from a unique metric
            sql_collect_rows = "select * from metric_value where metric_id = (?) and measuring_point_id = (?)"
            retrieve_collected_rows = self.data_object.query_with_par(sql_collect_rows, (((unique_metric_id),)[0],
                                                                                         (((user_time_frame),)[0]))
                                                                      )

            # print('METRIC ', metric)
            # print('METRIC ', unique_metric_id)
            # print ('RETRIEVE COLLECTED ROWS ',retrieve_collected_rows)

            # rows for every unique metric
            for entry_counter, row in enumerate(retrieve_collected_rows):
                metric_entries = entry_counter + 1
                # print('Row: ', entry_counter, '-', row)
                # print('data_type_index(data_type) ', data_type_index(metric[2]))

                if row[data_type_index(metric[2])] is not None:
                    values_list.append(row[data_type_index(metric[2])])

            # print("# of rows: ", metric_entries)
            # print("")

            if values_list:
                create_table_row(metric[0], metric_entries, values_list, metric[3], metric[2], self.data_list)

            else:
                continue

    def delete_frame(self, frame):

        if frame is not None:
            frame.destroy()

    def make_table(self, frame, timeframe, target):

        TableMargin = tk.Frame(frame, width=1200, height=500)
        TableMargin.pack(side="top", fill="both", expand='True')

        self.scrollbary = tk.Scrollbar(TableMargin, orient='vertical')
        self.scrollbarx = tk.Scrollbar(TableMargin, orient='horizontal')

        # make tree
        self.tree = ttk.Treeview(TableMargin,
                                 columns=("Metric Name",
                                          "# of responses",
                                          "Min",
                                          "Max",
                                          "Mean",
                                          "Modus",
                                          "Median"),
                                 selectmode="extended",
                                 yscrollcommand=self.scrollbary.set,
                                 xscrollcommand=self.scrollbarx.set,
                                 height=400)

        self.scrollbary.config(command=self.tree.yview)
        self.scrollbary.pack(side="right", fill="y")

        self.scrollbarx.config(command=self.tree.xview)
        self.scrollbarx.pack(side="bottom", fill="both", expand='True')

        # make tree headings
        self.tree.heading('Metric Name', text="Metric Name", anchor='w')
        self.tree.heading('# of responses', text="# of responses", anchor='w')
        self.tree.heading('Min', text="Min", anchor='w')
        self.tree.heading('Max', text="Max", anchor='w')
        self.tree.heading('Mean', text="Mean", anchor='w')
        self.tree.heading('Modus', text="Modus", anchor='w')
        self.tree.heading('Median', text="Median", anchor='w')

        # make tree columns
        self.tree.column('#0', stretch='no', minwidth=0, width=0)
        self.tree.column('#1', stretch='no', minwidth=0, width=400)
        self.tree.column('#2', stretch='no', minwidth=0, width=120)
        self.tree.column('#3', stretch='no', minwidth=0, width=120)
        self.tree.column('#4', stretch='no', minwidth=0, width=120)
        self.tree.column('#5', stretch='no', minwidth=0, width=120)
        self.tree.column('#6', stretch='no', minwidth=0, width=200)
        self.tree.column('#7', stretch='no', minwidth=0, width=200)

        # place tree
        self.tree.pack(fill='both',
                       padx=10)

        # if len(self.tree.get_children()) == 0:
        #     print('NOPS')

    def create_canvas_frame(self, frame):
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

        # create toolbar and place
        toolbar = NavigationToolbar2Tk(self.canvas, frame)
        toolbar.update()
        self.canvas.get_tk_widget().pack()

    def remap_data_type(self, data_type):
        if data_type == 'float':
            return 7
        elif data_type == 'int':
            return 6
        elif data_type == 'bool':
            return 4
        else:
            return 5

    def create_visualisations(self, target_group, point, metric, frame):

        print('target_group ---', target_group)
        print('point ---', point)
        print('metric ---', metric)
        print("")

        time_list = []
        value_list_sop = []
        value_list_hop = []
        value_list_eop = []
        value_list_yap = []
        score_list = []

        value_list_all = [value_list_sop,
                          value_list_hop,
                          value_list_eop,
                          value_list_yap]

        for index, time in enumerate(point):
            if time:
                time_list.append(index + 1)

        # TODO select the graph type based on the metric

        cleaned_target = self.remap_target(target_group)

        # -------------------
        # retrieve data from db
        sql_data = "select * from metric where lower(target_name) = (?) and lower(metric_name) = (?)"
        retrieve_sql_data = self.data_object.query_with_par(sql_data, (cleaned_target, (metric).lower()))

        metric_id = retrieve_sql_data[0][0]
        metric_question_type = retrieve_sql_data[0][5]
        metric_data_type = retrieve_sql_data[0][10]
        metric_question = retrieve_sql_data[0][4]

        figure_for_plot = Figure(figsize=(12, 4.2), dpi=100)
        self.canvas = FigureCanvasTkAgg(figure_for_plot, master=frame)

        if metric_question_type == 'Likert_6' or metric_question_type == "Likert_7":
            self.plot_figure_1 = figure_for_plot.add_subplot(1,2,1, polar=True)
            self.plot_figure_2 = figure_for_plot.add_subplot(1,2,2, polar=True)

        else:
            self.plot_figure = figure_for_plot.add_subplot()

        print("Metric ID ", metric_id)

        for time_unit in time_list:
            sql_metric = "select * from metric_value where metric_id = (?) and measuring_point_id = (?)"
            retrieve_metrics = self.data_object.query_with_par(sql_metric, (metric_id, time_unit))

            print("retrieve_metrics ", retrieve_metrics)

            for item in retrieve_metrics:
                data_value = item[self.remap_data_type(metric_data_type)]
                value_list_all[(time_unit - 1)].append(data_value)

        # -------------------
        # scoring likert scales
        def score_likert(list, isLikert_7):
            score = 0

            score_1 = score_2 = score_3 = score_4 = score_5 = score_6 = score_7 = 0

            score_list_6 = [score_1, score_2, score_3, score_4, score_5, score_6]
            score_list_7 = [score_1, score_2, score_3, score_4, score_5, score_6, score_7]

            for point in list:
                print("point: ", point)

                if isLikert_7:
                    score_list_7[(c.DataTypes.likert_7).index(point)] += c.DataTypes.likert_7_score[point]
                else:
                    score_list_6[(c.DataTypes.likert_6).index(point)]  += c.DataTypes.likert_6_score[point]

            print('score_list_7: ', score_list_7)

            if isLikert_7:
                return score_list_7
            else:
                return score_list_6

        def get_label_time(index):
            if index == 0:
                return 'Start of project'
            elif index == 1:
                return 'Halfway of project'
            elif index == 2:
                return 'End of project'
            else:
                return 'Year after end of project'

        # -------------------
        # numerical data
        def create_bar_chart(y_values):

            x = ['Start','Halfway','End','Year after']
            y = []
            width = 0.4


            for time_frame in y_values:
                if time_frame :
                    rounded_mean = round(statistics.mean(time_frame), 1)
                    y.append(rounded_mean)
                else:
                    y.append(0)

            self.plot_figure.bar(x, y, width)

            long_label = metric.replace("(", "\n(")

            x_label = 'Time frame'
            y_label = "Average " + long_label.lower()
            title_plot = "Average " + metric.lower() + "\n per time frame"

            # text with y values
            for i, value in enumerate(y):
                if not value:
                    self.plot_figure.text(i, value, str(value), color='black', fontweight='bold')
                else:
                    self.plot_figure.text(i, 0.9 * value, str(value), color='white', fontweight='bold')

            self.plot_figure.set_xlabel(x_label)
            self.plot_figure.set_ylabel(y_label)
            self.plot_figure.set_title(title_plot)

        # bool data
        def create_stacked_bar_chart_bool(y_values):

            x = ['Start','Halfway','End','Year after']
            y1 = []
            y2 = []
            width = 0.35

            for item in y_values:
                if item:
                    counter = Counter(item)
                    y1.append(counter['yes'])
                    y2.append(counter['no'])
                else:
                    y1.append(0)
                    y2.append(0)

            self.plot_figure.bar(x, y1, width, label='Yes')
            self.plot_figure.bar(x, y2, width, bottom=y1, label='No')

            y_label = metric
            title = metric_question

            # text with y values
            for i, value in enumerate(y1):
                if not value:
                    self.plot_figure.text(i, value, str(value), color='black', fontweight='bold')
                else:
                    self.plot_figure.text(i, 0.9 * value, str(value), color='white', fontweight='bold')

            # text with y values
            for i, value in enumerate(y2):
                if not value:
                    self.plot_figure.text(i, value + y1[i], str(value), color='black', fontweight='bold')
                else:
                    self.plot_figure.text(i, 0.9 * (value + y1[i]), str(value), color='white', fontweight='bold')

            self.plot_figure.set_xlabel([0,1,2,3])
            self.plot_figure.set_ylabel(y_label)
            self.plot_figure.set_title(title)
            self.plot_figure.legend()

        # likert data
        def create_radar_chart(y_values):

            categories = []
            y = []
            color_line_list = ['tab:blue', 'tab:green', 'tab:red', 'tab:purple']
            color_fill_list = ['deepskyblue', 'mediumseagreen', 'lightcoral', 'mediumpurple']

            isLikert_7 = True

            if metric_question_type.lower() == 'likert_7':
                categories = c.DataTypes.likert_7_show
            else:
                isLikert_7 = False
                categories = c.DataTypes.likert_6_show

            categories = [*categories, categories[0]]


            for item in y_values:
                if item:
                    score = score_likert(item, isLikert_7)
                    y.append(score)
                else:
                    if isLikert_7:
                        y.append([0, 0, 0, 0, 0, 0, 0])
                    else:
                        y.append([0, 0, 0, 0, 0, 0])

            value_counter_left = 0
            value_counter_right = 0

            for index, item in enumerate(y):

                item = [*item, item[0]]
                counter = Counter(item)

                if index == 0 or index == 1:
                    if counter[0] != 8:
                        label_loc = np.linspace(start=0, stop=2 * np.pi, num=len(item))

                        self.plot_figure_1.set_xticks(label_loc)
                        self.plot_figure_1.set_xticklabels(categories, size = 9)

                        self.plot_figure_1.set_yticks(np.arange(0, (max(item) + 10)))

                        self.plot_figure_1.plot(label_loc, item, color=color_line_list[index], label = get_label_time(index))
                        self.plot_figure_1.fill(label_loc, item, color=color_fill_list[index], alpha=0.1)


                        value_counter_left += 1

                    else:
                        if index == 1:
                            if value_counter_left:
                                continue
                            else:
                                figure_for_plot.delaxes(figure_for_plot.axes[0])

                else:
                    if counter[0] != 8:
                        label_loc = np.linspace(start=0, stop=2 * np.pi, num=len(item))

                        self.plot_figure_2.set_xticks(label_loc)
                        self.plot_figure_2.set_xticklabels(categories, size = 9)

                        self.plot_figure_2.set_yticks(np.arange(0, (max(item) + 10)))

                        self.plot_figure_2.plot(label_loc, item, color = color_line_list[index], label = get_label_time(index))
                        self.plot_figure_2.fill(label_loc, item, color=color_fill_list[index], alpha=0.1)

                        value_counter_right += 1

                    else:
                        if index == 3:
                            if value_counter_right:
                                continue
                            else:
                                figure_for_plot.delaxes(figure_for_plot.axes[1])

            figure_for_plot.legend(prop={'size': 8})

        # scale data
        def create_horizontal_chart():
            print("horizontal bar chart (scale)")

        # multiple choice data
        def create_stacked_bar_chart_mc():

            x = ['Start', 'Halfway', 'End', 'Year after']
            y1 = []
            y2 = []
            width = 0.35

            for item in y_values:
                if item:
                    counter = Counter(item)
                    y1.append(counter['yes'])
                    y2.append(counter['no'])
                else:
                    y1.append(0)
                    y2.append(0)

            self.plot_figure.bar(x, y1, width, label='Yes')
            self.plot_figure.bar(x, y2, width, bottom=y1, label='No')

            y_label = metric
            title = metric_question

            # text with y values
            for i, value in enumerate(y1):
                if not value:
                    self.plot_figure.text(i, value, str(value), color='black', fontweight='bold')
                else:
                    self.plot_figure.text(i, 0.9 * value, str(value), color='white', fontweight='bold')

            # text with y values
            for i, value in enumerate(y2):
                if not value:
                    self.plot_figure.text(i, value + y1[i], str(value), color='black', fontweight='bold')
                else:
                    self.plot_figure.text(i, 0.9 * (value + y1[i]), str(value), color='white', fontweight='bold')

            self.plot_figure.set_xlabel([0, 1, 2, 3])
            self.plot_figure.set_ylabel(y_label)
            self.plot_figure.set_title(title)
            self.plot_figure.legend()

        # -------------------

        self.create_canvas_frame(frame)

        if (metric_question_type.lower()) == "numerical":
            create_bar_chart(value_list_all)

        elif (metric_question_type.lower()) == "boolean":
            create_stacked_bar_chart_bool(value_list_all)

        elif metric_question_type.lower().startswith("likert"):
            create_radar_chart(value_list_all)

        elif (metric_question_type.lower()) == "scale":
            create_horizontal_chart()

        elif (metric_question_type.lower()) == "multiple_choice":
            create_stacked_bar_chart_mc()


















        # print('--- create_visualisations')
        # print('TARGET GROUP: ', target_group)
        # print('POINT: ', point)
        # print('METRIC: ', metric)
        # print('')

class ImpactEvaluation(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        self.tree_rows = []
        self.row_list = []

    def get_data_object(self, data):
        self.data_object = data

    # evaluation treeview
    def create_treeview(self, frame):

        TableMargin = tk.Frame(frame, width=1200, height=500)
        TableMargin.pack(side="top", fill="both", expand='True')

        self.scrollbary = tk.Scrollbar(TableMargin, orient='vertical')
        self.scrollbarx = tk.Scrollbar(TableMargin, orient='horizontal')

        # make tree
        self.tree = ttk.Treeview(TableMargin,
                                 columns=("Metric Name",
                                          "Target group",
                                          "Demographic scope",
                                          "Target for metric",
                                          "Increase / Decrease",
                                          "Current average",
                                          "% of target reached"),
                                 selectmode="extended",
                                 yscrollcommand=self.scrollbary.set,
                                 xscrollcommand=self.scrollbarx.set,
                                 height=400
                                 )


        self.scrollbary.config(command=self.tree.yview)
        self.scrollbary.pack(side="right", fill="y")

        self.scrollbarx.config(command=self.tree.xview)
        self.scrollbarx.pack(side="bottom", fill="both", expand='True')

        # make tree headings
        self.tree.heading('Metric Name', text="Metric Name", anchor='w')
        self.tree.heading('Target group', text="Target group", anchor='w')
        self.tree.heading('Demographic scope', text="Demographic scope", anchor='w')
        self.tree.heading('Target for metric', text="Target for metric", anchor='w')
        self.tree.heading('Increase / Decrease', text="Increase / Decrease", anchor='w')
        self.tree.heading('Current average', text="Current average", anchor='w')
        self.tree.heading('% of target reached', text="% of target reached", anchor='w')


        # make tree columns
        self.tree.column('#0', stretch='no', minwidth=0, width=0)
        self.tree.column('#1', stretch='no', minwidth=0, width=400)
        self.tree.column('#2', stretch='no', minwidth=0, width=120)
        self.tree.column('#3', stretch='no', minwidth=0, width=150)
        self.tree.column('#4', stretch='no', minwidth=0, width=150)
        self.tree.column('#5', stretch='no', minwidth=0, width=150)
        self.tree.column('#6', stretch='no', minwidth=0, width=150)
        self.tree.column('#7', stretch='no', minwidth=0, width=150)

        # place tree
        self.tree.pack(fill='both',
                       padx=10,
                       pady=10)

        self.make_rows()

    def remap_target_to_show(self, target):

        if target == "project_provider":
            return 'Project Provider'
        elif target == "community_school_leader":
            return 'Community School Leader'
        elif target == "teacher":
            return 'Teacher'
        else:
            return 'Student'

    def remap_target(self, target):
        if target == "Project Provider":
            return 'project_provider'
        elif target == "Community School Leader":
            return 'community_school_leader'
        elif target == "Teacher":
            return 'teacher'
        else:
            return 'student'

    def refresh_tree(self):

        try:

            for i in self.tree.get_children():
                self.tree.delete(i)

            self.make_rows()

        except:
            print('Please load in data')


    def calculate_target_mean(self, metric_id):

        values_list = []
        average = 0
        data_bool = data_str = data_int = data_float = False

        # look up the rows in db
        sql_values = "select *  from metric_value where metric_id = (?)"
        retrieve_values = self.data_object.query_with_par(sql_values, (metric_id,))

        # check data_type
        if retrieve_values[0][4]:
            data_bool = True
        elif retrieve_values[0][5]:
            data_str = True
        elif retrieve_values[0][6]:
            data_int = True
        elif retrieve_values[0][7]:
            data_float = True

        # skip string
        for item in retrieve_values:
            if item[6]:
                values_list.append(item[6])
            elif item[7]:
                values_list.append(item[7])
            elif item[4]:
                values_list.append(item[4])
            elif item[5]:
                values_list.append(item[5])
            else:
                continue

        # if int or float type
        if data_int or data_float:
            mean = statistics.mean(values_list)

        elif data_str:
            print('To Fix')
        elif data_bool:
            print('To Fix')

        # print("values_list, ", values_list)

        if values_list:
            return(mean)
        else:
            return(None)


    def make_rows(self):

        unique_ids = []
        self.row_list = []

        metric_id = None
        metric_name = None
        target_group = None
        demo_scope = None
        metric_target = None
        increase_decrease = None
        target_reached = None

        def remap_increase_decrease(bool):
            if bool:
                return "Increase"
            else:
                return "Decrease"

        # select the unique metrics from metric_value database
        sql_unique = "select distinct metric_id from metric_value order by metric_id"
        retrieve_unique_metrics = self.data_object.query_no_par(sql_unique)

        for metric in retrieve_unique_metrics:
            unique_ids.append(metric[0])

        # get the metric name and target group from each unique id
        sql_metrics = "select * from metric where metric_id in ({seq})".format(
            seq=','.join(['?'] * len(unique_ids)))
        retrieve_sql_metrics = self.data_object.query_with_par(sql_metrics, unique_ids)

        for metric in retrieve_sql_metrics:

            metric_id = None
            metric_name = None
            target_group = None
            demo_scope = None
            metric_target = None
            increase_decrease = None
            target_reached = None

            metric_id = metric[0]
            metric_name = metric[1]
            target_group = metric[8]

            target_mean = self.calculate_target_mean(metric_id)

            # look in metric_target db
            sql_targets = "select * from metric_target where metric_id = (?)"
            retrieve_sql_targets = self.data_object.query_with_par(sql_targets, (metric_id,))

            # if no metric_target
            if not retrieve_sql_targets:
                demo_scope = "all"
                metric_target = "not specified"
                increase_decrease = '-'
                target_reached = '-'

            else:
                # if no metric_value
                if retrieve_sql_targets[0][2] is None:

                    metric_target = "not specified"
                    increase_decrease = '-'
                    target_reached = '-'

                    if retrieve_sql_targets[0][4] == "":
                        demo_scope = "all"
                    else:
                        demo_scope = retrieve_sql_targets[0][4]

                else:

                    if retrieve_sql_targets[0][4] == "":
                        demo_scope = "all"
                    else:
                        demo_scope = retrieve_sql_targets[0][4]

                    metric_target =retrieve_sql_targets[0][2]
                    increase_decrease =retrieve_sql_targets[0][1]

                    if increase_decrease:
                        target_reached = (target_mean / metric_target) * 100
                    else:
                        target_reached = (metric_target / target_mean) * 100

                    target_reached = round(target_reached, 1)

                    increase_decrease = remap_increase_decrease(increase_decrease)

                    # print("metric_target: ", metric_target)
                    # print("target_mean: ", target_mean)
                    # print("target_reached: ", target_reached)

            self.row_list.append((metric_name,
                            self.remap_target_to_show(target_group),
                            demo_scope,
                            metric_target,
                            increase_decrease,
                            round(target_mean, 1),
                            target_reached))

            self.tree.insert("", tk.END, values=(metric_name, self.remap_target_to_show(target_group),
                                                 demo_scope, metric_target,
                                                 increase_decrease, round(target_mean, 1), target_reached))


        #
        # for item in row_list:
        #     print('Row: ---',item)

class ScrollableFrame(ttk.Frame):

    # ref: https://blog.teclado.com/tkinter-scrollable-frames/
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        self.canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)

        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)

        self.canvas.bind('<Enter>', self._bound_to_mousewheel)
        self.canvas.bind('<Leave>', self._unbound_to_mousewheel)

        scrollbar.pack(side="right", fill="y")

    # https://stackoverflow.com/questions/17355902/tkinter-binding-mousewheel-to-scrollbar
    def _bound_to_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")