# aiMojiCommit 📝🤖

aimojicommit is a lightweight tool that helps you generate meaningful commit messages for your Git commits. It uses AI-powered text generation to suggest commit messages based on your changes and provides a selection of commit types to choose from, with customizable categories 💡

## Installation 💻 (testend on MacOS arm64 only)

Install this software using pip:
  
  ```shell
  pip install aimojicommit
  ```

After this, it will be available as `aimoji` in your terminal.

### Manual installation
- Clone this repository
- Run `pip install .` in the root directory of the repository

```

## Dependencies 🛠️

aiMojiCommit is born for and relies on git, which must be installed and available as 'git' in your PATH.
Also, aiMojiCommit is a python package, and it needs Python 3.10 or higher to run.


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