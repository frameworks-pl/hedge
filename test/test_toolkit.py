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

    def testExtractFromHttpAddress(self):
        assert('k8s' == toolkit.Toolkit.extractRepoName('https://github.com/frameworks-pl/k8s'))

if __name__ == '__main__':
    unittest.main()        