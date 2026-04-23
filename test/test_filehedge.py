import unittest
import os, sys, re, pwd
import shutil
import filecmp
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

    def testEnsureFileWithBackup(self):
        
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
                
        backup_files = toolkit.Toolkit.findFiles(agent.fileBackupPath + '/tmp', r"^existingfile_\d{8}_\d{6}_hedge\.txt")
        assert(len(backup_files) == 1)

        with open(agent.fileBackupPath + "/tmp/{fileName}".format(fileName=backup_files[0])) as file:
            new_content = file.read()
        assert(new_content == 'abc')

    def testEnsureLineInFile(self):

        # 1. Given original file
        os.system('rm -rf /tmp/sshd_config*')
        shutil.copy('./resource/sshd_config', '/tmp/sshd_config')
        assert(os.path.isfile('/tmp/sshd_config') == True)

        # 2. When I attempt to replace original line (commented out)
        agent = Agent(TestBase.testDir + '/testrepo', TestBase.testDir + '/testrepoview')
        agent.ensureLineInFile('/tmp/sshd_config', r'^#ListenAddress\s+\d+\.\d+\.\d+.\d+', 'ListenAddress 1.2.3.4')

        # 3. Then line is replaced by new content
        filecmp.clear_cache()
        assert(filecmp.cmp('./resource/sshd_config_gold', '/tmp/sshd_config', shallow=False))

    def testEnsureLineInFileWhenNoMatch(self):

        # 1. Given original file
        os.system('rm -rf /tmp/sshd_config*')
        shutil.copy('./resource/sshd_config_no_listen', '/tmp/sshd_config_no_listen')
        assert(os.path.isfile('/tmp/sshd_config_no_listen') == True)

        # 2. When I attempt to replace line
        agent = Agent(TestBase.testDir + '/testrepo', TestBase.testDir + '/testrepoview')
        agent.ensureLineInFile('/tmp/sshd_config_no_listen', r'^#ListenAddress\s+\d+\.\d+\.\d+.\d+', 'ListenAddress 1.2.3.4')

        # 3. Line is added at the end because there was no match and 
        filecmp.clear_cache()
        assert(filecmp.cmp('./resource/sshd_config_no_listen_gold', '/tmp/sshd_config_no_listen', shallow=False))

    def testEnsureLineInFileWhenAlreadyThere(self):

        # 1. Given original file
        os.system('rm -rf /tmp/sshd_config*')
        shutil.copy('./resource/sshd_config_already_there', '/tmp/sshd_config_already_there')
        assert(os.path.isfile('/tmp/sshd_config_already_there') == True)

        # 2. When I attempt to replace the line in file
        agent = Agent(TestBase.testDir + '/testrepo', TestBase.testDir + '/testrepoview')
        agent.ensureLineInFile('/tmp/sshd_config_already_there', r'^#ListenAddress\s+\d+\.\d+\.\d+.\d+', 'ListenAddress 3.4.5.6')

        # 3. File is not changed, as content is already there
        assert(filecmp.cmp('./resource/sshd_config_already_there', '/tmp/sshd_config_already_there', shallow=False))

if __name__ == '__main__':
    unittest.main()