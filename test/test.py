import os
import subprocess
import argparse

#Clone test repo to be shared between all test files



for file in os.listdir("."):
    if not os.path.isdir(file) and file.endswith(".py") and file != __file__ and file != 'test_base.py':
        p = subprocess.Popen(['python', file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout,stderr = p.communicate();        
        if (p.returncode != 0):
            print("{file} FAIL ({exitcode})".format(file=file,exitcode=p.returncode))
        else:
            print("{file} OK".format(file=file))

