import unittest
import os, sys
srcFolder = os.path.realpath(os.getcwd() + '/../src')
sys.path.insert(0, srcFolder)
from agent import Agent
import zipfile
import logging
import random
import string

logging.basicConfig(level=logging.DEBUG)

class TestAgent(unittest.TestCase):

    testDir = None

    @classmethod
    def generateRandomString(self, length):        
        characters = string.ascii_letters + string.digits
        random_string = ''.join(random.choice(characters) for _ in range(length))
        return random_string

    @classmethod
    def setUpClass(self):

        logging.debug(TestAgent.testDir)
        if not TestAgent.testDir:
            currentDir = os.getcwd()
            TestAgent.testDir = currentDir + '/tmp/' + TestAgent.generateRandomString(10)
            if not os.path.isdir(TestAgent.testDir + '/testrepo.zip'):
                zipRef = zipfile.ZipFile(currentDir + '/testrepo.zip', 'r')
                zipRef.extractall(TestAgent.testDir)

                agent = Agent(TestAgent.testDir + '/testrepo', TestAgent.testDir + '/testrepoview')
                agent.cloneRepo()

    def testCloneRepo(self):
        assert(os.path.isdir(TestAgent.testDir + "/testrepoview"))


    def testEnsuerFile(self):
        agent = Agent(None, TestAgent.testDir + '/testrepoview')
        targetFontName = self.generateRandomString(10) + '.tty'                
        agent.ensureFile('/fonts/myfont.tty', '/usr/local/share/fonts/hedge/' + targetFontName)
        assert(os.path.isfile('/usr/local/share/fonts/hedge/' + targetFontName))

    def testExecuteEntryPoint(self):
        agent = Agent(None, TestAgent.testDir + '/testrepoview')
        agent.execute() #This should execute default target 'build', which will create /tmp/build.txt with content HedgeBuild
        #TODO: Assert below should check if there is /tmp/build.txt exists and has content HedgeBuild
        assert(False)




if __name__ == '__main__':
    unittest.main()