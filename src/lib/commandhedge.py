import subprocess
from basehedge import BaseHedge

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

        
        if (isinstance(command, str)):
            rawCmd = command.split(" ")
            self.log.addPending(command)
        else:
            # Assuming that command is already an array
            rawCmd = command

            cmd = " ".join(command)
            self.log.addPending(cmd)
        
        p = subprocess.Popen(rawCmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.communicate()

        if (p.returncode == 0):
            self.log.commitOK()
        else:
            self.log.commitFAIL()    