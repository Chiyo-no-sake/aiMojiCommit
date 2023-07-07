import os
import subprocess
from pick import pick
import yaml
import urllib.request
from pathlib import Path
from generate_commit_msg import generate_commit_message
import injector

CONFIG_FILE_PATH = os.path.expanduser("~/.aimojicommit/config.yaml")
REMOTE_DEFAULT_CONFIG_FILE_PATH = "https://raw.githubusercontent.com/Chiyo-no-sake/aiMojiCommit/main/config.yaml"

def check_dependencies():
    # Check git
    subprocess.call(["git", "--version"])
    # Check if pick is installed
    try:
        import pick
    except ImportError:
        print("Error: 'pick' is not installed.")
        print("Installing 'pick'...")
        subprocess.call(["pip", "install", "pick"])

def check_git_status():
    result = subprocess.run(['git', 'diff', '--cached', '--quiet'])
    if result.returncode != 0:
        print("No changes added to commit. Use 'git add' to track changes.")
        exit(1)

def create_default_config():
    if not os.path.exists(CONFIG_FILE_PATH):
        os.makedirs(os.path.dirname(CONFIG_FILE_PATH), exist_ok=True)
        urllib.request.urlretrieve(REMOTE_DEFAULT_CONFIG_FILE_PATH, CONFIG_FILE_PATH)
        if Path(CONFIG_FILE_PATH).is_file():
            with open(CONFIG_FILE_PATH, 'a') as f:
                openAIKey = input("Enter your OpenAI API key (press Enter to skip -> disable AI commit gen): ") 
                f.write(f"\nopenAIKey: {openAIKey}")
        else:
            print("Error: Failed to download the default config file. Exiting.")
            exit(1)

def load_config():
    with open(CONFIG_FILE_PATH, 'r') as stream:
        config = yaml.safe_load(stream)
    return config

def commit_type_prompt(commit_types):
    title = 'Please choose a commit type'
    options = [commit_type['label'] for commit_type in commit_types]
    option, index = pick(options, title)
    return option

def make_commit(config, commit_type):
    # Get the prefix corresponding to the selected commit type
    prefix = next((item['prefix'] for item in config['commit_types'] if item['label'].strip() == commit_type), '')

    if prefix == '':
        print("Error: Invalid commit type. Exiting.")
        return -1

    diffs = subprocess.getoutput('git diff --cached -U5').strip()
    diff_stat = subprocess.getoutput('git diff --cached --stat').strip()

    if diffs.length or diff_stat.length  == 0:
        print("Error: No changes added to commit. Exiting.")
        return -1

    commit_message = generate_commit_message(diff_stat, diffs, prefix, CONFIG_FILE_PATH)
    
    print('Final commit message:', commit_message)
    confirmation = input('Confirm commit? (y/n): ')

    if confirmation.lower() == 'y':
        # Commit the changes
        subprocess.call(['git', 'commit', '-m', f"{prefix}: {commit_message.strip()}"])
        return 0
    else:
        print("Commit cancelled.")
        return -1

def main():

    injector = injector.Injector()
    injector.binder.install(injector.Module(configure, file_path))
    check_dependencies()
    check_git_status()

    create_default_config()
    config = load_config()

    commit_type = commit_type_prompt(config['commit_types'])

    make_commit(config, commit_type)

if __name__ == "__main__":
    main()