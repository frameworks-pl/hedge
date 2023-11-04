import unittest
import os, sys
srcFolder = os.path.realpath(os.getcwd() + '/../src')
sys.path.insert(0, srcFolder)
libFolder = os.path.realpath(os.getcwd() + '/../src/lib')
sys.path.insert(0, libFolder)
from agent import Agent

from test_base import TestBase
import logging

logging.basicConfig(level=logging.DEBUG)

class TestFileHedge(TestBase):
    
    @classmethod
    def setUpClass(self):

        #This will prepare test repo
        TestBase.setUpClass()

    def testEnsureDir(self):

        if os.path.isdir('/tmp/testdir'):
            os.system('rm -rf /tmp/testdir')
        assert(os.path.isdir('/tmp/testdir') == False)

        logging.debug(TestBase.testDir)

        agent = Agent(TestBase.testDir + '/testrepo', TestBase.testDir + '/testrepoview')
        agent.ensureDir('/tmp/testdir')
        assert(os.path.isdir('/tmp/testdir') == True)


if __name__ == '__main__':
    unittest.main()