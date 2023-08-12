import unittest
import os, sys
srcFolder = os.path.realpath(os.getcwd() + '/../src/lib')
sys.path.insert(0, srcFolder)
from command import Command

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
          


if __name__ == '__main__':
    unittest.main()        

