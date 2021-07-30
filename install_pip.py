# import os
# import pandas as pd
# from sqlite3 import Error
# import sqlite3
# import numpy as np
# import tkinter as tk
# from tkinter import ttk
# from tkinter import filedialog
# import webbrowser
# from functools import partial
# from tkinter import ttk
# from tkinter import filedialog
# import subprocess
# import sys

import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

package_list = ['pandas', 'numpy', 'tkinter', 'functools']

for item in package_list:
    install(item)