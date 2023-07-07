#!/bin/bash

source ./check_dependencies.sh
source ./check_git_status.sh
source ./config_utils.sh
source ./commit_utils.sh

CONFIG_FILE_PATH=~/.aimojicommit/config.yaml
REMOTE_DEFAULT_CONFIG_FILE_PATH=https://raw.githubusercontent.com/Chiyo-no-sake/aiMojiCommit/main/config.yaml

# Check dependencies
check_dependencies

# Check git status
check_git_status

# Load or create default config
load_config $CONFIG_FILE_PATH $REMOTE_DEFAULT_CONFIG_FILE_PATH

# Parse command line arguments
while getopts "t:" opt; do
    case ${opt} in
        t)
            COMMIT_TYPE=$OPTARG
            ;;
        \?)
            echo "Invalid option: -$OPTARG" 1>&2
            exit 1
            ;;
        :)
            echo "Option -$OPTARG requires an argument" 1>&2
            exit 1
            ;;
    esac
done

# Check if there is a preconfigured commit message
check_for_preconfigured_merge_commit

# If commit type is not provided as a CLI argument, prompt user for it
if [[ -z $COMMIT_TYPE ]]; then
    COMMIT_TYPE=$(prompt_commit_type)
fi

# Perform the commit
make_commit