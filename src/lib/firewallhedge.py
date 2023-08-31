import logging
import shutil
import os
from basehedge import BaseHedge

class FirewallHedge(object):
    
    def addInputRejectionRule(self, ip, port = None, protocol = "all"):
        """
            Adds a rule to reject all incoming traffic from specified IP address
            
            Args:
                ip (str): IP address
                port (int): Port number
            Returns:
                void
        """
        self._addRule('INPUT', 'REJECT', ip, port, protocol)

    def _addRule(self, chain, action, ip, port, protocol):
        """
            Adds a rule to specified chain
            
            Args:
                chain (str): Chain name
                ip (str): IP address
                port (int): Port number
                protocol (str): Protocol name
            Returns:
                Boolean: True if rule was added, False otherwise
        """

        cmd = "iptables -A {chain}".format(chain=chain)
        if (protocol != None):
            cmd += " -p {protocol}".format(protocol=protocol)

        cmd += " -s {ip}".format(ip=ip)

        if (port != None):
            cmd += " --dport {port}".format(port=str(port))

        cmd += " -j {action}".format(action=action)
        print(cmd)
        return os.system(cmd) == 0
      