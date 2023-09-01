import unittest
import os, sys
srcFolder = os.path.realpath(os.getcwd() + '/../src')
sys.path.insert(0, srcFolder)
libFolder = os.path.realpath(os.getcwd() + '/../src/lib')
sys.path.insert(0, libFolder)
from test_base import TestBase
from firewallhedge import FirewallHedge

class TestFirewallHedge(TestBase):
    
    def testSimpleRejectRule(self):

        # If the rule IS present remove it before the test
        if os.system('iptables --check INPUT -p all -s 10.0.0.10/32 -j REJECT >> /dev/null') == 0:
            os.system('iptables -D INPUT -p all -s 10.0.0.10/32 -j REJECT >> /dev/null')
            
        # Rule is NOT present
        assert(os.system('iptables --check INPUT -p all -s 10.0.0.10/32 -j REJECT >> /dev/null') != 0)

        firewall = FirewallHedge()
        firewall.addInputRejectRule('10.0.0.10/32')

        assert(os.system('iptables --check INPUT -p all -s 10.0.0.10/32 -j REJECT >> /dev/null') == 0)

    def testSimpleAcceptRule(self):
        # If the rule IS present remove it before the test
        if os.system('iptables --check INPUT -p all -s 10.0.0.11/32 -j ACCEPT >> /dev/null') == 0:
            os.system('iptables -D INPUT -p all -s 10.0.0.11/32 -j ACCEPT >> /dev/null')
            
        # Rule is NOT present
        assert(os.system('iptables --check INPUT -p all -s 10.0.0.11/32 -j ACCEPT >> /dev/null') != 0)

        firewall = FirewallHedge()
        firewall.addInputAcceptRule('10.0.0.11/32')

        assert(os.system('iptables --check INPUT -p all -s 10.0.0.11/32 -j ACCEPT >> /dev/null') == 0)

if __name__ == '__main__':
    unittest.main()  
