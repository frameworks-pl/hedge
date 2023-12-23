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

    def testEnsureFileViaSsh(self):

        #make sure file we want to copy from remote host is not here
        if os.path.isfile('/tmp/testbackup.7z'):
            os.system('rm -rf /tmp/testbackup.7z')
        assert(os.path.isfile('/tmp/testbackup.7z') == False)

        agent = Agent(TestBase.testDir + '/testrepo', TestBase.testDir + '/testrepoview')
        agent.ensureFileViaSsh('/backup/testbackup.7z', '/tmp/testbackup.7z', 'root', 'c-hedge-unknown', '/root/.ssh/hedge_unknown')
        assert(os.path.isfile('/tmp/testbackup.7z') == True)


if __name__ == '__main__':
    unittest.main()