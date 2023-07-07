# config_utils.sh

create_default_config() {
    if [[ ! -f "$CONFIG_FILE_PATH" ]]; then
        mkdir -p ~/.aimojicommit
        wget --quiet -O $CONFIG_FILE_PATH "$REMOTE_DEFAULT_CONFIG_FILE_PATH"

        if [[ $? -ne 0 ]]; then
            echo "Error: Failed to download the default config file. Exiting." >&2
            rm "$CONFIG_FILE_PATH"
            exit 1
        fi

        echo "It appears to be the first time you run $0."
        read -p "Enter your OpenAI API key (press Enter to skip -> disable AI commit gen): " openAIKey
        echo "" >> $CONFIG_FILE_PATH
        echo "openAIKey: $openAIKey" >> $CONFIG_FILE_PATH
    fi
}

load_config() {
    LABELS=$(yq e '.commit_types.[].label' $CONFIG_FILE_PATH)
    OPENAI_KEY=$(yq e '.openAIKey' $CONFIG_FILE_PATH)
}