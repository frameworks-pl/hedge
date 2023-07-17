
class AptHedge:

    def __init__(self, repoRootPath):
        self.repoRootPath = repoRootPath

    def ensurePackages(self, packageNames):
            for packageName in packageNames:
                ensurePackage(packageName
                
    def ensurePackage(self, packageName):
        print(packageName)