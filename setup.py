from cx_Freeze import setup, Executable
from hdver import verstrs

__author__ = 'tram'

setup(name="hide",
      version=verstrs,
      description="F4/Helen IDE",
      options={
          "build_exe": {
              "init_script": "Console",
              "create_shared_zip": False
          },
          "bdist_msi": {
              "add_to_path": False
          }
      },
      executables=[Executable("hdmain.py")],
      requires=['cx_Freeze'])