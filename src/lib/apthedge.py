
import subprocess

class AptHedge:

    def __init__(self, repoRootPath):
        self.repoRootPath = repoRootPath

    def ensurePackages(self, packageNames):
        """
            Installs specified packages using apt-get
            Args:
                packageNames (array): List of package names to be instaleed
            Returns:
                void
        """

        packageList = ",".join(packageNames)
        
        p = subprocess.Popen(['apt-get', 'install', '-y', packageList], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.communicate()

                