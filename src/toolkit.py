import re

class Toolkit:

    @staticmethod
    def extractRepoName(repoUrl):
         pattern = r'/([^/]+?)(?:\.git)?$'
         match = re.search(pattern, repoUrl)
         if match:
            return match.group(1)
         return None
