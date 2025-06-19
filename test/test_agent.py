import unittest
import os, sys, pwd
srcFolder = os.path.realpath(os.getcwd() + '/../src')
sys.path.insert(0, srcFolder)
libFolder = os.path.realpath(os.getcwd() + '/../src/lib')
sys.path.insert(0, libFolder)
from agent import Agent
import re

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

    def testCloneFromBranch(self):
        agent = Agent(TestBase.testDir + '/testrepo', None)
        agent.cloneRepo("testbranch")
        assert(os.path.isfile('/root/.hedge/testrepo/onlyonbranch/onlyonbranch.txt'))

    def testCloneFromBranchAndThenCheckout(self):
        agent = Agent(TestBase.testDir + '/testrepo', None)
        agent.cloneRepo("testbranch")
        #initial clone of a branch - onlyonbranch.txt file should be there
        assert(os.path.isfile('/root/.hedge/testrepo/onlyonbranch/onlyonbranch.txt'))

        #now checkout master (default) branch, onlyonbranch.txt should not be there
        agent.cloneRepo("master")
        assert(os.path.isfile('/root/.hedge/testrepo/onlyonbranch/onlyonbranch.txt') == False)

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
        agent = Agent(TestBase.testDir + '/testrepo', TestBase.testDir + '/testrepoview')
        params = {"testDir" : TestBase.testDir}        
        agent.execute('build', params) #This should execute default target 'build', which will create /tmp/build.txt with content HedgeBuild
        assert(os.path.isfile(TestBase.testDir + '/filehedge/testHedgeFile.txt'))

    def testExecuteFromDifferntModule(self):
        agent = Agent(TestBase.testDir + '/testrepo', TestBase.testDir + '/testrepoview')
        #params = {"testDir" : TestBase.testDir}
        params = {"testDir" : TestBase.testDir}
        agent.execute('targetfromothermodule', params, 'anotherhedge')
        assert(os.path.isfile(TestBase.testDir + '/filehedge/targetfromothermodule.txt' ))


    def testEnsureFileViaAgent(self):
        agent = Agent(TestBase.testDir + '/testrepo', TestBase.testDir + '/testrepoview')
        params = {"testDir" : TestBase.testDir}
        agent.execute('copyfile', params)
        assert(os.path.isfile(TestBase.testDir + '/filehedge/testEnsureFileViaAgent.txt'))


    def testCloneMultipleTimes(self):
        agent = Agent(TestBase.testDir + '/testrepo', TestBase.testDir + '/testrepoview')
        try:
            agent.cloneRepo()
        except:
            self.fail("Cloning repo for the second time failed.")


    def testDownloadFileToTmpFolder(self):
        agent = Agent(TestBase.testDir + '/testrepo', TestBase.testDir + '/testrepoview')
        # we are trying here to download a 'well known' file from interent
        # if this fails, it could be connection issue or this location being no longer valid
        if os.path.isfile("{tmp}/kubectl".format(tmp=agent.getTempPath())):
            os.remove("{tmp}/kubectl".format(tmp=agent.getTempPath()))
        agent.runCommand("curl -o \"{tmp}/kubectl\" -k -s -LO \"https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl\"".format(tmp=agent.getTempPath()))
        assert(os.path.isfile("{tmp}/kubectl".format(tmp=agent.getTempPath())))

    def testDestinationFolder(self):
        agent = Agent('/some/localy/created/git/repo')
        assert(agent.repoDestinationPath == '/root/.hedge/repo')

        agent1 = Agent("ssh://somehost.com/some/remote/git/repo")
        assert(agent1.repoDestinationPath == '/root/.hedge/repo')

        agent2 = Agent('https://github.com/frameworks-pl/hedge')
        assert(agent2.repoDestinationPath == '/root/.hedge/hedge')

    def testRunCommandAndGetOutput(self):
        agent = Agent(TestBase.testDir + '/testrep', TestBase.testDir + '/testrepoview')
        agent.runCommand("echo 'hello world'", True, True)

    def testRunCommandRemotelyAndGetOutput(self):
        agent = Agent(TestBase.testDir + '/testrep', TestBase.testDir + '/testrepoview')
        agent.runCommand('cat /root/c-hedge-slave.txt', True, True,  'root', 'c-hedge-slave')
        assert(agent.lastCommandOutput == 'c-hedge-slave')

    def testRunCommandRemotelyWithNonDefaultKey(self):
        agent = Agent(TestBase.testDir + '/testrep', TestBase.testDir + '/testrepoview')
        agent.runCommand('cat /root/c-hedge-unknown.txt', True, True,  'root', 'c-hedge-unknown', '/root/.ssh/hedge_unknown')
        assert(agent.lastCommandOutput == 'c-hedge-unknown')

    def testExecuteCommandRemotlyNonDefaultPort(self):
        agent = Agent(TestBase.testDir + '/testrep', TestBase.testDir + '/testrepoview')
        agent.runCommand('cat /root/c-hedge-2222.txt', True, True, 'root', 'c-hedge-2222', None, 2222)
        assert(agent.lastCommandOutput == 'c-hedge-2222')

    def testReadSymlinkFromRemoteHost(self):
        agent = Agent(TestBase.testDir + '/testrep', TestBase.testDir + '/testrepoview')
        agent.runCommand('readlink /backup/backup_latest', True, True, 'root', 'c-hedge-2222', None, 2222)
        stripped = agent.lastCommandOutput.rstrip()
        assert(stripped == '/backup/testbackup.7z')

    def testChownWithoutOutput(self):
        agent = Agent(TestBase.testDir + '/testrep', TestBase.testDir + '/testrepoview')
        agent.runCommand('chown -R root:root /root/scripts/*.7z')
        pattern = r'^sudo chown -R root:root /root/scripts/\*\.7z\s+\|\s+tee /tmp/hedge_output_[a-f0-9\-]+ OK$'
        print(agent.lastHedgeObject.log.lastOutput)
        match = re.match(pattern, agent.lastHedgeObject.log.lastOutput)
        assert(match)

    def testEnsureDirectoryWithUserGroupAndPermissions(self):
    
        # 1. Given a user belonging to a specific group
        if os.path.isdir('/tmp/dirowned'):
            os.system('rm -rf /tmp/dirowned')
        assert(os.path.isdir('/tmp/dirowned') == False)
        
        # 2. When directory creation is requested for the user, group and permissions
        agent = Agent(TestBase.testDir + '/testrep', TestBase.testDir + '/testrepoview')
        agent.ensureDir('/tmp/dirowned', 'testuser', 'testuser', '770')
        
        # 3. Then created directory belongs to the user, group and has proper permissions
        stat_info = os.stat('/tmp/dirowned')
        assert(pwd.getpwuid(stat_info.st_uid).pw_name == 'testuser')

    def testListAvailableTargets(self):

        #1. Given sample hedge script with targets
        from sample_hedge import Hedge
        assert(Hedge is not None)

        #2. When collect_targets target called, then list of targets is returned
        agent = Agent(TestBase.testDir + '/testrep', TestBase.testDir + '/testrepoview')
        hedge = Hedge(agent.repoDestinationPath)
        targets = agent.listTargets(hedge)
        #targets = hedge.collect_targets(agent, {})

        #3. Then all available targets are collected
        print(targets)
        assert(2 == len(targets.keys()))
        assert(3 == len(targets['target1']['parameters']))
        assert('self' == targets['target1']['parameters'][0])
        assert('agent' == targets['target1']['parameters'][1])
        assert('params' == targets['target1']['parameters'][2])
        assert(3 == len(targets['target2']['parameters']))
        assert('self' == targets['target2']['parameters'][0])
        assert('agent' == targets['target2']['parameters'][1])
        assert('params' == targets['target2']['parameters'][2])



        



if __name__ == '__main__':
    unittest.main()