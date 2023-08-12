import subprocess
import os
from basehedge import BaseHedge
from command import Command

class CommandHedge(BaseHedge):
    
    def __init__(self, repoRootPath):
        BaseHedge.__init__(self, repoRootPath)    

    def runCommand(self, command):  
        """
            Executes a command with all its parameters

            Command can be either string or array. If it is string, it will be split by space.            
            Args:
                command (array, str): command with all its parameters
            Returns:
                void
        """

        # Always run with sudo (second param)
        cmd = Command(command, True)    
        self.log.addPending(cmd.getAsString())
        
        if (cmd.hasRedirect()):
            result = os.system(cmd.getAsString())
        else:
            p = subprocess.Popen(cmd.getArray(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            result = p.communicate()

        if (result == 0):
            self.log.commitOK()
        else:
            self.log.commitFAIL()    