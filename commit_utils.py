import subprocess
import yaml
import tempfile
import os
import generate_commit_msg

def make_commit(CONFIG_FILE_PATH, COMMIT_TYPE, OPENAI_KEY):
    with open(CONFIG_FILE_PATH, 'r') as config_file:
        config = yaml.safe_load(config_file)
    
    prefix = next((item['prefix'] for item in config['commit_types'] if item['label'].strip() == COMMIT_TYPE), '')
    
    if len(prefix.strip()) == 0:
        raise Exception("Error: Invalid commit type. Exiting.")

    changes = subprocess.check_output(["git", "diff", "--cached", "-U5"])
    changes_length = len(changes)
    
    diff_stat = subprocess.check_output(["git", "diff", "--cached", "--stat"])
    diff_stat_length = len(diff_stat)
    
    total_length = diff_stat_length + changes_length
    
    temp_file = tempfile.NamedTemporaryFile(delete = False)

    if total_length < 15000 and len(OPENAI_KEY.strip()) > 0:
        print("Generating AI commit message")
        confirmed = False
        while not confirmed:
            temp_file.write(f'{prefix}: '.encode())
            
            COMMIT_MESSAGE = generate_commit_msg(diff_stat, changes, prefix)  # Call your external function here
            
            if len(COMMIT_MESSAGE.strip()) == 0:
                raise Exception("Error: Unable to determine the commit message. Exiting.")
            
            print(f'\nFinal commit message: {prefix}: {COMMIT_MESSAGE}')
            
            temp_file.write(COMMIT_MESSAGE.strip().encode())
            
            response = input("Edit the message or regenerate? (E/r/q) ")
            
            if not response.upper().startswith('R'):
                confirmed = True
            elif response.upper().startswith('Q'):
                os.remove(temp_file.name)
                return
            else:
                temp_file.truncate(0)
        
        subprocess.run(["git", "commit", "-eF", temp_file.name])
        
        os.remove(temp_file.name)
    else:
        temp_file.write(f'{prefix}: '.encode())
        subprocess.run(["git", "commit", "-eF", temp_file.name])
        os.remove(temp_file.name)


def check_for_preconfigured_merge_commit():
    git_dir = subprocess.check_output(["git", "rev-parse", "--git-dir"]).decode().strip()
    MERGE_MESSAGE_FILE = os.path.join(git_dir, "MERGE_MSG")
    if os.path.isfile(MERGE_MESSAGE_FILE):
        with open(MERGE_MESSAGE_FILE, 'r') as file:
            COMMIT_MESSAGE = file.read()
        print(f'Found preconfigured merge commit message: {COMMIT_MESSAGE}')
        response = input("Do you want to use this message? (Y/n) ")
        if not response.upper().startswith('N'):
            subprocess.run(["git", "commit"])