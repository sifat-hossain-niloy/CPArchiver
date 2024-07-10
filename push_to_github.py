import os
from github import Github, GithubException, InputGitAuthor
from datetime import datetime
import json

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
    with open(os.path.join(directory, 'submissions.json'), 'r', encoding='utf-8') as json_file:
        submissions_data = json.load(json_file)

    for submission_id, data in submissions_data.items():
        filename = data['path']
        file_path = os.path.join(directory, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            path_in_repo = filename
            commit_date = datetime.strptime(data['timestamp'], '%Y-%m-%d %H:%M:%S')

            author = InputGitAuthor(
                name='Md Sifat Hossain',
                email='sifatb910@gmail.com',
                date=commit_date.isoformat() + 'Z'
            )

            try:
                # Check if the file already exists in the repo
                repo.get_contents(path_in_repo)
                print(f"File {filename} already exists in the repository. Skipping.")
            except GithubException as e:
                if e.status == 404:
                    # Create the file if it does not exist
                    repo.create_file(
                        path_in_repo,
                        f"Add {data['problem_name']} solution submitted at {data['timestamp']}",
                        content,
                        committer=author,
                        author=author
                    )
                    print(f"Added {filename} to repository.")
                else:
                    raise e
