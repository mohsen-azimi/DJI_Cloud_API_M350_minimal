import subprocess

def git_add_commit_push():
    # Configure Git to avoid CRLF/LF warnings (this part remains unchanged)
    subprocess.run(["git", "config", "--local", "core.autocrlf", "false"])

    # Stage only changes to already tracked files (ignoring files in .gitignore)
    subprocess.run(["git", "add", "-u"])  # Use 'git add -u' to only add modified and deleted tracked files

    # Commit the changes
    subprocess.run(["git", "commit", "-m", "minimal_working_example"])

    # Push the changes to the remote repository (force push)
    subprocess.run(["git", "push", '-f'])

if __name__ == '__main__':
    git_add_commit_push()
