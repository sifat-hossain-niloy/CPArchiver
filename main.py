import requests
import os
import re
from html import unescape
from datetime import datetime

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
                accepted_solutions.append((submission['id'], filename, submission['contestId'], submission_time, submission['creationTimeSeconds']))
    else:
        print(f"Error fetching data: {response['comment']}")
    
    return accepted_solutions

def save_solutions_to_disk(solutions, handle):
    if not os.path.exists(handle):
        os.makedirs(handle)
    
    for submission_id, filename, contest_id, submission_time, submission_timestamp in solutions:
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

if __name__ == "__main__":
    cf_handle = input("Enter your Codeforces handle: ")
    
    solutions = fetch_codeforces_solutions(cf_handle)
    save_solutions_to_disk(solutions, cf_handle)
    
    print(f"Solutions from {cf_handle} have been saved to the local disk.")
