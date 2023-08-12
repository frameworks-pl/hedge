
import subprocess
from basehedge import BaseHedge
from command import Command

class AptHedge(BaseHedge):

    def __init__(self, repoRootPath, verbose = False):
        BaseHedge.__init__(self, repoRootPath)
        self.verbose = verbose

    def ensurePackages(self, packageNames):
        """
            Installs specified packages using apt-get
            Args:
                packageNames (array): List of package names to be instaleed
            Returns:
                void
        """

        cmd = Command(['apt-get', 'install', '-y'], True)
        cmd.add(packageNames)
        self.log.addPending(cmd.getAsString())
        
        p = subprocess.Popen(cmd.getArray(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        if self.verbose:
            print(stdout)
            print(stderr)

        if (p.returncode == 0):
            self.log.commitOK()
        else:
            self.log.commitFAIL()

                