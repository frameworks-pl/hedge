import unittest
import os, sys
srcFolder = os.path.realpath(os.getcwd() + '/../src')
sys.path.insert(0, srcFolder)
libFolder = os.path.realpath(os.getcwd() + '/../src/lib')
sys.path.insert(0, libFolder)
from test_base import TestBase
from symlinkhedge import SymlinkHedge

class TestSymlinkHedge(TestBase):

    def testNewSymlink(self):
        
        #if there is a symlink, remove it first
        if (os.path.islink('/tmp/bootstrap.log')):
            os.remove('/tmp/bootstrap.log')
        assert(not os.path.isfile('/tmp/bootstrap.log'))

        #now create it
        symlinkhedge = SymlinkHedge(TestBase.testDir + '/testrepoview')
        symlinkhedge.ensureSymlink('/var/log/bootstrap.log', '/tmp/bootstrap.log')
        assert(os.path.islink('/tmp/bootstrap.log'))
        

    def testChangeExsitingSymlink(self):
        pass

    def testRemoveSymlink(self):
        pass

if __name__ == '__main__':
    unittest.main()