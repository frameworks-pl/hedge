import sys
class Hedge:

    def __init__(self, repoRootPath):
        self.repoRootPath = repoRootPath

    def target1(self, agent, params):
        pass

    def notATargetBecauseToFewParams(self, abc):
        pass

    def notATargetBecauseWrongNameOfParams(self, notAgentParam, NotParamsParam):
        self

    def target2(self, agent, params):
        pass