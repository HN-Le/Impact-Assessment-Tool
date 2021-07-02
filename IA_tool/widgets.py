import sys
import tkinter as tk
from tkinter import ttk
from . import views as v
from tkPDFViewer import tkPDFViewer as pdf
from tkinter import filedialog
import os
import webbrowser

class PDFViewer(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        global file_path
        file_path = ''
        self.file_path = file_path


    # # PDF viewer
    # def create_popup(self, path):

        # # get file stats
        # stats = os.stat(path)
        # print('Size of file is', stats.st_size, 'bytes')
        #
        # root = tk.Toplevel()
        # root.wm_title(path)
        #
        # width = root.winfo_screenwidth()
        # height = root.winfo_screenheight()
        #
        # # root.geometry(f'{width/2}x{height/2}')
        # root.geometry('%sx%s' % (int(width / 2.5), int(height / 1.2)))
        #
        # # creating object of ShowPdf from tkPDFViewer.
        # v1 = pdf.ShowPdf()
        # print('INITIAL: ', v1.img_object_li)
        #
        # v1.pdf_view(root, pdf_location=path).pack()
        #
        # # v2 = v1.pdf_view(root, pdf_location=path)
        # # v2.pack()
        #
        # print('TEST: ', v1.img_object_li)
        #
        # # print('LENGTH IMAGES 44', length_images)
        #
        # # if length_images > 0:
        # #     v1.img_object_li = []
        # #
        # #     print('WHY ')
        # #     print('LENGTH IMAGES 58', length_images)



    def show_project_goals(self):
        # self.create_popup(self.file_path)
        webbrowser.open(self.file_path)

    def get_file_path(self):
        filename = filedialog.askopenfilename()
        print('Selected:', filename)
        self.file_path = filename

