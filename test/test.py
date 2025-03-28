import os
import subprocess
import argparse


for file in os.listdir("."):
    if not os.path.isdir(file) and file.endswith(".py")  and file.startswith("test") and file != __file__ and file != 'test_base.py':
        p = subprocess.Popen(['python', file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout,stderr = p.communicate();        
        if (p.returncode != 0):
            print("{file} FAIL ({exitcode})".format(file=file,exitcode=p.returncode))
        else:
            print("{file} OK".format(file=file))

