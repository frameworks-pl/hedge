import os
import grp
from basehedge import BaseHedge

class GroupHedge(BaseHedge):

    def __init__(self, repoRootPath):
        BaseHedge.__init__(self, repoRootPath)

    def ensureGroup(self, groupName):
        """
            Makes sure that group exists
            Args:
                groupName (str): Name of the group
            Returns:
                bool: True if group exists
        """

        self.log.addPending("Making sure '{group}' exists".format(group=groupName))

        try:
            grp.getgrnam(groupName)
            self.log.commitOK()
            return True
        except KeyError:
            #getgrnam throws KeyError if group does not exist (which is fine)
            pass

        os.system('sudo groupadd ' + groupName)
        try:
            grp.getgrnam(groupName)
            self.log.commitOK()
            return True
        except KeyError:
            #getgrnam throws KeyError if group does not exist (which is fine)
            pass

        self.log.commitFAIL()
        return False    