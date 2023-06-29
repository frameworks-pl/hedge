import subprocess
import logging
import shutil
import argparse


def cloneRepo(repoUrl, destinationPath):    
    """
    Clones repository from which agent should take artifcats and code to be executed

    Args:
        repoUrl (str): URL/path to git repository
        destinationPath: Location where agent should clone the repo
    Returns:
        bool: True if cloning was successful
    """
    try:
        subprocess.check_output(['git', 'clone', repoUrl, destinationPath])
        return True
    except Exception as e:
        logging.error("Failed to clone repo {repo} to {location}".format(repo=repoUrl, location=destinationPath))
    return False

def ensureFile(repoAbsolutePath, destinationPath):
    """
        Makes sure that file from the repo and destination path are the same
        Args:
            repoAbsolutePath (str): Path in the repository provided from the root directory of the repo
            destinationPath (str): Absolute path on the system where the file is to be placed
        Returns:
            bool: True if they are the same
    """

    #TODO: Before actually coping the file into location, check if file is there
    shutil.copy()

#TODO: In first approach we will give path to the repo as parameter
def main():

    parser = argparse.ArgumentParser(prog="Hedge Agent",
        description='Agent performing automated server configuration')
    parser.add_argument('-r', "--repository", type=str, help='URL of the repository with server configuration')
    args = parser.parse_args()


    repoURL = args.repository
    if not repoURL:
        print("Missing repository URL")
        exit(1)

    #Assuming that the workdir for the agent willbe ~/.hedge
    workDir = '~/.hedge'


    print('missing params')

    #TODO: load config, clone repo, execute target

main()
