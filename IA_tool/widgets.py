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

        self.checkbox_list = {}

        global selection_window
        self.selection_window = None


    def show_selection_screen(self):

        if not self.selection_window:
            self.selection_window = tk.Toplevel()
            self.selection_window.wm_title('Select Method Fragments')

            width =  self.selection_window.winfo_screenwidth()
            height =  self.selection_window.winfo_screenheight()

            # root.geometry(f'{width/2}x{height/2}')
            self.selection_window.geometry('%sx%s' % (int(width / 2.5), int(height / 1.2)))

            self.selection_window.protocol("WM_DELETE_WINDOW", self.hide_window)

            frame_method_fragments= ttk.LabelFrame( self.selection_window, text="1.3 - Select method fragments",
                                                 width=600, height=600)
            frame_method_fragments.grid_propagate(0)
            frame_method_fragments.grid(padx=(10, 0),
                                     sticky='nsew')

            # pd.DataFrame.to_csv
            # pd.DataFrame.to_excel
            # pd.DataFrame.to_csv

            # HARDCODED, CHANGE LATER!
            raw_data = pd.read_excel("C:/Users/Tiny/ IA-Tool-V1/data/method_fragments/master_list.xlsx")
            dataframe = pd.DataFrame(raw_data)

            # print(len(dataframe.category.unique()))
            # print(print(dataframe.category.unique()))

            self.make_checkboxes(dataframe,  frame_method_fragments)

            # generate button
            button_generate = tk.Button(frame_method_fragments,
                                        text='Generate',
                                        width=c.Size.button_width, height=c.Size.button_height,
                                        command=self.close_screen)

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

        print('Amount of unique values: ', len(self.unique_values ))
        counter = 0

        self.checkbox = dict()

        for item in self.unique_values:

            self.checkbox[item] = tk.Checkbutton(frame, text=item, onvalue=True, offvalue =False)
            self.checkbox[item].var = tk.BooleanVar()
            self.checkbox[item]['variable'] = self.checkbox[item].var

            if counter < 15:
                # print('Unique item: ', item)
                counter += 1
                self.checkbox[item].grid(row=counter, sticky='w')


            else:
                counter += 1
                self.checkbox[item].grid(row=(counter - 15), column=1, sticky='w')

            self.checkbox[item]['command'] = lambda w=self.checkbox[item]: self.send_category_object(w['text'], w.var.get())


    def selected_method_fragments(self, checkbox_state, checkbox_name):

        self.append_value(self.checkbox_list, checkbox_name, checkbox_state)
        print(self.checkbox_list)



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

    def close_screen(self):

        scrollbar = tk.Scrollbar(self.frame)

        scrollbar.grid(column=6, sticky='ns')

        mylist = tk.Listbox(self.frame, yscrollcommand=scrollbar.set, width=50)

        for line in self.checkbox_list:
            mylist.insert(tk.END, line)

        mylist.grid(row=6, column=0,
                    padx=(10, 0),
                    pady=2,
                    sticky='nswe')
        scrollbar.config(command=mylist.yview)

        self.hide_window()

    def retrieve_frame(self, frame):
        self.frame = frame

    def hide_window(self):
        self.selection_window.withdraw()