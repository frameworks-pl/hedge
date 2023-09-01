import unittest
import os, sys
srcFolder = os.path.realpath(os.getcwd() + '/../src')
sys.path.insert(0, srcFolder)
libFolder = os.path.realpath(os.getcwd() + '/../src/lib')
sys.path.insert(0, libFolder)
from test_base import TestBase
from symlinkhedge import SymlinkHedge
from agent import Agent

class TestSymlinkHedge(TestBase):

    @classmethod
    def tearDownClass(cls):
        super(TestSymlinkHedge, cls).tearDownClass()    

    def testNewSymlink(self):
        
        #if there is a symlink, remove it first
        if (os.path.islink('/tmp/bootstrap.log')):
            os.remove('/tmp/bootstrap.log')
        assert(not os.path.isfile('/tmp/bootstrap.log'))

        #now create it
        symlinkhedge = SymlinkHedge()
        symlinkhedge.ensureSymlink('/var/log/bootstrap.log', '/tmp/bootstrap.log')
        assert(os.path.islink('/tmp/bootstrap.log'))
        

    def testChangeExsitingSymlink(self):  

        #TODO: Rather than testing it on 'python' a temp symlink should be created for this

        if (os.path.islink('/tmp/python')):
            os.remove('/tmp/python')        
        assert(not os.path.islink('/tmp/python'))
        os.symlink('/usr/bin/python2.7', '/tmp/python')
        assert(os.readlink('/tmp/python') == '/usr/bin/python2.7')

        #replace existing link with new one
        symlinkhedge = SymlinkHedge()
        symlinkhedge.ensureSymlink('/usr/bin/python3.4', '/tmp/python')
        assert(os.path.islink('/tmp/python'))
        assert(os.readlink('/tmp/python') == '/usr/bin/python3.4')

        

    def testRemoveSymlink(self):
        if (os.path.islink('/tmp/python')):
            os.remove('/tmp/python')        
        assert(not os.path.islink('/tmp/python'))
        os.symlink('/usr/bin/python2.7', '/tmp/python')
        assert(os.readlink('/tmp/python') == '/usr/bin/python2.7')

        symlinkhedge = SymlinkHedge()
        symlinkhedge.removeSymlink('/tmp/python')

        assert(not os.path.isfile('/tmp/python'))

    def testCreateSymlinkUsingAgent(self):

        if (os.path.islink('/tmp/python')):
            os.remove('/tmp/python')        
        assert(not os.path.islink('/tmp/python'))

        agent = Agent(TestBase.testDir + '/testrepo', TestBase.testDir + '/testrepoview')
        agent.ensureSymlink('/usr/bin/python2.7', '/tmp/python')

        assert(os.path.islink('/tmp/python'))
        


if __name__ == '__main__':
    unittest.main()