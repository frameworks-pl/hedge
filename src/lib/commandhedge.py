import subprocess
import os
from basehedge import BaseHedge
from command import Command

class CommandHedge(BaseHedge):
    
    def __init__(self, repoRootPath, verbose = False, sudo = True):
        BaseHedge.__init__(self, repoRootPath)    
        self.verbose = verbose
        self.sudo = sudo

    def runCommand(self, command):  
        """
            Executes a command with all its parameters

            Command can be either string or array. If it is string, it will be split by space.            
            Args:
                command (array, str): command with all its parameters
            Returns:
                void
        """

        cmd = Command(command, self.sudo)    
        self.log.addPending(cmd.getAsString())
        
        if cmd.hasRedirect() or cmd.hasInnerCommand() or cmd.isAndCommand():
            result = os.system(cmd.getAsString())
        else:
            p = subprocess.Popen(cmd.getArray(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = p.communicate()
            if self.verbose:
                print(stdout)
                print(stderr)
            result = p.returncode

        if result == 0:
            self.log.commitOK()
        else:
            self.log.commitFAIL()    