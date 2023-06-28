import unittest
import os, sys
srcFolder = os.path.realpath(os.getcwd() + '/../src')
sys.path.insert(0, srcFolder)
import agent
import zipfile
import logging
logging.basicConfig(level=logging.DEBUG)

class TestAgent(unittest.TestCase):

    def setUp(self):
        currentDir = os.getcwd()
        if not os.path.isdir(currentDir + '/test_repo'):
            zipRef = zipfile.ZipFile(currentDir + '/testrepo.zip', 'r')
            zipRef.extractall(currentDir)

    def tearDown(self):
        currentDir = os.getcwd()
        if os.path.isdir(currentDir + "/testrepo"):
            os.remove(currentDir + "/testrepo")
        if (os.path.isdir(currentDir + "/testrepoview")):
            os.remove(currentDir + "/testrepoview")

    def testCloneRepo(self):
        #TODO: Some temporary location is needed where tests will be performed

        agent.cloneRepo('testrepo', 'testrepoview')
        assert(os.path.isdir(os.getcwd() + "/testrepoview"))


if __name__ == '__main__':
    unittest.main()