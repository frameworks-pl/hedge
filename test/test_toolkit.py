import unittest
import os, sys
srcFolder = os.path.realpath(os.getcwd() + '/../src')
sys.path.insert(0, srcFolder)
import zipfile
import logging
import random
import string
import toolkit
import datetime
import re

class TestToolkit(unittest.TestCase):

    def testExtractRepoName(self):
        assert('hedge' == toolkit.Toolkit.extractRepoName('/tmp/hedge'))

    def testExtractFromHttpAddress(self):
        assert('k8s' == toolkit.Toolkit.extractRepoName('https://github.com/frameworks-pl/k8s'))

    def testBackupFile(self):

        # 1. Given files to backup
        os.system('rm -rf /tmp/testBackup*')
        os.system('rm -rf /tmp/noExttestBackup*')
        assert(os.path.exists('/tmp/testBackup.txt') == False)
        os.system("echo 'xyz' > /tmp/testBackup.txt")
        os.system("echo '123' > /tmp/noExttestBackup")

        # 2. When file with extension is backed up then backup is crated in location of the file
        toolkit.Toolkit.backupFile('/tmp/testBackup.txt')        
        backup_files = toolkit.Toolkit.findFiles('/tmp', r"^testBackup_\d{8}_\d{6}_hedge\.txt")
        assert(len(backup_files) == 1)

        # 3. When file without extension is backed up then backup is created in location of the file
        toolkit.Toolkit.backupFile('/tmp/noExttestBackup')
        backup_files = toolkit.Toolkit.findFiles('/tmp', r"^noExttestBackup_\d{8}_\d{6}_hedge")
        assert(len(backup_files) == 1)

    def testBackupFileToBackupDir(self):

        #1. Given a file to backup
        os.system('rm -rf /tmp/testGoToBackupDir.txt')
        assert(os.path.exists('/tmp/testGoToBackupDir.txt'))
        os.system('echo -n testGoToBackupDir > /tmp/testGoToBackupDir.txt')

        #2. When backup file is created with backup dir specified
        toolkit.Toolkit.backupFile('/tmp/testGoToBackupDir.txt', '/tmp/backup')

        #3 Then backupfile is created relative to backup dir root
        
        


if __name__ == '__main__':
    unittest.main()        