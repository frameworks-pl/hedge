import unittest
import os, sys
from basehedge import BaseHedge

class SymlinkHedge(BaseHedge):

    def __init__(self, repoRootPath):
        BaseHedge.__init__(self, repoRootPath)

    def ensureSymlink(self, realFilePath, symlinkPath):
        """
            Makes sure that specified symlink exists
            Args:                
                realFilePath (str): Path to the actual file
                symlinkPath (str): Path to of the symlink to be created
            Returns:
                bool: True if symlink exists and points to the specified file
        """
        os.symlink(realFilePath, symlinkPath)
        return os.path.islink(symlinkPath) and os.readlink(symlinkPath) == realFilePath
