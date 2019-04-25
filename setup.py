import sys 
from cx_Freeze import setup, Executable 

# GUI applications require a different base on Windows (the default is for a 
# console application). 
base = None 
if sys.platform == "win32": 
    base = "Win32GUI" 

# Dependencies are automatically detected, but it might need fine tuning. 
build_exe_options = { 
"packages": ["sys", "PyQt5"],  
} 

# 
executables = [ 
Executable("window.py", targetName="win.exe", icon=r"C:\Users\yufei.chen\Desktop\Python_scripts\logo.png")
] 

setup( name = "setup", 
version = "0.1", 
description = "Joker3D prop manager tool!", 
author = "tylerzhu", 
author_email = "saylor.zhu@gmail.com", 
options = {"build_exe": build_exe_options}, 
executables = executables, 
)
