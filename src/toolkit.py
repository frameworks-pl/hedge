import re
import subprocess

class Toolkit:

   @staticmethod
   def extractRepoName(repoUrl):
         pattern = r'/([^/]+?)(?:\.git)?$'
         match = re.search(pattern, repoUrl)
         if match:
            return match.group(1)
         return None

   @staticmethod
   def getUserGroups(userName):
         groups = subprocess.check_output(["groups", userName]).rstrip()
         groups = groups.split(":")
         #we should have two groups, the first one is the user name, the second one is the list of groups
         if (len(groups) > 1):
            return groups[1].split(" ")

         raise Exception("Could not get groups for user '{user}'".format(user=userName))
