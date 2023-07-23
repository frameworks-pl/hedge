import unittest
import string
import random
import logging
import os
import zipfile
from agent import Agent
import shutil

class TestBase(unittest.TestCase):

    testDir = None

    @classmethod
    def generateRandomString(self, length):        
        characters = string.ascii_letters + string.digits
        random_string = ''.join(random.choice(characters) for _ in range(length))
        return random_string

    @classmethod
    def setUpClass(self):
        if (os.path.isdir('/root/.hedge')):
            shutil.rmtree('/root/.hedge')
            
        logging.debug(TestBase.testDir)
        if not TestBase.testDir:
            currentDir = os.getcwd()
            TestBase.testDir = currentDir + '/tmp/' + TestBase.generateRandomString(10)
            if not os.path.isdir(TestBase.testDir + '/testrepo.zip'):
                zipRef = zipfile.ZipFile(currentDir + '/testrepo.zip', 'r')
                zipRef.extractall(TestBase.testDir)

                agent = Agent(TestBase.testDir + '/testrepo', TestBase.testDir + '/testrepoview')
                agent.cloneRepo()            