import unittest
import os, sys
srcFolder = os.path.realpath(os.getcwd() + '/../src')
sys.path.insert(0, srcFolder)
libFolder = os.path.realpath(os.getcwd() + '/../src/lib')
sys.path.insert(0, libFolder)
from test_base import TestBase
from agent import Agent
from commandhedge import CommandHedge

class TestCommandHedge(TestBase):

    @classmethod
    def tearDownClass(cls):
        super(TestCommandHedge, cls).tearDownClass()    
    
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

    def testSysCtlCommand(self):
        os.system('sudo sysctl -w net.bridge.bridge-nf-call-iptables=0');
        value = None
        with open('/proc/sys/net/bridge/bridge-nf-call-iptables', 'r') as file:
            value = int(file.read().strip())
        assert(value == 0)

        agent = Agent(TestBase.testDir + '/testrepo', TestBase.testDir + '/testrepoview')
        agent.runCommand('sudo sysctl -w net.bridge.bridge-nf-call-iptables=1')
        with open('/proc/sys/net/bridge/bridge-nf-call-iptables', 'r') as file:
            value = int(file.read().strip())
        assert(value == 1)
    
    def testGetCommandOutput(self):
        commandHedge =   CommandHedge(TestBase.testDir + '/testrepo', False, True, True)
        commandHedge.runCommand('echo "test"')
        assert(commandHedge.lastCommandOutput == 'test\n')
        #Make sure temporary file created to catch output is deleted
        assert(os.path.isfile(commandHedge.tmpOutputPath) == False)

    def testExecuteCommandRemotly(self):
        commandHedge = CommandHedge(TestBase.testDir + '/testrepo', False, True, True)
        commandHedge.runCommand('cat /root/c-hedge-slave.txt', 'root', 'c-hedge-slave')
        assert(commandHedge.lastCommandOutput.decode('utf-8') == 'c-hedge-slave')


if __name__ == '__main__':
    unittest.main()
