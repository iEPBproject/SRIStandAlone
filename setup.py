'''
Created on 8 abr 2024

@author: Efinovatic
'''
import sys
from cx_Freeze import setup, Executable



# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "excludes": ["tkinter", "unittest",'scipy','matplotlib','pandas','pytz','wx','email','html','http','logging','pydoc_data','urllib'],
    # "include_msvcr": True
}



setup(
    name="sri2StandAlone",
    version="0.1",
    description="Sri Stand Alone Application",
    options={"build_exe": build_exe_options,
                  },
    executables=[Executable("sriStandAlone.py")],

)