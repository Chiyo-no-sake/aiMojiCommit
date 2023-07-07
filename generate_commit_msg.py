import openai
import yaml
import sys
import os
import time

def load_api_key(api_key_file):
    with open(api_key_file) as file:
        api_key = yaml.safe_load(file)
    return api_key['openAIKey']

def generate_commit_message(stats, diffs, commit_prefix, api_key_file):
    # Set up your OpenAI API key
    openai.api_key = load_api_key(api_key_file)
    prompt = f"""Generate a concise and descriptive git commit message written in present tense and using only natural language and no emoji. Logically group changes and write a short sentence for each. Maintain the output in one single line. Base your answer only on the following git stats and diffs:

##Git Stats
{stats}

##Git Diffs
{diffs}

##Commit Message
{commit_prefix}:"""

    retries = 3  # Number of retries
    for attempt in range(1, retries + 1):
        try:
            response = openai.Completion.create(
                engine='text-davinci-003',
                prompt=prompt,
                max_tokens=64,
                temperature=.6,
                n=1,
                stop=None,
            )
            commit_message = response.choices[0].text.strip()
            return commit_message
        except Exception as e:
            sys.stderr.write(f"OpenAI request failed (attempt {attempt}/{retries}): {str(e)}")
            if attempt == retries:
                raise

            # Retry after a delay
            wait_time = 1  # seconds
            sys.stderr.write(f"Retrying in {wait_time} seconds...")
            time.sleep(wait_time)

try:
    stats = sys.argv[1]
    diffs = sys.argv[2]
    commit_prefix = sys.argv[3]
    api_key_file = sys.argv[4]
    commit_msg = generate_commit_message(stats, diffs, commit_prefix, api_key_file)
    print(commit_msg)
except Exception as e:
    sys.stderr.write(f"Error: {str(e)}")
    sys.exit(1)