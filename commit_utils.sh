# commit_utils.sh

prompt_commit_type() {
  echo "$LABELS" | fzf --header 'Please choose a commit type'
}

determine_commit_message() {
  export COMMIT_DIFFS=$1
  export COMMIT_STATS=$2
  export COMMIT_PREFIX=$3
  local COMMIT_MESSAGE=$(
    python - <<EOF
import openai
import yaml
import sys
import os
import time

def load_api_key():
    api_key_file = os.path.expanduser("$CONFIG_FILE_PATH")
    with open(api_key_file) as file:
        api_key = yaml.safe_load(file)
    return api_key['openAIKey']

def generate_commit_message(stats, diffs):
    # Set up your OpenAI API key
    openai.api_key = load_api_key()
    commit_prefix = os.environ['COMMIT_PREFIX']
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
    commit_diffs = os.environ['COMMIT_DIFFS']
    commit_stats = os.environ['COMMIT_STATS']
    commit_msg = generate_commit_message(commit_stats, commit_diffs)
    sys.stdout.write(commit_msg)
except Exception as e:
    sys.stderr.write(f"Error: {str(e)}")
    sys.exit(1)
EOF
  )

  if [[ $? -ne 0 ]]; then
    echo "Error: Failed to execute the Python script. Exiting." >&2
    exit 1
  fi

  echo $COMMIT_MESSAGE
}

make_commit() {
  local PREFIX=$(python -c "import yaml; config = yaml.safe_load(open('$CONFIG_FILE_PATH')); print(next((item['prefix'] for item in config['commit_types'] if item['label'].strip() == '$COMMIT_TYPE'), ''))")

  if [[ -z $PREFIX ]]; then
    echo "Error: Invalid commit type. Exiting."
    exit 1
  fi

  local CHANGES=$(git diff --cached -U5)
  local CHANGES_LENGTH=$(echo $CHANGES | wc -c)

  local DIFF_STAT=$(git diff --cached --stat)
  local DIFF_STAT_LENGTH=$(echo $DIFF_STAT | wc -c)

  local TOT_LENGTH=$(expr $DIFF_STAT_LENGTH + $CHANGES_LENGTH)

  # Create a temporary file
  TEMP_FILE=$(mktemp)

  if [[ $TOT_LENGTH -lt 15000 && -n $OPENAI_KEY ]]; then
    echo "Generating AI commit message"

    local confirmed=false
    while [[ $confirmed == false ]]; do
      # Write the prefix to the temporary file
      echo -n "${PREFIX}" >$TEMP_FILE
      echo -n ": " >>$TEMP_FILE

      # Call the external function to determine the commit message
      COMMIT_MESSAGE=$(determine_commit_message "$DIFF_STAT" "$CHANGES" "$PREFIX")

      if [[ -z $COMMIT_MESSAGE ]]; then
        echo "Error: Unable to determine the commit message. Exiting."
        exit 1
      else
        echo
        echo Final commit message: >&2
        echo "$PREFIX: ""$COMMIT_MESSAGE" >&2
      fi

      # Append the generated commit message to the temporary file
      echo -n "$COMMIT_MESSAGE" >>$TEMP_FILE

      # Ask if the message is ok or must be regenerated
      read -p "Edit the message or regenerate? (E/r/q) " -n 1 -r
      echo
      if [[ ! $REPLY =~ ^[Rr]$ ]]; then
        confirmed=true
      elif [[ $REPLY =~ ^[Qq]$ ]]; then
        rm $TEMP_FILE
        exit 0
      else
        # Remove the generated commit message from the temporary file
        echo -n '' >$TEMP_FILE
      fi
    done

    # Use the temporary file as the commit message template
    git commit -eF $TEMP_FILE

    # Remove the temporary file
    rm $TEMP_FILE
  else
    # Write the prefix to the temporary file
    echo -n "${PREFIX}" >$TEMP_FILE
    git commit -eF $TEMP_FILE
    rm $TEMP_FILE
  fi
}

check_for_preconfigured_merge_commit() {
  MERGE_MESSAGE_FILE=$(git rev-parse --git-dir)/MERGE_MSG
  if [[ -f $MERGE_MESSAGE_FILE ]]; then
    COMMIT_MESSAGE=$(cat $MERGE_MESSAGE_FILE)
    echo "Found preconfigured merge commit message: $COMMIT_MESSAGE"
    read -p "Do you want to use this message? (Y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
      git commit
      exit 0
    fi
  fi
}