import os
from github import Github, GithubException

def get_or_create_repo(username, token, repo_name):
    # Authenticate to GitHub
    g = Github(username, token)
    
    try:
        # Try to get the repository
        repo = g.get_user().get_repo(repo_name)
        print(f"Repository {repo_name} already exists.")
    except GithubException as e:
        if e.status == 404:
            # Repository does not exist, create a new one
            repo = g.get_user().create_repo(repo_name)
            print(f"Repository {repo_name} created.")
        else:
            # Re-raise the exception if it's not a 404
            raise e
    
    return repo

def push_files_to_repo(repo, directory):
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                path_in_repo = os.path.relpath(file_path, directory)
                try:
                    # Check if the file already exists in the repo
                    repo.get_contents(path_in_repo)
                    print(f"File {file} already exists in the repository. Skipping.")
                except GithubException as e:
                    if e.status == 404:
                        # Create the file if it does not exist
                        repo.create_file(path_in_repo, f"Add {file}", content)
                        print(f"Added {file} to repository.")
                    else:
                        raise e

if __name__ == "__main__":
    github_username = input("Enter your GitHub username: ")
    github_token = input("Enter your GitHub access token: ")
    repo_name = input("Enter the name of the GitHub repository to create or push to: ")
    local_directory = input("Enter the local directory containing the files to push: ")
    
    repo = get_or_create_repo(github_username, github_token, repo_name)
    push_files_to_repo(repo, local_directory)
    
    print(f"Files from {local_directory} have been pushed to the GitHub repository {repo_name}.")
