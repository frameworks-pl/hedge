import subprocess
import logging
import argparse
import os
import toolkit
import sys
import importlib
import inspect
from datetime import datetime
srcFolder = os.path.realpath(os.getcwd())
sys.path.insert(0, srcFolder)
libFolder = os.path.realpath(os.getcwd() + '/lib')
sys.path.insert(0, libFolder)
from command import Command
from symlinkhedge import SymlinkHedge
from apthedge import AptHedge
from commandhedge import CommandHedge
from filehedge import FileHedge
from grouphedge import GroupHedge
from userhedge import UserHedge


class Agent:

    TEMP_DIR = "tmp"

    def __init__(self, repoUrl, repoDestinationPath = None, repoPort = None, verbose = False, sshOptions = ""):
        """
        Args:
            repoUrl (str): URL/path to git repository
            repoDestinationPath: Location where agent should clone the repo
            repoPort: (int): Port of git repository        
        """
        self.repoUrl = repoUrl
        self.repoPort = repoPort
        self.verbose = verbose
        self.sshOptions = sshOptions
        self.lastHedgeObject = None
                
        self.fileBackupPath = os.path.expanduser("~") + '/.hedge/backup/'  + toolkit.Toolkit.extractRepoName(self.repoUrl) + '/' + datetime.now().strftime('%Y%m%d')
        if not repoDestinationPath:
            self.repoDestinationPath = os.path.expanduser("~") + '/.hedge/' + toolkit.Toolkit.extractRepoName(self.repoUrl)
        else:
            self.repoDestinationPath = repoDestinationPath.replace("~", os.path.expanduser("~"))


    def cloneRepo(self, branchName = None):    
        """
        Clones repository from which agent should take artifcats and code to be executed
        Returns:
            bool: True if cloning was successful
        """        

        try:
            if not os.path.isdir(self.repoDestinationPath):
                command = Command(['git', 'clone'])
                sshCommand = Command([])

                if branchName:
                    command.add(['--branch', branchName])

                if self.repoPort != None:
                    sshCommand.add(['-p', self.repoPort])
                if self.sshOptions != "":
                    sshCommand.add([self.sshOptions])
                
                if sshCommand.commandItems.__len__() > 0:
                    command.add(['--config', "core.sshCommand=\"ssh {sshcmd}\""
                    .format(sshcmd=sshCommand.getAsString())])

                command.add([self.repoUrl, self.repoDestinationPath])
                os.system(command.getAsString())
            else:
                if branchName:
                    command = Command(['git', 'fetch'])
                    subprocess.check_output(command.getArray(), cwd=self.repoDestinationPath)

                    command = Command(['git', 'checkout', branchName])
                    subprocess.check_output(command.getArray(), cwd=self.repoDestinationPath)

                #We already cloned that repo, so second call should just run update
                command = Command(['git', 'pull'])
                subprocess.check_output(command.getArray(), cwd=self.repoDestinationPath)

            self.createTmpFolder()

            return True
        except Exception as e:
            logging.error("Failed to clone repo {repo} to {location}".format(repo=self.repoUrl, location=self.repoDestinationPath))
        return False

    def createTmpFolder(self):
        """
        Creates temporary folder in target the repo folder
        You may want to add that folder to ignored files in your repo
        """
        if (not os.path.isdir(self.repoDestinationPath + '/' + self.TEMP_DIR)):
            os.makedirs(self.repoDestinationPath + '/' + self.TEMP_DIR)

        return os.path.isdir(self.repoDestinationPath + '/' + self.TEMP_DIR)

    def getTempPath(self):
        """
        Returns path to temporary folder in target the repo folder
        Use this method to obtain path to temporary folder rather than using hardcoded paths
        """
        return self.repoDestinationPath + '/' + self.TEMP_DIR
    
    def instantiateHedge(self, module):
        masterFile = self.repoDestinationPath + '/hedge.py'
        if not os.path.isfile(masterFile):
            logging.error("Master file ({masterFile}) could not be found.".format(masterFile=masterFile))
            return False

        # Adding path from which we want import the master class
        sys.path.insert(0, self.repoDestinationPath)

        # Loads master file, create instance of Hedge class and run target
        logging.debug("repo:" + self.repoDestinationPath)
        hedge_module = importlib.import_module(module)
        hedge_class = getattr(hedge_module, 'Hedge')
        return hedge_class(self.repoDestinationPath)


    def execute(self, target = 'build', params = {}, module = 'hedge'):
        hedgeInstance = self.instantiateHedge(module)

        # Executs specified target
        targetMethod = getattr(hedgeInstance, target)

        # 'self' here is passing instance of Agent to the target method!
        targetMethod(self, params)


    def ensureFile(self, absolutePathInRepo, destinationPath):
        """
        See lib/filehedge.py ensureFile for details
        """
        filehedge = FileHedge(self.repoDestinationPath, self.fileBackupPath)
        return filehedge.ensureFile(absolutePathInRepo, destinationPath)

    def ensureFileViaSsh(self, pathOnRemoteHost, destinationPath, user = None, host = None, keyPath = None, port = None):
        """
        See lib/filehedge.py ensureFileFromRemote for details
        """
        filehedge = FileHedge(self.repoDestinationPath)
        return filehedge.ensureFileViaSsh(pathOnRemoteHost, destinationPath, user, host, keyPath, port)

    def ensureDir(self, destinationPath, user = None, group = None, permissions = None):
        """
        See lib/filehedge.py ensureDir for details
        """
        filehedge = FileHedge(self.repoDestinationPath)
        return filehedge.ensureDir(destinationPath, user, group, permissions)

    def ensureSymlink(self, realFilePath, symlinkPath):

        """
        See lib/symlinkhedge.py ensureSymlink for detail
        """
        symlinkhedge = SymlinkHedge()
        return symlinkhedge.ensureSymlink(realFilePath, symlinkPath) 

    def ensurePackages(self, packageList):
        """
        See lib/apthedge.py ensurePackages for details
        """
        aptHedge = AptHedge(self.repoDestinationPath)
        return aptHedge.ensurePackages(packageList)        

    def runCommand(self, command, sudo = True, collectOutput = False, user = None, host = None, keyPath = None, port = None):
        """
        See lib/commandhedge.py runCommand for details
        """
        self.lastHedgeObject = CommandHedge(self.repoDestinationPath, False, sudo, collectOutput)
        result = self.lastHedgeObject.runCommand(command, user, host, keyPath, port)
        if collectOutput == True:
            if isinstance(self.lastHedgeObject.lastCommandOutput, bytes):
                self.lastCommandOutput = self.lastHedgeObject.lastCommandOutput.decode('utf-8')
            else:
                self.lastCommandOutput = self.lastHedgeObject.lastCommandOutput


    def ensureGroup(self, groupName):
        """
        See lib/grouphedge.py ensureGroup for details
        """
        grouphedge = GroupHedge(self.repoDestinationPath)
        return grouphedge.ensureGroup(groupName)

    def ensureUserBelongsToGroup(self, userName, groupName):
        """
        See lib/useredge.py ensureUserBelongsToGroup for details
        """
        userhedge = UserHedge(self.repoDestinationPath)
        return userhedge.ensureUserBelongsToGroup(userName, groupName)
    
    def listTargets(self, hedge_obj):
        methods = {}
        for name, func in inspect.getmembers(hedge_obj.__class__, inspect.isfunction):
            if not name.startswith("_"):
                params = list(inspect.signature(func).parameters.keys())
                if len(params) == 3 and params[0] == 'self' and params[1] == 'agent' and params[2] == 'params':
                    methods[name]= {'parameters' :params}
        return methods


