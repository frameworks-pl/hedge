import unittest
import os, sys
srcFolder = os.path.realpath(os.getcwd() + '/../src')
sys.path.insert(0, srcFolder)
libFolder = os.path.realpath(os.getcwd() + '/../src/lib')
sys.path.insert(0, libFolder)
from test_base import TestBase
from agent import Agent

class TestFirewallHedge(TestBase):
    
    def testSimpleRejectRule(self):
        firewall = FireWallHedge(self)
        firewall.addRejectRule('10.0.0.10/24')

