
# CPArchiver

**CPArchiver** is a Python-based tool that helps competitive programmers streamline the process of archiving their solutions to competitive programming problems. The script automates the process of pushing solutions to a GitHub repository, allowing users to easily store and organize their code across different platforms.

## Files

- **main.py**: The core script for CPArchiver. It manages the process of gathering solutions from local directories and prepares them for archival.
  
- **push_to_github.py**: Handles the automated process of pushing your solutions to a GitHub repository. It simplifies version control, ensuring that your solutions are always up-to-date on GitHub.

- **.gitignore**: Specifies files and directories to be excluded from version control.

## Installation

1. Clone this repository:
    \`\`\`bash
    git clone https://github.com/sifat-hossain-niloy/CPArchiver.git
    \`\`\`

2. Install the required dependencies (if any). Make sure you have Python installed:
    \`\`\`bash
    pip install -r requirements.txt
    \`\`\`

3. Set up your GitHub credentials for pushing the solutions:
    - Add your GitHub token or configure the script to use your SSH keys for authentication.

4. Run the script:
    \`\`\`bash
    python main.py
    \`\`\`

## Usage

- Ensure you have your solutions stored in a local directory.
- Modify `main.py` to specify the directory paths and filenames of your solutions.
- Run the script, and `push_to_github.py` will handle committing and pushing these files to your GitHub repository.

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

## Contributions

Feel free to fork this project, create new features, and submit pull requests. Contributions are welcome!
"""
