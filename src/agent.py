import subprocess

def cloneRepo(repo_url, destinantion_path):    
    try:
        subprocess.check_output(['git', 'clone', repo_url, destinantion_path])
        print("Repository cloned successfully")
    except Exception as e:
        print("Error cloning repository:", e)