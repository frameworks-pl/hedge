import logging

#This is dummy class used only to test importing module dynamically from client repo
#It should not be imported anywhere statically!!!
class DummyHedge:

    def __init__(self, repoRootPath):
        self.repoRootPath = repoRootPath

    def testMethod(self):
        logging.info("You are now inside testMethod of DummyHedge")
