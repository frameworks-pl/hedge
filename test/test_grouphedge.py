import unittest
import os, sys
import grp
srcFolder = os.path.realpath(os.getcwd() + '/../src')
sys.path.insert(0, srcFolder)
libFolder = os.path.realpath(os.getcwd() + '/../src/lib')
sys.path.insert(0, libFolder)
from test_base import TestBase
from agent import Agent

class TestCommandHedge(TestBase):

    @classmethod
    def tearDownClass(cls):
        super(TestCommandHedge, cls).tearDownClass()    

    def testCreateGroupIfNotExist(self):
        
        # if testgroup exists remove it first
        try:
            grp.getgrnam('testgroup')
            os.system('sudo groupdel testgroup')
        except KeyError:
            #getgrnam throws KeyError if group does not exist (which is fine)
            pass

        # now KeyError must be thrown as group should not be there!
        try:
            grp.getgrnam('testgroup')
            assert(False)
        except KeyError:
            pass
        
        agent = Agent(TestBase.testDir + '/testrepo', TestBase.testDir + '/testrepoview')
        agent.ensureGroup('testgroup')

        # now group must exist
        grinfo = grp.getgrnam('testgroup')
        assert(grinfo.gr_gid > 0)
        assert(grinfo.gr_name == 'testgroup')
        
if __name__ == '__main__':
    unittest.main()        