# aiMojiCommit 📝🤖

aimojicommit is a lightweight tool that helps you generate meaningful commit messages for your Git commits. It uses AI-powered text generation to suggest commit messages based on your changes and provides a selection of commit types to choose from, with customizable categories 💡

## Installation 💻

Sure! Here are the installation instructions for your tool, "aiMojiCommit":

## Installation

### Windows (wip)

Open PowerShell as an administrator and run the following command:

```powershell
iex "& { $(irm -useb https://github.com/Chiyo-no-sake/aiMojiCommit/releases/latest/download/aimojicommit-windows.zip -Headers @{ 'user-agent' = 'Mozilla/5.0'; 'accept' = '*/*' }) }"; Move-Item -Path .\aimojicommit.exe -Destination $env:USERPROFILE\AppData\Local\bin\aimoji.exe -Force
```

### macOS - arm64

Open Terminal and execute the following command:

```bash
curl -LOJ https://github.com/Chiyo-no-sake/aiMojiCommit/releases/latest/download/aimojicommit-macos-arm64 && sudo mv ./aimojicommit-macos-arm64 /usr/local/bin/aimoji && sudo chmod +x /usr/local/bin/aimoji
```

### Linux (wip)

Open a terminal and run the following command:

```bash
curl -LOJ https://github.com/Chiyo-no-sake/aiMojiCommit/releases/latest/download/aimojicommit-linux-amd64 > aimoji && sudo mv ./aimoji /usr/local/bin/aimoji && sudo chmod +x /usr/local/bin/aimoji
```

Once installed, you can use the tool by running `aimoji` in any location within your terminal.

### Manual installation
Head to the release page and download the latest release for your operating system. Extract the archive and move the `aimojicommit` executable to a directory in your PATH. You can also rename the executable to `aimoji` if you wish to be able to use the tool by running `aimoji` in your terminal.

```

## Dependencies 🛠️

aiMojiCommit is born for and relies on git, which must be installed and available as 'git' in your PATH.


## Configuration ⚙️

aiMojiCommit uses a configuration file to specify commit types and OpenAI API key. The default configuration file is located at `$HOME/.aimojicommit/config.yaml`. If the configuration file doesn't exist, aiMojiCommit will create it for you and prompt you to enter your OpenAI API key and choose the model to use, model IDs that ends with 32k are recommended, since they have a bigger context window and allows generating commit messages for longer diffs.

To modify the commit types or update your OpenAI API key or model, edit the `config.yaml` file using a text editor, or use the `aimoji set-key <openai key>` or `aimoji set-model <openai-model-id>` commands (use `aimoji list-models` to list all your available models).

## Usage 🚀

To use aimojicommit, navigate to a Git repository and run the following command:

```shell
aimoji [-t COMMIT_TYPE]
```

If the `-t` option is omitted, aimojicommit will prompt you to choose a commit type interactively. The commit type determines the prefix of the commit message.

Once you select a commit type, aimojicommit will generate a suggested commit message based on the changes in your repository using the OpenAI API. If the changes are small enough and you have provided an OpenAI API key in the configuration file, aimojicommit will include the generated commit message automatically. Otherwise, aimojicommit will open a text editor for you to review and modify the commit message before committing.

If there are any preconfigured merge commit messages, aimojicommit will prompt you to use them before making the commit.

## Contributing 🤝

If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request on the [GitHub Issues page](https://github.com/Chiyo-no-sake/aiMojiCommit/issues).

## License 📄

This project is licensed under the MIT License