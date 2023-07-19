
class AptHedge:

    def __init__(self, repoRootPath):
        self.repoRootPath = repoRootPath

    def ensurePackage(self, packageName):
        print(packageName)        

    def ensurePackages(self, packageNames):
            for packageName in packageNames:
                self.ensurePackage(packageName)
                