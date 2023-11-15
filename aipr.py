import subprocess
import openai
import os
import difflib
import re
import json

# print(json.dumps(dict(os.environ), indent=4))

issue_title = os.environ["ISSUE_TITLE"]
issue_body = os.environ["ISSUE_BODY"]
open_ai_api_key = os.environ["OPENAI_API_KEY"]

# Step 1: Set up OpenAI API client
openai.api_key = open_ai_api_key
question = issue_title + "\n\n" + issue_body + "\n\n"

# Step 2: Read all files from a local repository
def read_all_files_from_directory(directory):
    file_contents = {}
    for root, _, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                file_contents[filepath] = f.read()
    return file_contents

# Step 3: Query OpenAI for changes (this is a simplistic approach and can be refined)
def request_changes_from_openai(context):
    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        #engine="gpt-3.5-turbo",
        #prompt=context + "\n\n insert a title 'created by AIPRs README' on README.md file and 'Created by AIPRs other' on otherfile.txt file \n\n",
        prompt=question,
        max_tokens=100  # you can adjust this based on your needs
    )
    print('reponse choices', response.choices)
    return response.choices[0].text.strip()

# Step 4: Generate a Git-like patch
def generate_patch(original, modified, filename):
    d = difflib.unified_diff(original.splitlines(), modified.splitlines(), filename, filename)
    return '\n'.join(list(d))

def extract_specific_file_path(text):
    # Regular expression to find file paths in a specific format as per the example
    # This regex will look for a path that starts with './' followed by a directory structure
    # and a file name with an extension.
    regex = r"\.\/[\w\/.-]+\.\w+"

    # Find all matches in the text
    file_paths = re.findall(regex, text)
    
    return file_paths

# Main script
if __name__ == "__main__":
    directory = './repo'
    all_files = read_all_files_from_directory(directory)
    #print('all files', all_files)

    patches = {}

    file_in_prompt = extract_specific_file_path(question)
    print('----------------------------------\n')
    print('files in prompt', file_in_prompt)
    print('----------------------------------\n')
    
    for filename, content in all_files.items():
        print('filename: ', filename)
        if filename in file_in_prompt:
            modified_content = request_changes_from_openai(content)
            print('modified content', modified_content)
            patch = generate_patch(content, modified_content, filename)
            patches[filename] = patch
            print(patch)
    # Saving patches to a file
    with open("changes.patch", "w") as f:
        for filename, patch in patches.items():
            f.write(patch)
            f.write('\n\n')
    #subprocess.run(["git", "apply", "../changes.patch"], check=True)
