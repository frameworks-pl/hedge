
import subprocess
from basehedge import BaseHedge

class AptHedge(BaseHedge):

    def __init__(self, repoRootPath):
        BaseHedge.__init__(self, repoRootPath)

    def ensurePackages(self, packageNames):
        """
            Installs specified packages using apt-get
            Args:
                packageNames (array): List of package names to be instaleed
            Returns:
                void
        """

        packageList = ",".join(packageNames)
        self.log.addPending("apt-get install -y {packets}".format(packets=packageList))
        
        p = subprocess.Popen(['sudo', 'apt-get', 'install', '-y', packageList], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.communicate()

        if (p.returncode == 0):
            self.log.commitOK()
        else:
            self.log.commitFAIL()

                