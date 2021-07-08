import sys
import tkinter as tk
from tkinter import ttk
from . import views as v
from tkPDFViewer import tkPDFViewer as pdf
from tkinter import filedialog
import os
import webbrowser
import numpy as np
import pandas as pd
from . import constants as c
from varname import nameof
from . import models as m
from tkinter import font


class PDFViewer(tk.Frame):

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
        return self.file_path.split("/")[-1]

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




    def show_selection_screen(self):

        if not self.selection_window:
            self.selection_window = tk.Toplevel()
            self.selection_window.wm_title('Select Method Fragments')

            width =  self.selection_window.winfo_screenwidth()
            height =  self.selection_window.winfo_screenheight()


            # root.geometry(f'{width/2}x{height/2}')
            self.selection_window.geometry('%sx%s' % (int(width-100), int(height)))

            self.selection_window.protocol("WM_DELETE_WINDOW", self.hide_window)

            frame_method_fragments= ttk.LabelFrame( self.selection_window, text="1.3 - Select method fragments",
                                                 width=1200, height=400)
            frame_method_fragments.grid_propagate(0)
            frame_method_fragments.grid(padx=(10, 0),
                                     sticky='nsew')

            frame_add_metric = ttk.LabelFrame(self.selection_window, text="Add additional metrics",
                                                    width=1200, height=400)
            frame_add_metric.grid_propagate(0)
            frame_add_metric.grid(padx=(10, 0),
                                        sticky='nsew')

            self.add_metric(frame_add_metric)

            dataframe_object = m.surveyModel()
            dataframe = dataframe_object.dataframe

            # remove dataframe from function ?
            self.make_checkboxes(dataframe, frame_method_fragments)

            # generate button
            button_generate = tk.Button(frame_method_fragments,
                                        text='Generate',
                                        width=c.Size.button_width, height=c.Size.button_height,
                                        command=self.generate_questions)

            button_generate.grid(row=18, column=0,
                                 padx=(10, 0),
                                 pady=2,
                                 sticky='w')

        else:
            self.selection_window.deiconify()



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

        self.create_list('project_provider')

        combobox_target = ttk.Combobox(
            self.frame,
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

        # # ---------------------------------------------------------------------------

        # hide select method fragment screen to show questions
        self.hide_window()

    def retrieve_frame(self, frame):
        self.frame = frame

    def hide_window(self):
        self.selection_window.withdraw()

    def add_metric(self, frame):

        label_metric = tk.Label(frame, text='Metric')

        label_metric.grid(row=2, column=0,

                                            pady=(10, 0),
                                            sticky='w')

        user_metric = tk.StringVar()
        user_metric_input = ttk.Entry(frame, width = 15, textvariable=user_metric)
        user_metric_input.grid(row=3, column=0, padx=2)

        label_fragment = tk.Label(frame, text='Method fragment')
        label_fragment.grid(row=2, column=1,

                          pady=(10, 0),
                          sticky='w')

        combobox = ttk.Combobox(
            frame,
            values=["Option 1", "Option 2", "Option 3"])
        combobox.grid(row=3, column=1, padx=2)

        label_type= tk.Label(frame, text='Data type')
        label_type.grid(row=2, column=2,
                          pady=(10, 0),
                          sticky='w')

        combobox_2 = ttk.Combobox(
            frame,
            values=["Option 1", "Option 2", "Option 3"])
        combobox_2.grid(row=3, column=2, padx=2)


        button_add = tk.Button(frame,
                                    text='Add',
                                    width=c.Size.button_width, height=c.Size.button_height,
                                    command= lambda: [self.add_button(combobox, combobox_2, user_metric)])

        button_add.grid(row=3, column=3,
                             padx=(10, 0),
                             sticky='w')

        button_remove = tk.Button(frame,
                               text='Remove',
                               width=c.Size.button_width, height=c.Size.button_height,
                               command='')

        button_remove.grid(row=3, column=4,
                        padx=(10, 0),
                        sticky='w')


    def add_button(self, combobox, combobox_2, text):
        combobox.current()
        combobox_2.current()

        combobox.get()
        combobox_2.get()
        print('COMBOBOX 1: ', combobox.get())
        print('COMBOBOX 2: ', combobox_2.get())
        print('TEXT BOX: ', text.get())

    def get_target(self, event=None):
        self.input_combobox = event.widget.get()

        target_key = self.chose_target_list[self.input_combobox]


        self.create_list(target_key)

    def create_list(self, target_key):

        self.dataframe = m.surveyModel()

        label_survey_questions_community = tk.Label(self.frame,
                                                    text='Generated questions for: ')

        label_survey_questions_community.grid(row=4, column=0,
                                              padx=(20, 0),
                                              pady=(10, 0),
                                              sticky='w')

        scrollbar_v_community_list = tk.Scrollbar(self.frame)
        scrollbar_h_community_list = tk.Scrollbar(self.frame)

        self.community_list = tk.Listbox(self.frame, yscrollcommand=scrollbar_v_community_list.set,
                                         xscrollcommand=scrollbar_h_community_list.set,
                                         width=140, height=20)

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
                self.community_list.insert(tk.END, ' ' + item)
                self.community_list.insert(tk.END, '      ' + 'Metric: ' + metrics[index])
                self.community_list.insert(tk.END, '      ' + 'Type:  ' + types[index])
                self.community_list.insert(tk.END, '\n')