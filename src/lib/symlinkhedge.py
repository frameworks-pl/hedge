import unittest
import os, sys

class SymlinkHedge(object):

    def ensureSymlink(self, realFilePath, symlinkPath):
        """
            Makes sure that specified symlink exists
            Args:                
                realFilePath (str): Path to the actual file
                symlinkPath (str): Path to of the symlink to be created
            Returns:
                bool: True if symlink exists and points to the specified file
        """

        #if symlink exists and points to something else than we want, remove it
        if (os.path.islink(symlinkPath)):
            os.remove(symlinkPath)

        os.symlink(realFilePath, symlinkPath)
        return os.path.islink(symlinkPath) and os.readlink(symlinkPath) == realFilePath

    def removeSymlink(self, symlinkPath):
        """
            Removes specified symlink
            Args:                
                symlinkPath (str): Path to of the symlink to be removed
            Returns:
                bool: True if symlink (file) no longer exists
        """
        if (os.path.islink(symlinkPath)):
            os.remove(symlinkPath)
        return not os.path.isfile(symlinkPath)
