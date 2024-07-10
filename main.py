import requests
import os
import re
from html import unescape
from datetime import datetime
import json
from push_to_github import get_or_create_repo, push_files_to_repo

def fetch_codeforces_solutions(handle):
    url = f'https://codeforces.com/api/user.status?handle={handle}'
    response = requests.get(url).json()
    accepted_solutions = []

    if response['status'] == 'OK':
        for submission in response['result']:
            if submission['verdict'] == 'OK':
                problem_name = submission['problem']['name']
                programming_language = submission['programmingLanguage'].lower()
                
                # Handle different variations of programming language names
                if 'c++' in programming_language:
                    extension = '.cpp'
                elif 'python' in programming_language:
                    extension = '.py'
                elif 'java' in programming_language:
                    extension = '.java'
                elif 'kotlin' in programming_language:
                    extension = '.kt'
                elif 'ruby' in programming_language:
                    extension = '.rb'
                elif 'perl' in programming_language:
                    extension = '.pl'
                elif 'haskell' in programming_language:
                    extension = '.hs'
                elif 'clojure' in programming_language:
                    extension = '.clj'
                elif 'scala' in programming_language:
                    extension = '.scala'
                elif 'rust' in programming_language:
                    extension = '.rs'
                elif 'php' in programming_language:
                    extension = '.php'
                elif 'go' in programming_language:
                    extension = '.go'
                elif 'd' in programming_language:
                    extension = '.d'
                elif 'ocaml' in programming_language:
                    extension = '.ml'
                elif 'pascal' in programming_language:
                    extension = '.pas'
                elif 'swift' in programming_language:
                    extension = '.swift'
                elif 'javascript' in programming_language:
                    extension = '.js'
                elif 'c#' in programming_language:
                    extension = '.cs'
                elif 'vb.net' in programming_language:
                    extension = '.vb'
                elif 'f#' in programming_language:
                    extension = '.fs'
                elif 'lua' in programming_language:
                    extension = '.lua'
                elif 'gcc' in programming_language or 'gnu' in programming_language:
                    extension = '.c'
                else:
                    extension = '.txt'

                sanitized_problem_name = re.sub(r'[\\/*?:"<>|]', "", problem_name)
                filename = f"{sanitized_problem_name.replace(' ', '_')}{extension}"
                submission_time = datetime.utcfromtimestamp(submission['creationTimeSeconds']).strftime('%Y-%m-%d %H:%M:%S')
                accepted_solutions.append({
                    'submission_id': submission['id'],
                    'filename': filename,
                    'contest_id': submission['contestId'],
                    'submission_time': submission_time,
                    'submission_timestamp': submission['creationTimeSeconds'],
                    'problem_name': problem_name,
                    'problem_url': f"https://codeforces.com/contest/{submission['contestId']}/problem/{submission['problem']['index']}",
                    'submission_url': f"https://codeforces.com/contest/{submission['contestId']}/submission/{submission['id']}",
                    'tags': submission['problem'].get('tags', []),
                    'language': submission['programmingLanguage'],
                    'platform': 'Codeforces',
                    'problem_index': submission['problem']['index']
                })
    else:
        print(f"Error fetching data: {response['comment']}")
    
    return accepted_solutions

def save_solutions_to_disk(solutions, handle):
    if not os.path.exists(handle):
        os.makedirs(handle)

    submissions_data = {}
    
    for solution in solutions:
        submission_id = solution['submission_id']
        filename = solution['filename']
        submission_time = solution['submission_time']
        submission_timestamp = solution['submission_timestamp']
        problem_name = solution['problem_name']
        problem_url = solution['problem_url']
        submission_url = solution['submission_url']
        tags = solution['tags']
        language = solution['language']
        platform = solution['platform']
        problem_index = solution['problem_index']
        contest_id = solution['contest_id']

        solution_url = f'https://codeforces.com/contest/{contest_id}/submission/{submission_id}'
        solution_page = requests.get(solution_url).text
        solution_start = solution_page.find('<pre id="program-source-text" class="prettyprint') + len('<pre id="program-source-text" class="prettyprint')
        solution_start = solution_page.find('>', solution_start) + 1
        solution_end = solution_page.find('</pre>', solution_start)
        solution_code = solution_page[solution_start:solution_end]
        
        # Decode HTML entities
        solution_code = unescape(solution_code).replace('<br>', '\n')
        
        file_path = os.path.join(handle, filename)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(solution_code)
            print(f"Saved {filename} submitted at {submission_time}")
        
        # Update the file's modification time to match the submission time
        os.utime(file_path, (submission_timestamp, submission_timestamp))

        # Prepare data for submissions.json
        submissions_data[submission_id] = {
            'contest_id': contest_id,
            'language': language,
            'path': file_path,
            'platform': platform,
            'problem_index': problem_index,
            'problem_name': problem_name,
            'problem_url': problem_url,
            'submission_id': submission_id,
            'submission_url': submission_url,
            'tags': tags,
            'timestamp': submission_time
        }
    
    # Save submissions data to submissions.json
    with open(os.path.join(handle, 'submissions.json'), 'w', encoding='utf-8') as json_file:
        json.dump(submissions_data, json_file, indent=4)
        print(f"Saved submissions metadata to submissions.json")

if __name__ == "__main__":
    cf_handle = input("Enter your Codeforces handle: ")
    
    solutions = fetch_codeforces_solutions(cf_handle)
    save_solutions_to_disk(solutions, cf_handle)
    
    github_username = input("Enter your GitHub username: ")
    github_token = input("Enter your GitHub access token: ")
    repo_name = input("Enter the name of the GitHub repository to create or push to: ")
    
    repo = get_or_create_repo(github_username, github_token, repo_name)
    push_files_to_repo(repo, cf_handle)
    
    print(f"Solutions from {cf_handle} have been saved to the local disk and pushed to the GitHub repository {repo_name}.")
