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
        os.system('rm -rf /tmp/testBackup*')
        os.system('rm -rf /tmp/noExttestBackup*')
        assert(os.path.exists('/tmp/testBackup.txt') == False)
        os.system("echo 'xyz' > /tmp/testBackup.txt")
        os.system("echo '123' > /tmp/noExttestBackup")

        #file with extendsion        
        toolkit.Toolkit.backupFile('/tmp/testBackup.txt')        
        backup_files = toolkit.Toolkit.findFiles('/tmp', r"^testBackup_\d{8}_\d{6}_hedge\.txt")
        assert(len(backup_files) == 1)

        #file without extension
        toolkit.Toolkit.backupFile('/tmp/noExttestBackup')
        backup_files = toolkit.Toolkit.findFiles('/tmp', r"^noExttestBackup_\d{8}_\d{6}_hedge")
        assert(len(backup_files) == 1)


if __name__ == '__main__':
    unittest.main()        