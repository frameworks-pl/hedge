import subprocess
import os
from basehedge import BaseHedge
from command import Command
import uuid

class CommandHedge(BaseHedge):
    
    def __init__(self, repoRootPath, verbose = False, sudo = True, collectOutput = False):
        BaseHedge.__init__(self, repoRootPath)    
        self.verbose = verbose
        self.sudo = sudo
        self.collectOutput = collectOutput

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

        if self.collectOutput:
            self.tmpOutputPath = "/tmp/hedge_output_" + str(uuid.uuid4())
            cmd.add(" | tee " + self.tmpOutputPath)

        self.log.addPending(cmd.getAsString())
        
        if cmd.hasRedirect() or cmd.hasInnerCommand() or cmd.isAndCommand():
            result = os.system(cmd.getAsString())
            if self.collectOutput:
                with open(self.tmpOutputPath, "r") as f:
                    self.lastCommandOutput = f.read()
                os.remove(self.tmpOutputPath)
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