import sys
from cx_Freeze import setup, Executable
import os.path

# os.environ['TCL_LIBRARY'] = r"C:\Users\LENOVO\AppData\Local\Programs\Python\Python37-32\tcl\tcl8.6"
# os.environ['TK_LIBRARY'] = r"C:\Users\LENOVO\AppData\Local\Programs\Python\Python37-32\tcl\tk8.6"

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "Melody",
        version = "0.1",
        description = "Music Player!",
        options = {"build_exe": build_exe_options},
        executables = [Executable("melody.py", base=base)])
