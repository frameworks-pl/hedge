import unittest
import os, sys
srcFolder = os.path.realpath(os.getcwd() + '/../src')
sys.path.insert(0, srcFolder)
from agent import Agent
import zipfile
import logging
import random
import string
import toolkit

class TestAgent(unittest.TestCase):

    def testExtractRepoName(self):
        assert('hedge' == toolkit.Toolkit.extractRepoName('/tmp/hedge'))

if __name__ == '__main__':
    unittest.main()        