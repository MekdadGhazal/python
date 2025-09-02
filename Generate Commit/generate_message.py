import sys
import os
import subprocess
import google.generativeai as genai
import configparser

# git config --global alias.aicommit '!python generate_message.py'

# run: git add . >> git aicommit 

class AiCommitTool:

    MAX_DIFF_LENGTH = 8000

    def __init__(self):

        ## Empty Config File
        config = configparser.ConfigParser()

        ## Configuration Folder
        script_dir = os.path.dirname(os.path.realpath(__file__))
        config_path = os.path.join(script_dir, 'config.ini')

        ## Read the Config and set API, Model and prompt
        config.read(config_path)

        ## Get the main Variable from 'Config.ini'
        self.api_key = config.get('API', 'key', fallback=None)
        self.model_name = config.get('Settings', 'model', fallback='gemini-1.5-flash-latest')
        self.prompt_template = config.get('Prompt', 'template', fallback='')


    ## Check if the API is set
    def check_api_key(self) -> bool: 
        return bool(self.api_key and self.api_key != "YOUR_API_KEY_HERE")

    ## Generate a new Commit using AI
    def generate_commit_message(self, diff_content: str) -> str:

        if not self.check_api_key():
            return "Error: Google AI API key is not configured in config.ini"
        
        try:
            ## Called Model using API 
            genai.configure(api_key=self.api_key)

            ## Called Model using Name 
            model = genai.GenerativeModel(self.model_name)

            ## Prompt Template with 'diff_content' that contains local Changes
            prompt = self.prompt_template.format(diff_content=diff_content)

            ## Get Response
            response = model.generate_content(prompt)
            
            ## Modify the Response 
            commit_message = response.text.strip().replace("`", "")
            return commit_message
        
        except Exception as e:
            print(f"Error generating commit message: {e}")
            return None


    ## Get the All lines that contain changes 
    def get_staged_diff(self):
        try:
            ## Execute the command: git diff --staged 
            command = ["git", "diff", "--staged"]

            ## Run the command
            result = subprocess.run(command, capture_output=True, text=True, check=True, encoding='utf-8')
            return result.stdout
        except Exception:
            return None


    ## Get a summary for large diffs that lagre than  'MAX_DIFF_LENGTH'
    def get_staged_diff_summary(self) -> str | None:
        try:
            ## Runs command: git diff --staged --stat
            command = ["git", "diff", "--staged", "--stat"]
            result = subprocess.run(command, capture_output=True, text=True, check=True, encoding='utf-8')
            return result.stdout
        except Exception:
            return None

    def run(self):

        ## Get the lines
        diff_content = self.get_staged_diff()

        if not diff_content or not diff_content.strip():
            print("No staged changes to commit. Use 'git add' to stage your changes.")
            sys.exit(1)

        ## To check the length of the diff less than 'MAX_DIFF_LENGTH'
        ##  |__ if it is large : generate a summary using 'get_staged_diff_summary'
        ##  then using 'generate_commit_message' to get AI commit

        if len(diff_content) > self.MAX_DIFF_LENGTH:
            print(f"Diff is too large ({len(diff_content)} chars). Generating message from summary instead.")
            diff_content = self.get_staged_diff_summary()
            if not diff_content:
                print("Could not retrieve diff summary. Aborting.")
                sys.exit(1)

        ## AI message
        ai_message = self.generate_commit_message(diff_content)

        if not ai_message:
            print("Could not generate AI message. Aborting commit.")
            sys.exit(1)
        
        # Make user decied if it want it as a commit message
        check = input(f'The commit has successfully generated.\n\n{ai_message}\n\nDo you want to commit it? (Y): ')
        
        if check.lower() == 'y':
            try:
                ## Run The Git command : git commit -m {ai_message} 
                commit_command = ["git", "commit", "-m", ai_message]
                subprocess.run(commit_command, check=True)
                print("Commit successful!")

            except subprocess.CalledProcessError as e:
                print(f"An error occurred during commit: {e}")
                sys.exit(1)

## Main
if __name__ == '__main__':
    app = AiCommitTool()
    app.run()
