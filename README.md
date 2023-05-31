# aiMojiCommit 📝🤖

aimojicommit is a lightweight tool that helps you generate meaningful commit messages for your Git commits. It uses AI-powered text generation to suggest commit messages based on your changes and provides a selection of commit types to choose from, with customizable categories 💡

## Installation 💻

To install aiMojiCommit, run the following command:

```shell
mkdir -p ~/.aimojicommit && \
  wget --quiet -O - https://raw.githubusercontent.com/Chiyo-no-sake/aiMojiCommit/main/aimoji > ~/.aimojicommit/aimoji && \
  chmod +x ~/.aimojicommit/aimoji && \
  sudo ln -sf ~/.aimojicommit/aimoji /usr/local/bin/aimoji
```

## Dependencies 🛠️

aiMojiCommit relies on the following dependencies:

- `git`: Version control system
- `fzf`: Command-line fuzzy finder
- `yq`: Command-line YAML processor
- `python3`: Python interpreter
- `openai`: Python package for OpenAI API
- `pyyaml`: Python package for YAML

Make sure these dependencies are installed on your system before using aiMojiCommit.
To install them, follow this instructions:

#### Debian
  
```sh
sudo apt install -y git fzf python3 python3-pip && \
python3 -m pip install openai pyyaml
```
#### Linux
Refer to you distro's package manager documentation

#### MacOS
```sh
brew install git fzf python3 python3-pip && \
python3 -m pip install openai pyyaml
```


## Configuration ⚙️

aiMojiCommit uses a configuration file to specify commit types and OpenAI API key. The default configuration file is located at `~/.aimojicommit/config.yaml`. If the configuration file doesn't exist, aiMojiCommit will create it for you and prompt you to enter your OpenAI API key. If no API key is provided, aiMojiCommit will not use the OpenAI API and will prompt you to review and modify the commit message before committing

To modify the commit types or update your OpenAI API key, edit the `config.yaml` file using a text editor.

## Usage 🚀

To use aimojicommit, navigate to a Git repository and run the following command:

```shell
aimoji [-t COMMIT_TYPE]
```

If the `-t` option is omitted, aimojicommit will prompt you to choose a commit type interactively. The commit type determines the prefix of the commit message.

Once you select a commit type, aimojicommit will generate a suggested commit message based on the changes in your repository using the OpenAI API. If the changes are small enough and you have provided an OpenAI API key in the configuration file, aimojicommit will include the generated commit message automatically. Otherwise, aimojicommit will open a text editor for you to review and modify the commit message before committing.

If there are any preconfigured merge commit messages, aimojicommit will prompt you to use them before making the commit.

## Contributing 🤝

If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request on the [Github Issues page](https://github.com/Chiyo-no-sake/aiMojiCommit/issues).

## License 📄

This project is licensed under the MIT License