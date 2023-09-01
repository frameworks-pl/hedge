import os
from basehedge import BaseHedge

class FirewallHedge(BaseHedge):

    def __init__(self, repoRootPath):
        BaseHedge.__init__(self, repoRootPath)    

    def __del__(self):              

        BaseHedge.__del__(self)
    
    def addInputRejectRule(self, ip, port = None, protocol = "all"):
        """
            Adds a rule to reject all incoming traffic from specified IP address
            
            Args:
                ip (str): IP address
                port (int): Port number
            Returns:
                void
        """
        return self._addRule('INPUT', 'REJECT', ip, port, protocol)


    def addInputAcceptRule(self, ip, port = None, protocol = "all"):
        """
            Adds a rule to accept all incoming traffic from specified IP address
            
            Args:
                ip (str): IP address
                port (int): Port number
            Returns:
                void
        """
        return self._addRule('INPUT', 'ACCEPT', ip, port, protocol)
        

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
        self.log.addPending(cmd)
        result = os.system(cmd)

        #create cronjob that will restore iptables rules on reboot
        self._persist(cmd)

        if (result != 0):
            self.log.commitFAIL()
        else:
            self.log.commitOK()

        return result == 0

    def _persist(self, cmd):
        """
            Persists the changes to the firewall
        """
        if (not os.path.isdir('/etc/iptables')):
            os.system('mkdir /etc/iptables')            

        #There is a problem with dumping ALL and then loading ALL rules on docker container
        #To cicumvent this, we dump only INPUT rules for now
        os.system('echo "#!/bin/bash" > /etc/iptables/hedge-rules.sh')

        #TODO: Possibly we should add to the script check if rule exists before adding it (to prevent duplicates)
        os.system('echo "{cmd}"  >> /etc/iptables/hedge-rules.sh'.format(cmd=cmd))
        os.system('chmod +x /etc/iptables/hedge-rules.sh')

        # cron job that will load rules after reboot
        os.system('echo "@reboot /etc/iptables/hedge-rules.sh" > /etc/cron.d/hedge-rules')
      