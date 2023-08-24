import os
import grp
from basehedge import BaseHedge
from toolkit import Toolkit

class UserHedge(BaseHedge):

    def __init__(self, repoRootPath):
        BaseHedge.__init__(self, repoRootPath)

    def ensureUserBelongsToGroup(self, userName, groupName):
        
        self.log.addPending("Adding user '{user}' to group '{group}'".format(user=userName, group=groupName))
        groups = Toolkit.getUserGroups(userName)
        if not groupName in groups:            
            result = os.system("sudo gpasswd --add {user} {group}".format(user=userName, group=groupName))
            if result == 0:
                self.log.commitOK()
            else:
                self.log.commitFAIL()

            return result == 0
            


