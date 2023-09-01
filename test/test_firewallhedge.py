import unittest
import os, sys
srcFolder = os.path.realpath(os.getcwd() + '/../src')
sys.path.insert(0, srcFolder)
libFolder = os.path.realpath(os.getcwd() + '/../src/lib')
sys.path.insert(0, libFolder)
from test_base import TestBase
from firewallhedge import FirewallHedge

class TestFirewallHedge(TestBase):

    @classmethod
    def tearDownClass(cls):
        cls._deleteTestRules()

    @classmethod
    def setUp(self):
        if (os.path.isfile('/etc/cont.d/firewall')):
            os.remove('/etc/cont.d/firewall')

        if (os.path.isfile('/etc/iptables/hedge-rules.sh')):
            os.remove('/etc/iptables/hedge-rules.sh')

    @classmethod
    def tearDownClass(cls):
        super(TestFirewallHedge, cls).tearDownClass()

    @classmethod
    def _deleteTestRules(cls):
        os.system('iptables -D INPUT -p all -s 10.0.0.10/32 -j REJECT >> /dev/null')
        os.system('iptables -D INPUT -p all -s 10.0.0.11/32 -j ACCEPT >> /dev/null')
        os.system('iptables -D INPUT -p tcp -s 10.0.0.12/32 --dport 5000 -j REJECT >> /dev/null')        
        os.system('iptables -D INPUT -p udp -s 10.0.0.12/32 --dport 5000 -j REJECT >> /dev/null')            
    
    def testSimpleRejectRule(self):

        assert(os.path.isfile('/etc/cont.d/firewall') == False)

        # If the rule IS present remove it before the test
        if os.system('iptables --check INPUT -p all -s 10.0.0.10/32 -j REJECT >> /dev/null') == 0:
            os.system('iptables -D INPUT -p all -s 10.0.0.10/32 -j REJECT >> /dev/null')
            
        # Rule is NOT present
        assert(os.system('iptables --check INPUT -p all -s 10.0.0.10/32 -j REJECT >> /dev/null') != 0)

        firewall = FirewallHedge(TestBase.testDir + '/testrepoview')
        firewall.addInputRejectRule('10.0.0.10/32')

        assert(os.system('iptables --check INPUT -p all -s 10.0.0.10/32 -j REJECT >> /dev/null') == 0)
        assert(os.path.isfile('/etc/cron.d/hedge-rules'))
        assert(os.path.isfile('/etc/iptables/hedge-rules.sh'))

        with open('/etc/cron.d/hedge-rules', 'r') as f:
            content = f.read()
            assert(content.find('@reboot /etc/iptables/hedge-rules.sh') == 0)

    def testRejectWithPort(self):
        # If the rule IS present remove it before the test
        if os.system('iptables --check INPUT -p tcp -s 10.0.0.12/32 --dport 5000 -j REJECT >> /dev/null') == 0:
            os.system('iptables -D INPUT -p tcp -s 10.0.0.12/32 --dport 5000 -j REJECT >> /dev/null')

        if os.system('iptables --check INPUT -p udp -s 10.0.0.12/32 --dport 5000 -j REJECT >> /dev/null') == 0:
            os.system('iptables -D INPUT -p udp -s 10.0.0.12/32 --dport 5000 -j REJECT >> /dev/null')            
            
        # Rule is NOT present
        assert(os.system('iptables --check INPUT -p tcp --dport 5000 -s 10.0.0.12/32 -j REJECT >> /dev/null') != 0)
        assert(os.system('iptables --check INPUT -p udp --dport 5000 -s 10.0.0.12/32 -j REJECT >> /dev/null') != 0)

        firewall = FirewallHedge(TestBase.testDir + '/testrepoview')
        firewall.addInputRejectRule('10.0.0.12/32', 5000)

        assert(os.system('iptables --check INPUT -p tcp -s 10.0.0.12/32 --dport 5000 -j REJECT >> /dev/null') == 0)
        assert(os.system('iptables --check INPUT -p udp -s 10.0.0.12/32 --dport 5000 -j REJECT >> /dev/null') == 0)
        assert(os.path.isfile('/etc/cron.d/hedge-rules'))
        assert(os.path.isfile('/etc/iptables/hedge-rules.sh'))

        with open('/etc/cron.d/hedge-rules', 'r') as f:
            content = f.read()
            assert(content.find('@reboot /etc/iptables/hedge-rules.sh') == 0)        

    def testSimpleAcceptRule(self):
        # If the rule IS present remove it before the test
        if os.system('iptables --check INPUT -p all -s 10.0.0.11/32 -j ACCEPT >> /dev/null') == 0:
            os.system('iptables -D INPUT -p all -s 10.0.0.11/32 -j ACCEPT >> /dev/null')
            
        # Rule is NOT present
        assert(os.system('iptables --check INPUT -p all -s 10.0.0.11/32 -j ACCEPT >> /dev/null') != 0)

        firewall = FirewallHedge(TestBase.testDir + '/testrepoview')
        firewall.addInputAcceptRule('10.0.0.11/32')

        assert(os.system('iptables --check INPUT -p all -s 10.0.0.11/32 -j ACCEPT >> /dev/null') == 0)
        

if __name__ == '__main__':
    unittest.main()  
