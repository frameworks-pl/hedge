import subprocess
import logging
import shutil
import argparse
import os
import toolkit


class Agent:

    def __init__(self, repoUrl, destinationPath = None):
        self.repoUrl = repoUrl
        self.destinationPath = destinationPath
        if not self.destinationPath:
            self.destinationPath = os.path.expanduser("~") + '/.hedge/' + toolkit.Toolkit.extractRepoName(repoUrl)

    def cloneRepo(self):    
        """
        Clones repository from which agent should take artifcats and code to be executed

        Args:
            repoUrl (str): URL/path to git repository
            destinationPath: Location where agent should clone the repo
        Returns:
            bool: True if cloning was successful
        """
        try:
            subprocess.check_output(['git', 'clone', self.repoUrl, self.destinationPath])
            return True
        except Exception as e:
            logging.error("Failed to clone repo {repo} to {location}".format(repo=self.repoUrl, location=destinationPath))
        return False

    def ensureFile(self, repoAbsolutePath, destinationPath):
        """
            Makes sure that file from the repo and destination path are the same
            Args:
                repoAbsolutePath (str): Path in the repository provided from the root directory of the repo
                destinationPath (str): Absolute path on the system where the file is to be placed
            Returns:
                bool: True if they are the same
        """

        #TODO: Before actually coping the file into location, check if file is there
        sourcePath = self.destinationPath + repoAbsolutePath
        if not os.path.isfile(sourcePath):
            logging.error("{source} does not exist".format(source=sourcePath))
            return False

        shutil.copy(sourcePath, destinationPath)

#TODO: In first approach we will give path to the repo as parameter
def main():

    agent = Agent()

    parser = argparse.ArgumentParser(prog="Hedge Agent",
        description='Agent performing automated server configuration')
    parser.add_argument('-r', "--repository", type=str, help='URL of the repository with server configuration')
    parser.add_argument('-w', "--workdir", type=str, help='Location of work directory', default='./~hedge')
    args = parser.parse_args()


    repoURL = args.repository
    agent.workDir = args.workdir

    if not repoURL:
        logging.error("Missing repository URL")
        return 1


    if not agent.cloneRepo(workDir):
        logging.error("Failed to clone repo")
        return 1
    

    #TODO: load config, clone repo, execute target


if __name__ == '__main__':
    exitCode = main()
    exit(exitCode)