#TODO: In first approach we will give path to the repo as parameter
def main():

    parser = argparse.ArgumentParser(prog="Hedge Agent",
        description='Agent performing automated server configuration')
    parser.add_argument('-r', "--repository", type=str, help='URL of the repository with server configuration')
    parser.add_argument('-b', "--branch", type=str, help="Branch for the repository", default=None)
    parser.add_argument('-m', "--module", type=str, help='Execute target from the provided module rather than from default one (hedge)', default='hedge')
    parser.add_argument('-p', "--port", type=str, help='Port of the repository with server configuration', default=None)
    parser.add_argument('-w', "--workdir", type=str, help='Location of work directory', default=None)
    parser.add_argument('-t', "--target", type=str, help='Target to execute', default='build')
    parser.add_argument('-lt', "--list-targets", help="List available arguments", nargs='?', const=True, default=None)
    parser.add_argument('-s', "--skip", type=bool, help='Skip cloning repository', default=False)
    parser.add_argument('-v', "--verbose", type=bool, help='Verbose mode', default=False)
    parser.add_argument('-o', "--sshoptions", type=str, help='SSH options', default="")
    
    args = parser.parse_args()

    repoURL = args.repository
    workDIR = args.workdir
    target = args.target
    agent = Agent(repoURL, workDIR, args.port, False, args.sshoptions)
    module = 'hedge'

    if not repoURL:
        logging.error("Missing repository URL")
        return 1

    if not args.skip:
        if not agent.cloneRepo(args.branch):
            logging.error("Failed to clone repo")
            return 1

    if args.module:
        module = args.module

    if args.list_targets:
        print("\nList of available targets (if you do not see one you are looking for, check if signature is correct):")
        targets = agent.listTargets(agent.instantiateHedge(module))
        for key in targets:
            print(key) 
        return 0

    #TODO: load config, clone repo, execute target
    agent.execute(target, {}, module)


if __name__ == '__main__':
    exitCode = main()
    exit(exitCode)

