import unittest
import os, sys, subprocess
srcFolder = os.path.realpath(os.getcwd() + '/../src')
sys.path.insert(0, srcFolder)
libFolder = os.path.realpath(os.getcwd() + '/../src/lib')
sys.path.insert(0, libFolder)
from test_base import TestBase
from agent import Agent
from toolkit import Toolkit

class TestUserHedge(TestBase):

    @classmethod
    def tearDownClass(cls):
        super(TestUserHedge, cls).tearDownClass()    

    def testUserBelongsToGroup(self):

        # Make sure user does not belong to group to which we want to add it
        groups = Toolkit.getUserGroups('testuser')
        if 'testgroup' in groups:
            os.system('gpasswd --delete testuser testgroup')
        groups = Toolkit.getUserGroups('testuser')        
        assert('testgroup' not in groups)

        agent = Agent(TestBase.testDir + '/testrepo', TestBase.testDir + '/testrepoview')
        agent.ensureUserBelongsToGroup('testuser', 'testgroup')

        groups = Toolkit.getUserGroups('testuser')
        assert('testgroup' in groups)


if __name__ == '__main__':
    unittest.main()  