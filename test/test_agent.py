import unittest
import os, sys
srcFolder = os.path.realpath(os.getcwd() + '/../src')
sys.path.insert(0, srcFolder)
import agent
import zipfile
import logging
import random
import string

logging.basicConfig(level=logging.DEBUG)

class TestAgent(unittest.TestCase):

    testDir = ''

    def generateRandomString(self, length):        
        characters = string.ascii_letters + string.digits
        random_string = ''.join(random.choice(characters) for _ in range(length))
        return random_string

    def setUp(self):

        if not self.testDir:
            currentDir = os.getcwd()        
            self.testDir = currentDir + '/tmp/' + self.generateRandomString(10)

            if not os.path.isdir(self.testDir + '/testrepo.zip'):
                zipRef = zipfile.ZipFile(currentDir + '/testrepo.zip', 'r')
                zipRef.extractall(self.testDir)

    def testCloneRepo(self):
        agent.cloneRepo(self.testDir + '/testrepo', self.testDir + '/testrepoview')
        logging.debug(self.testDir)
        assert(os.path.isdir(self.testDir + "/testrepoview"))


    def testEnsuerFile(self):
        targetFontName = self.generateRandomString(10) + '.ttf'        
        #TODO: Turn agent into class, so that we can initialize it (work dir) before we run it
        agent.ensureFile('/fonts/myfont.tff', '/usr/local/share/fonts/hedge/' + targetFontName)
        assert(os.path.isfile('/usr/local/share/fonts/hedge/' + targetFontName))


if __name__ == '__main__':
    unittest.main()