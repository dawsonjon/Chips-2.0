import subprocess

def open_file(filename, lineno = 1):
    subprocess.Popen("gedit {0} +{1}:1".format(filename, lineno), shell=True)

def new_file():
    subprocess.Popen("gedit", shell=True)
