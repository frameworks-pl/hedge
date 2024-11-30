import unittest
import os, sys, re
srcFolder = os.path.realpath(os.getcwd() + '/../src')
sys.path.insert(0, srcFolder)
libFolder = os.path.realpath(os.getcwd() + '/../src/lib')
sys.path.insert(0, libFolder)
from agent import Agent

from test_base import TestBase
import logging
import toolkit

logging.basicConfig(level=logging.DEBUG)

class TestFileHedge(TestBase):
    
    @classmethod
    def setUpClass(self):

        #This will prepare test repo
        TestBase.setUpClass()

    def testEnsureDir(self):

        if os.path.isdir('/tmp/testdir'):
            os.system('rm -rf /tmp/testdir')
        assert(os.path.isdir('/tmp/testdir') == False)

        logging.debug(TestBase.testDir)

        agent = Agent(TestBase.testDir + '/testrepo', TestBase.testDir + '/testrepoview')
        agent.ensureDir('/tmp/testdir')
        assert(os.path.isdir('/tmp/testdir') == True)

    def testEnsureFileViaSsh(self):

        #make sure file we want to copy from remote host is not here
        if os.path.isfile('/tmp/testbackup.7z'):
            os.system('rm -rf /tmp/testbackup.7z')
        assert(os.path.isfile('/tmp/testbackup.7z') == False)

        agent = Agent(TestBase.testDir + '/testrepo', TestBase.testDir + '/testrepoview')
        agent.ensureFileViaSsh('/backup/testbackup.7z', '/tmp/testbackup.7z', 'root', 'c-hedge-unknown', '/root/.ssh/hedge_unknown')
        assert(os.path.isfile('/tmp/testbackup.7z') == True)

    def testEnsureFileViaSshNonDefaultPort(self):

        #make sure file we want to copy from remote host is not here
        if os.path.isfile('/tmp/testbackup2222.7z'):
            os.system('rm -rf /tmp/testbackup2222.7z')
        assert(os.path.isfile('/tmp/testbackup2222.7z') == False)

        agent = Agent(TestBase.testDir + '/testrepo', TestBase.testDir + '/testrepoview')
        agent.ensureFileViaSsh('/backup/testbackup2222.7z', '/tmp/testbackup2222.7z', 'root', 'c-hedge-2222', None, 2222)
        assert(os.path.isfile('/tmp/testbackup2222.7z') == True)

    def testEnsureOriginalBackup(self):
        
        # 1. Given old existing file in a directory
        os.system('rm -rf /tmp/existingfile*')
        os.system("echo -n abc > /tmp/existingfile.txt")
        assert(os.path.isfile('/tmp/existingfile.txt') == True)

        # 2. When the file is replaced by hedge
        agent = Agent(TestBase.testDir + '/testrepo', TestBase.testDir + '/testrepoview')
        agent.ensureFile('/filehedge/testEnsureOriginalBackedup.txt', '/tmp/existingfile.txt')

        # 3. Then file has new content and backup of old file is created
        with open('/tmp/existingfile.txt') as file:
            content = file.read()
        assert(content == 'testEnsureOriginalBackedup')
        
        backup_files = toolkit.Toolkit.findFiles('/tmp', r"^existingfile_\d{8}_\d{6}_hedge\.txt")
        assert(len(backup_files) == 1)

        with open("/tmp/{fileName}".format(fileName=backup_files[0])) as file:
            new_content = file.read()
        print(new_content)
        assert(new_content == 'abc')

        



if __name__ == '__main__':
    unittest.main()