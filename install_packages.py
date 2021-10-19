import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

package_list = ['pandas', 'numpy', 'tk', 'functools', 'openpyxl', 'matplotlib', 'pyperclip']

for item in package_list:
    install(item)

