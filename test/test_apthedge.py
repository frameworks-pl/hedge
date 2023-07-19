import unittest
import os, sys
import subprocess
srcFolder = os.path.realpath(os.getcwd() + '/../src')
sys.path.insert(0, srcFolder)
libFolder = os.path.realpath(os.getcwd() + '/../src/lib')
sys.path.insert(0, libFolder)
from apthedge import AptHedge

class TestAptHedge(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        #TODO: in python 3.3 or newer we can stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
        p = subprocess.Popen(['dpkg-query', '-W', 'ncdu'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout,stderr = p.communicate();
        #p.returncode == None means success (package exists)
        if p.returncode == None:
            p = subprocess.Popen('apt-get', 'remove' '-y', 'ncdu')
            stdout,stderr = p.communicate();

            
    def testInstall(self):

        #TODO: setUpClass needs to run agent to clone repo!!!


        #Make sure ncdu is NOT installed
        p = subprocess.Popen(['dpkg-query', '-W', 'ncdu'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.communicate();
        assert(p.returncode != None)

        aptHedge = AptHedge()
        aptHedge.ensurePackages(['ncdu'])

        p.communicate()
        assert(p.returncode == None)

        

if __name__ == '__main__':
    unittest.main()