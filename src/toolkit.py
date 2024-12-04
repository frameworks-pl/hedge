import re
import subprocess
import shutil
import os
from datetime import datetime

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

   @staticmethod
   def backupFile(filePath, backupRootDir = None):
      """
         Creates backup copy of a file in the same location as the file (unless backupRootDir is specified), adds timestamp and 'hedge' to name
         Args:
               filePath (str): Absolute path to file which is to be backed up
               backupRootDir (str): Path to the directory, relative to which backup files will be created
         Returns:
               path to created backup file, False if backup failed
      """

      fileParts = os.path.splitext(os.path.basename(filePath))
      timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
      backupFileName = fileParts[0] +   '_' + timestamp + '_hedge' + fileParts[1]

      if backupRootDir != None:
         backupDir = backupRootDir + '/' + os.path.dirname(filePath)
         if not os.path.isdir(backupDir):
            os.makedirs(backupDir)        
         backupFilePath = backupDir + '/' +  backupFileName
      else:
         # Fallback - create in location where the source file is
         fileParts = os.path.splitext(filePath)
         backupFilePath = fileParts[0] +   '_' + timestamp + '_hedge' + fileParts[1]

      try: 
         result = shutil.copy(filePath,  backupFilePath)
         return result
      except Exception:
         pass

      return False

   @staticmethod
   def findFiles(filePath, pattern):
      """
         Finds all files that match provided pattern
         Args:
               filePath (str): Absolute path to directory where to look for file
               pattern (str): patter to be used when matching files
         Returns:
               bool: True if directory exists         
      """      
      files = [f for f in os.listdir(filePath) if os.path.isfile(os.path.join(filePath, f))]
      matching_files = []
      for f in files:
         if re.match(pattern, f):
            matching_files.append(f) 

      return matching_files
         
