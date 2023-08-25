import unittest
import os, sys
srcFolder = os.path.realpath(os.getcwd() + '/../src')
sys.path.insert(0, srcFolder)
libFolder = os.path.realpath(os.getcwd() + '/../src/lib')
sys.path.insert(0, libFolder)
from agent import Agent

from test_base import TestBase
import logging

logging.basicConfig(level=logging.DEBUG)

class TestAgent(TestBase):

    def testCloneRepo(self):
        assert(os.path.isdir(TestBase.testDir + "/testrepoview"))

    def testCloneDefaultDir(self):
        agent = Agent(TestBase.testDir + '/testrepo', None)
        agent.cloneRepo()
        assert(os.path.isdir('/root/.hedge/testrepo'))

    def testCloneOurLibFromClientScript(self):
        agent = Agent(TestBase.testDir + '/testrepo', TestBase.testDir + '/testrepoview')
        #params = {"testDir" : TestBase.testDir}
        print(sys.path)
        exit
        agent.execute('dummylibtest')

    def testEnsuerFile(self):
        targetFontName = self.generateRandomString(10) + '.tty'        
        from filehedge import FileHedge
        filehedge = FileHedge(TestBase.testDir + '/testrepoview')
        filehedge.ensureFile('/fonts/myfont.tty', '/usr/local/share/fonts/hedge/' + targetFontName)
        assert(os.path.isfile('/usr/local/share/fonts/hedge/' + targetFontName))

    def testExecuteEntryPoint(self):
        agent = Agent(None, TestBase.testDir + '/testrepoview')
        params = {"testDir" : TestBase.testDir}        
        agent.execute('build', params) #This should execute default target 'build', which will create /tmp/build.txt with content HedgeBuild
        assert(os.path.isfile(TestBase.testDir + '/filehedge/testHedgeFile.txt'))

    def testEnsureFileViaAgent(self):

        agent = Agent(None, TestBase.testDir + '/testrepoview')
        params = {"testDir" : TestBase.testDir}
        agent.execute('copyfile', params)

        assert(os.path.isfile(TestBase.testDir + '/filehedge/testEnsureFileViaAgent.txt'))

    def testCloneMultipleTimes(self):
        agent = Agent(TestBase.testDir + '/testrepo', TestBase.testDir + '/testrepoview')
        try:
            #We already cloned that repo, so second call should just run update
            agent.cloneRepo()
        except:
            self.fail("Cloning repo for the second time failed.")

    def testDownloadFileToTmpFolder(self):
        agent = Agent(TestBase.testDir + '/testrepo', TestBase.testDir + '/testrepoview')
        # we are trying here to download a 'well known' file from interent
        # if this fails, it could be connection issue or this location being no longer valid
        agent.runCommand("curl -k -LO \"https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl\" -o {tmp}/kubectl".format(tmp=agent.getTempPath()))
        assert(os.path.isfile(TestBase.testDir + "/testrepoview/{tmp}/kubectl".format(tmp=Agent.TEMP_DIR)))

        


if __name__ == '__main__':
    unittest.main()