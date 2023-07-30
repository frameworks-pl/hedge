from log import Log

class BaseHedge(object):

    def __init__(self, repoRootPath):
        self.repoRootPath = repoRootPath
        self.log = Log()