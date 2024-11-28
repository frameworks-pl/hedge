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

    def findFile(self, search_path, pattern):
        files = [f for f in os.listdir(search_path) if os.path.isfile(os.path.join(search_path, f))]
        backup_file = None
        for f in files:
            print(f)
            if re.match(pattern, f):
                backup_file = f        

        return backup_file


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
        backup_file = self.findFile('/tmp', r"^testBackup_\d{8}_\d{6}_hedge\.txt")
        assert(backup_file != None)        

        #file without extension
        toolkit.Toolkit.backupFile('/tmp/noExttestBackup')
        backup_file = self.findFile('/tmp', r"^noExttestBackup_\d{8}_\d{6}_hedge")


if __name__ == '__main__':
    unittest.main()        