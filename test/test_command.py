import unittest
import os, sys
srcFolder = os.path.realpath(os.getcwd() + '/../src/lib')
sys.path.insert(0, srcFolder)
from command import Command
import logging
logging.basicConfig(level=logging.DEBUG)

class TestCommand(unittest.TestCase):

    def testSimpleCommand(self):

        command = Command(['git', 'clone', 'ssh://git@github.com/somerepo.git'])
        commandArr = command.getArray()
        assert('git' == commandArr[0])
        assert('clone' == commandArr[1])
        assert('ssh://git@github.com/somerepo.git' == commandArr[2])


    def testAddGitConfigCommand(self):
        command = Command(['git', 'clone'])
        command.add(['--config', "core.sshCommand=ssh -p {port}".format(port=2222), 'ssh://git@github.com/somerepo.git'])
        commandArr = command.getArray()
        assert('git' == commandArr[0])
        assert('clone' == commandArr[1])
        assert('--config' == commandArr[2])
        assert('core.sshCommand=ssh -p 2222' == commandArr[3])
        assert('ssh://git@github.com/somerepo.git'== commandArr[4])


    def testMakeSureCommandIsRunWithSudo(self):
        # Second argument is True, which means that command should be run with sudo
        command = Command('apt-get update', True)
        commandArr = command.getArray()
        assert('sudo' == commandArr[0])
        assert('apt-get' == commandArr[1])
        assert('update' == commandArr[2])

    def testIsCommandWithRedirect(self):
        command = Command(['ls', '>', 'test.txt'])
        assert(command.hasRedirect() == True)

    def testIsCommandWithInnerCommand(self):
        command = Command("curl -o \"/tmp/kubectl\" -LO \"https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl\"")
        assert(command.hasInnerCommand() == True)

    def testIsAndCommand(self):
        command = Command("cd /home/user/repository && docker-compose up --build -d")
        assert(command.isAndCommand() == True)

    def testBuildSShParams(self):
        command = Command([])
        command.add(['-p', '2222'])
        assert('-p 2222' == command.getAsString())
        masterCmd = Command(['--config', 'core.sshCommand=\'ssh {cmd}\''.format(cmd=command.getAsString())])
        assert('--config core.sshCommand=\'ssh -p 2222\'' == masterCmd.getAsString())

        command1 = Command([])
        command1.add(['-o StrictHostKeyChecking=no'])
        assert('-o StrictHostKeyChecking=no' == command1.getAsString())
        masterCmd1 = Command(['--config', 'core.sshCommand=\'ssh {cmd}\''.format(cmd=command1.getAsString())])
        assert('--config core.sshCommand=\'ssh -o StrictHostKeyChecking=no\'' == masterCmd1.getAsString())

        command2 = Command([])
        command2.add(['-p 2222', '-o StrictHostKeyChecking=no'])
        assert('-p 2222 -o StrictHostKeyChecking=no' == command2.getAsString())
        masterCmd2 = Command(['--config', 'core.sshCommand=\'ssh {cmd}\''.format(cmd=command2.getAsString())])
        assert('--config core.sshCommand=\'ssh -p 2222 -o StrictHostKeyChecking=no\'' == masterCmd2.getAsString())        

    def testBuildGitCloneCommandWithCustomSshParams(self):
        command = Command(['git', 'clone'])
        sshCommand = Command([])
        sshCommand.add(['-p', '2017'])
        sshCommand.add(['-o StrictHostKeyChecking=no'])
        
        if sshCommand.commandItems.__len__() > 0:
            command.add(['--config', "core.sshCommand=\"ssh {sshcmd}\""
            .format(sshcmd=sshCommand.getAsString())])

        command.add(["abc", "def"])
        assert('git clone --config core.sshCommand="ssh -p 2017 -o StrictHostKeyChecking=no" abc def' == command.getAsString())

    def testBuildCommandWithTeeRedirect(self):
        command = Command("echo abc")
        path = "/tmp/hedge_output_" +"dcde1d58-6742-43bf-bf42-80b2d31b3b76"
        command.add("| tee " + path)
        assert("echo abc | tee /tmp/hedge_output_dcde1d58-6742-43bf-bf42-80b2d31b3b76" == command.getAsString()) 

    def testIsChownCommand(self):
        command = Command("chown -R user:group /home/user/repository")
        assert(command.isChownCommand() == True)

        command = Command("chmod 700 /home/user/repository")
        assert(command.isChownCommand() == False)

    def testHasWildcards(self):
        command = Command("ls -l /home/user/repository/*")
        assert(command.hasWildcards() == True)

        command = Command("ls -l /home/user/repository")
        assert(command.hasWildcards() == False)



if __name__ == '__main__':
    unittest.main()        

