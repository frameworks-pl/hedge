import subprocess

def cloneCepository(repo_url, destinantion_path):
    try:
        subprocess.check_output(['git', 'clone', repo_url, destinantion_path])
        print("Repository cloned successfully")
    except:
        print("Error cloning repository:", e)