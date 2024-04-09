'''
Created on 8 abr 2024

@author: Efinovatic
'''
import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "excludes": ["tkinter", "unittest",'scipy','matplotlib','pandas','pytz','wx'],
    "zip_include_packages": ["encodings", "PySide6"],
}



setup(
    name="sri2StandAlone",
    version="0.1",
    description="My GUI application!",
    options={"build_exe": build_exe_options},
    executables=[Executable("sriStandAlone.py")],
)