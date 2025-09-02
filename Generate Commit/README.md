## AI Commit Assistant
An intelligent command-line tool that uses Google's Gemini AI to automatically generate clear, descriptive, and conventional commit messages based on your staged changes. Say goodbye to writing "fix bug" forever!

### Features
AI-Powered Messages: Leverages the power of Google's Gemini AI to analyze your code changes (git diff) and write meaningful commit messages.

Conventional Commits: Enforces the Conventional Commits standard out-of-the-box for a clean and readable Git history.

Handles Large Commits: Intelligently detects when changes are too large and sends a summary (--stat) instead of the full diff to avoid API limits.

Interactive Confirmation: Shows you the generated message and asks for your confirmation before committing, giving you full control.

Fully Configurable: Easily change the AI model, API key, and even the prompt template through a simple config.ini file.

Seamless Integration: Integrates directly with Git through a simple alias (git aicommit), making it feel like a native command.

### Requirements
```bash
Python 3.7+
Git bash 
```

### Installation & Setup
Follow these steps to get the AI Commit Assistant up and running in minutes.

1. Clone or Download the Files
Place the project files (generate_message.py, config.ini, requirements.txt) into your project's root directory.


**(Note: It is recommended to rename generate_message.py to ai_commit.py for clarity).**

2. Install Dependencies
Install the required Python packages using pip:
```bash
pip install -r requirements.txt
```
3. Configure Your API Key:
####
>  3.1. Open the config.ini file.

> 3.2. Obtain a free API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

>3.3. Paste your key into the key field under the [API] section.
```bash
[API]
key = YOUR_API_KEY_HERE
```
4. Set Up the Git Alias **(Recommended)**
To make the tool feel like a native Git command, run this command once in your terminal:

**For Windows/Linux/macOS**
```bash
git config --global alias.aicommit '!python ai_commit.py'
```
This creates a global:
```git aicommit```
command that you can use in any of your Git repositories.

### Usage
Using the tool is as simple as 1-2-3!

Stage Your Changes: Make your code changes and stage them as you normally would.

```bash 
git add .
```

Run the Command: Instead of git commit, use the new alias.

```bash
git aicommit
```

Confirm: The tool will generate a message and ask for your approval.

```bash
Example : 
Generated message: "feat: Implement intelligent diff handling for large commits"
Do you want to commit it? (y/n): y
Type y and press Enter. Your commit will be made!
```

### Configuration
You can customize the tool's behavior by editing the config.ini file:
```bash
[API]
key: Your Google AI API key.

[Settings]
model: The specific Gemini model to use (e.g., gemini-1.5-flash-latest).

[Prompt]
template: The full prompt template sent to the AI. You can modify it to change the tone, language, or format of the generated messages.
```


### Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page (example link).

### License
This project is licensed under the MIT License.