import unittest
import os, sys
import grp
srcFolder = os.path.realpath(os.getcwd() + '/../src')
sys.path.insert(0, srcFolder)
libFolder = os.path.realpath(os.getcwd() + '/../src/lib')
sys.path.insert(0, libFolder)
from test_base import TestBase
from agent import Agent

class TestUserHedge(TestBase):

    def testUserBelongsToGroup(self):

        # Make sure user does not belong to group to which we want to add it
        result = os.system("groups testuser | grep -P 'testuser\s+:\s+testgroup\s+' && echo 1 || echo 0")
        if result != 0:
            os.system('gpasswd --delete testuser testgroup')
        result = os.system("groups testuser | grep -P 'testuser\s+:\s+testgroup\s+' && echo 1 || echo 0")
        assert(result == 0)

        agent = Agent(TestBase.testDir + '/testrepo', TestBase.testDir + '/testrepoview')
        agent.ensureUserBelongsToGroup('testuser', 'testgroup')

        result = os.system("groups testuser | grep -P 'testuser\s+:\s+testgroup\s+' && echo 1 || echo 0")
        assert(result == 1)


if __name__ == '__main__':
    unittest.main()  