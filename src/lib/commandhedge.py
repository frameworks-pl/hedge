import subprocess
import os
from basehedge import BaseHedge
from command import Command
import uuid
import paramiko
import logging

class CommandHedge(BaseHedge):
    
    def __init__(self, repoRootPath, verbose = False, sudo = True, collectOutput = False):
        BaseHedge.__init__(self, repoRootPath)    
        self.verbose = verbose
        self.sudo = sudo
        self.collectOutput = collectOutput

    def runCommand(self, command, user = None, host = None, keyPath = None):  
        """
            Executes a command with all its parameters

            Command can be either string or array. If it is string, it will be split by space.            
            Args:
                command (array, str): command with all its parameters
            Returns:
                void
        """

        cmd = Command(command, self.sudo)

        #If we are collecting output, we need to redirect it to a temporary file
        #but only if not running remotely
        if self.collectOutput and (user == None and host == None):
            self.tmpOutputPath = "/tmp/hedge_output_" + str(uuid.uuid4())
            cmd.add(" | tee " + self.tmpOutputPath)

        self.log.addPending(cmd.getAsString())

        if user != None and host != None:
            client = paramiko.SSHClient()
            paramiko.util.loglevel = logging.DEBUG
            paramiko.util.log_to_file('/tmp/paramiko.log')
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            private_key = None
            if keyPath != None:
                private_key = paramiko.RSAKey(filename=keyPath)
            if private_key != None:
                client.connect(host, username=user, pkey=private_key)
            else:
                client.connect(host, username=user)
            stdin,stdout,stderr = client.exec_command(cmd.getAsString())
            if self.collectOutput:
                self.lastCommandOutput = stdout.read()
            result = stdout.channel.recv_exit_status()
        elif cmd.hasRedirect() or cmd.hasInnerCommand() or cmd.isAndCommand():
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