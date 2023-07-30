import unittest
import os, sys
import subprocess
srcFolder = os.path.realpath(os.getcwd() + '/../src')
sys.path.insert(0, srcFolder)
libFolder = os.path.realpath(os.getcwd() + '/../src/lib')
sys.path.insert(0, libFolder)
from apthedge import AptHedge
from test_base import TestBase
import argparse



class TestAptHedge(TestBase):

    @classmethod
    def setUpClass(self):

        #This will prepare test repo
        TestBase.setUpClass()

        #TODO: in python 3.3 or newer we can stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
        p = subprocess.Popen(['dpkg-query', '-W', 'ncdu'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout,stderr = p.communicate()
        #p.returncode == None means success (package exists)
        if p.returncode == 0:
            p = subprocess.Popen(['apt-get', 'remove', '-y', 'ncdu'])
            p.communicate()


            
    def testInstall(self):

        #TODO: setUpClass needs to run agent to clone repo!!!


        #Make sure ncdu is NOT installed
        p = subprocess.Popen(['dpkg-query', '-W', 'ncdu'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.communicate()
        assert(p.returncode != 0)

        aptHedge = AptHedge(TestBase.testDir + '/testrepoview')        
        aptHedge.ensurePackages( ['ncdu'] )

        p = subprocess.Popen(['dpkg-query', '-W', 'ncdu'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.communicate()        
        assert(p.returncode == 0)

        

if __name__ == '__main__':

    unittest.main()    