import tkinter as tk
from tkinter import ttk
from datetime import datetime
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import filedialog
from . import widgets as w


class ProjectDefinition(tk.Frame):
    def __init__(self, parent, *args):
        super().__init__(parent, *args)

        # Build
        project_goals = tk.LabelFrame(self, text="Project Goals")
        goal_model = tk.LabelFrame(self, text="Goal Model")
        methode_fragments = tk.LabelFrame(self, text="Methode Fragments")

        project_goals.grid(row=0, column=0, sticky=(tk.W + tk.E))
        goal_model.grid(row=1, column=0, sticky=(tk.W + tk.E))
        methode_fragments.grid(row=2, column=0, sticky=(tk.W + tk.E))

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)


class Tabs(tk.Frame):

    def __init__(self, parent, *args):
        super().__init__(parent, *args)

        names = ['1 - Project Definition', '2 - Data Collection', '3 - Data Analysis', '4 - Impact Evaluation']
        self.nb = self.create_notebook(names)

    def create_notebook(self, names):
        nb = MyNotebook(self, names)
        nb.pack()

        def add_label(parent, text, row, column):
            label = tk.Label(parent, text=text)
            label.grid(row=row, column=column, sticky=tk.N, pady=10)
            return label

        # Add some labels to each tab
        tab = nb.tabs['1 - Project Definition']
        for i in range(3):
            add_label(tab, 'test' + str(i), i, 0)

        tab = nb.tabs['2 - Data Collection']
        for i in range(3):
            add_label(tab, 'goodie' + str(i), 0, i)

        tab = nb.tabs['3 - Data Analysis']
        for i in range(3):
            add_label(tab, 'mana' + str(i), i, i)

        return nb


class MyNotebook(ttk.Notebook):

    # A customised Notebook that remembers its tabs in a dictionary
    def __init__(self, master, names):
        super().__init__(master, width=(master.winfo_screenwidth()-150), height=(master.winfo_screenheight()-150))
        print("WIDTH:  ", master.winfo_screenwidth())
        print("HEIGHT:  ", master.winfo_screenheight())

        # Create tabs & save them by name in a dictionary
        self.tabs = {}
        for name in names:
            self.tabs[name] = tab = ttk.Frame(self)
            self.add(tab, text=name)


class MenuCreation(tk.Tk):
    """The input form for our widgets"""

    def __init__(self, parent, *args):
        super().__init__(parent, *args)

    def create_menu(self):
        # create menu bar
        menu_bar = Menu(self)
        self.config(menu=menu_bar)

        # menu item: file
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self._quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # menu item: data
        data_menu = Menu(menu_bar, tearoff=0)
        data_menu.add_command(label="Tables")
        data_menu.add_command(label="Graph")
        menu_bar.add_cascade(label="Data", menu=data_menu)

        # menu item: help
        help_menu = Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About")
        menu_bar.add_cascade(label="Help", menu=help_menu)

    # Exit GUI cleanly
    def _quit(self):
        self.quit()
        self.destroy()
        exit()