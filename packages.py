import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# 'functools',
package_list = ['pandas', 'numpy', 'tk',  'openpyxl', 'matplotlib', 'pyperclip']

for item in package_list:
    install(item)

