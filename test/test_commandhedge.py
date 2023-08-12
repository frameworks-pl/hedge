import unittest
import os, sys
srcFolder = os.path.realpath(os.getcwd() + '/../src')
sys.path.insert(0, srcFolder)
libFolder = os.path.realpath(os.getcwd() + '/../src/lib')
sys.path.insert(0, libFolder)
from test_base import TestBase
from agent import Agent

class TestCommandHedge(TestBase):
    
    def testSimpleCommand(self):

        #create test file to be removed by the command
        if not os.path.exists('/tmp/testSimpleCommand.txt'):
            f = open('/tmp/testSimpleCommand.txt', 'w')
            f.write('test')
            f.close()
        assert(os.path.isfile('/tmp/testSimpleCommand.txt') == True)

        agent = Agent(TestBase.testDir + '/testrepo', TestBase.testDir + '/testrepoview')
        agent.runCommand('rm -rf /tmp/testSimpleCommand.txt')

        assert(os.path.isfile('/tmp/testSimpleCommand.txt') == False)

if __name__ == '__main__':
    unittest.main()
