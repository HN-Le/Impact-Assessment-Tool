import tkinter as tk
from tkinter import ttk
from . import views as v
from tkPDFViewer import tkPDFViewer as pdf
from tkinter import filedialog
import os

class PDFViewer(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        global file_path
        file_path = ''
        self.file_path = file_path


    # PDF viewer
    def create_popup(self, path):

        # get file stats
        stats = os.stat(path)
        print('Size of file is', stats.st_size, 'bytes')

        win_popup = tk.Toplevel()
        win_popup.wm_title(path)

        # Initializing tk
        root = win_popup
        # Set the width and height of our root window.
        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()

        # root.geometry(f'{width/2}x{height/2}')
        root.geometry('%sx%s' % (int(width / 2.5), int(height / 1.2)))

        # creating object of ShowPdf from tkPDFViewer.
        v1 = pdf.ShowPdf()

        # Adding pdf location and width and height.
        v2 = v1.pdf_view(root,
                         pdf_location=path
                         )

        # Placing Pdf in gui.
        v2.pack()






    def show_project_goals(self):
        self.create_popup(self.file_path)
        print('SHOW PROJECT GOALS: ', self.file_path)



    # def show_project_model(self):
    #     create_popup(path_project_model)

    def get_file_path(self):
        filename = filedialog.askopenfilename()
        print('Selected:', filename)

        # widget = button.widget
        # info = widget.grid_info()
        # row = info['row']
        # column = info['column']

        # label = ttk.Label(button, text=filename)


        self.file_path = filename

