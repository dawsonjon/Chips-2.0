import subprocess

def open_file(filename):
    subprocess.Popen("gedit {0}".format(filename), shell=True)

def new_file():
    subprocess.Popen("gedit", shell=True)
