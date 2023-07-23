import subprocess
import logging
import argparse
import os
import toolkit
import sys
import importlib
srcFolder = os.path.realpath(os.getcwd() + '/src')
sys.path.insert(0, srcFolder)
libFolder = os.path.realpath(os.getcwd() + '/src/lib')
sys.path.insert(0, libFolder)


class Agent:

    def __init__(self, repoUrl, repoDestinationPath = None):
        self.repoUrl = repoUrl
                
        if not repoDestinationPath:
            self.repoDestinationPath = os.path.expanduser("~") + '/.hedge/' + toolkit.Toolkit.extractRepoName(repoUrl)
        else:
            self.repoDestinationPath = repoDestinationPath.replace("~", os.path.expanduser("~"))

    def cloneRepo(self):    
        """
        Clones repository from which agent should take artifcats and code to be executed

        Args:
            repoUrl (str): URL/path to git repository
            repoDestinationPath: Location where agent should clone the repo
        Returns:
            bool: True if cloning was successful
        """

        try:
            if not os.path.isdir(self.repoDestinationPath):
                subprocess.check_output(['git', 'clone', self.repoUrl, self.repoDestinationPath])
            else:
                subprocess.check_output(['git', 'pull'], cwd=self.repoDestinationPath)
            return True
        except Exception as e:
            logging.error("Failed to clone repo {repo} to {location}".format(repo=self.repoUrl, location=repoDestinationPath))
        return False

    def execute(self, target = 'build', params = {}):
        masterFile = self.repoDestinationPath + '/hedge.py'
        if not os.path.isfile(masterFile):
            logging.error("Master file ({masterFile}) could not be found.".format(masterFile=masterFile))
            return False

        #Adding path from which we want import the master class
        sys.path.insert(0, self.repoDestinationPath)

        #loads master file, create instance of Hedge class and run target
        logging.debug("repo:" + self.repoDestinationPath)
        hedge_module = importlib.import_module('hedge')
        hedge_class = getattr(hedge_module, 'Hedge')
        hedgeInstance = hedge_class(self.repoDestinationPath)

        #executs specified target
        targetMethod = getattr(hedgeInstance, target)        
        targetMethod(params)





#TODO: In first approach we will give path to the repo as parameter
def main():

    parser = argparse.ArgumentParser(prog="Hedge Agent",
        description='Agent performing automated server configuration')
    parser.add_argument('-r', "--repository", type=str, help='URL of the repository with server configuration')
    parser.add_argument('-w', "--workdir", type=str, help='Location of work directory', default='~/.hedge')
    parser.add_argument('-t', "--target", type=str, help='Target to execute', default='build')
    args = parser.parse_args()

    repoURL = args.repository
    workDIR = args.workdir
    target = args.target
    agent = Agent(repoURL, workDIR)

    if not repoURL:
        logging.error("Missing repository URL")
        return 1


    if not agent.cloneRepo():
        logging.error("Failed to clone repo")
        return 1
    

    #TODO: load config, clone repo, execute target
    agent.execute(target)


if __name__ == '__main__':
    exitCode = main()
    exit(exitCode)

