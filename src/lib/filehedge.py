import logging
import shutil
import os, sys
from basehedge import BaseHedge
import paramiko
from scp import SCPClient

libFolder = os.path.realpath(os.getcwd() + '/..')
sys.path.insert(0, libFolder)
import toolkit

class FileHedge(BaseHedge):

    def __init__(self, repoRootPath):
        BaseHedge.__init__(self, repoRootPath)
        self.backupRootDir = os.path.expanduser("~") + '/.hedge/backup'       

    def ensureFile(self, absolutePathInRepo, destinationPath):
        """
            Makes sure that file from the repo and destination path are the same
            Args:
                repoAbsolutePath (str): Path in the repository provided from the root directory of the repo
                destinationPath (str): Absolute path on the system where the file is to be placed
            Returns:
                bool: True if they are the same
        """

        self.log.addPending("{source} -> {target}".format(source=absolutePathInRepo,target=destinationPath))

        #TODO: Before actually coping the file into location, check if file is there
        sourcePath = self.repoRootPath + absolutePathInRepo
        if not os.path.isfile(sourcePath):
            logging.error("{source} does not exist".format(source=sourcePath))
            self.log.commitFAIL()
            return False
        
        targetDir = os.path.dirname(destinationPath)
        logging.debug('Target dir is ' + targetDir)

        #COMMENT: python 3.x has params to specify permissions and wether to ignore if dir exists
        #but for Ubuntu 18 we only have python 2.x which does not have those params
        if not os.path.isdir(targetDir):
            os.makedirs(targetDir)

        #make backup of exiting file beofre copying new content
        if os.path.isfile(destinationPath):
            toolkit.Toolkit.backupFile(destinationPath)

        shutil.copy(sourcePath, destinationPath)    
        self.log.commitOK() if os.path.isfile(destinationPath) else self.log.commitFAIL()

    def ensureFileViaSsh(self, pathOnRemoteHost, destinationPath, user = None, host = None, keyPath = None, port = None):
        """
            Copies file from remote host to destination path
            Args:
                pathOnRemoteHost (str): Path on the remote host
                destinationPath (str): Absolute path on the system where the file is to be placed
                user (str): Username to use when connecting to remote host
                host (str): Hostname to use when connecting to remote host
                keyPath (str): Path to private key to use when connecting to remote host
            Returns:
                bool: True if they are the same
        """
        self.log.addPending("{source} -> {target}".format(source=pathOnRemoteHost,target=destinationPath))
        client = paramiko.SSHClient()
        paramiko.util.loglevel = logging.DEBUG
        paramiko.util.log_to_file('/tmp/paramiko.log')
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        cnn_params = {
            'hostname' : host,
            'username' : user,
        }
        if keyPath != None:
            cnn_params['pkey'] = paramiko.RSAKey(filename=keyPath)
        if port != None:
            cnn_params['port'] = port

        client.connect(**cnn_params)

        scp = SCPClient(client.get_transport())
        scp.get(pathOnRemoteHost, destinationPath)

        self.log.commitOK() if os.path.isfile(destinationPath) else self.log.commitFAIL()


    def ensureDir(self, destinationPath):
        """
            Makes sure that directory exists
            Args:
                destinationPath (str): Absolute path on the system where the directory is to be placed
            Returns:
                bool: True if directory exists
        """
        self.log.addPending("Ensuring dir {target}".format(target=destinationPath))

        if not os.path.isdir(destinationPath):
            os.makedirs(destinationPath)

        self.log.commitOK() if os.path.isdir(destinationPath) else self.log.commitFAIL()