import logging
import shutil
import os
from basehedge import BaseHedge

class FileHedge(BaseHedge):

    def __init__(self, repoRootPath):
        BaseHedge.__init__(self, repoRootPath)

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

        shutil.copy(sourcePath, destinationPath)    
        self.log.commitOK() if os.path.isfile(destinationPath) else self.log.commitFAIL()