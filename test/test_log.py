import unittest
import os, sys
srcFolder = os.path.realpath(os.getcwd() + '/../src/lib')
sys.path.insert(0, srcFolder)
from log import Log

class TestLog(unittest.TestCase):

    def testAddEntry(self):
        log = Log(False)
        log.addPending("This is just a test")
        log.commitOK()
        assert("This is just a test OK" == log.flush())


        #assert('hedge' == toolkit.Toolkit.extractRepoName('/tmp/hedge'))


if __name__ == '__main__':
    unittest.main()