import unittest
import os, sys
srcFolder = os.path.realpath(os.getcwd() + '/../src')
sys.path.insert(0, srcFolder)
import agent

class TestAgent(unittest.TestCase):

    def cloneRepoTest(self):
        #TODO: Some temporary location is needed where tests will be performed
        agent.cloneRepository('testrepo', 'testrepoview')

if __name__ == '__main__':
    unittest.main()