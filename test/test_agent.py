import unittest
import os, sys
srcFolder = os.path.realpath(os.getcwd() + '/../src')
sys.path.insert(0, srcFolder)
libFolder = os.path.realpath(os.getcwd() + '/../src/lib')
sys.path.insert(0, libFolder)
from agent import Agent
from filehedge import FileHedge
from test_base import TestBase
import logging

logging.basicConfig(level=logging.DEBUG)

class TestAgent(TestBase):

    def testCloneRepo(self):
        assert(os.path.isdir(TestBase.testDir + "/testrepoview"))


    def testEnsuerFile(self):
        targetFontName = self.generateRandomString(10) + '.tty'                
        filehedge = FileHedge(TestBase.testDir + '/testrepoview')
        filehedge.ensureFile('/fonts/myfont.tty', '/usr/local/share/fonts/hedge/' + targetFontName)


        assert(os.path.isfile('/usr/local/share/fonts/hedge/' + targetFontName))

    def testExecuteEntryPoint(self):
        agent = Agent(None, TestBase.testDir + '/testrepoview')
        params = {"testDir" : TestBase.testDir}        
        agent.execute('build', params) #This should execute default target 'build', which will create /tmp/build.txt with content HedgeBuild
        #TODO: Assert below should check if there is /tmp/build.txt exists and has content HedgeBuild
        assert(os.path.isfile(TestBase.testDir + '/filehedge/testHedgeFile.txt'))

    def testCloneMultipleTimes(self):
        agent = Agent(TestBase.testDir + '/testrepo', TestBase.testDir + '/testrepoview')
        try:
            #We already cloned that repo, so second call should just run update
            agent.cloneRepo()
        except:
            self.fail("Cloning repo for the second time failed.")





if __name__ == '__main__':
    unittest.main()