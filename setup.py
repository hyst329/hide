from cx_Freeze import setup, Executable
import sys
from hdver import verstrs

__author__ = 'tram'

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(name="hide",
      version=verstrs,
      description="F4/Helen IDE",
      options={
          "build_exe": {
              "create_shared_zip": False
          },
          "bdist_msi": {
              "add_to_path": False
          }
      },
      executables=[Executable("hdmain.py", base=base)],
      requires=['cx_Freeze'])