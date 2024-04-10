import subprocess
import openai
import os
import difflib
import re
import json

issue_title = os.environ["ISSUE_TITLE"]
issue_body = os.environ["ISSUE_BODY"]
open_ai_api_key = os.environ["OPENAI_API_KEY"]
open_ai_tokens = os.environ["OPENAI_TOKENS"]
open_ai_model = os.environ["OPENAI_MODEL"]
chunks = os.environ["FILE_CHUNKS"]

# Step 1: Set up OpenAI API client
openai.api_key = open_ai_api_key
question = issue_body

# Step 2: Read all files from a local repository
def read_all_files_from_directory(directory):
    file_contents = {}
    for root, _, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                file_contents[filepath] = f.read()
    return file_contents

def split_into_chunks(text, chunk_size):
    """
    Splits a text into chunks, each of a maximum size of chunk_size.
    """
    chunks = []
    while text:
        chunk = text[:chunk_size]
        text = text[chunk_size:]
        chunks.append(chunk)
    return chunks


# Step 3: Query OpenAI for changes (this is a simplistic approach and can be refined)
def request_changes_from_openai(context, filename):
    response = openai.Completion.create(
        model=open_ai_model or "gpt-3.5-turbo-instruct",
        prompt="Giving the filename:'" + filename  + "' and the following content:'" + context + "'\n modify the content to provide a solution for this issue:\n'" + question + "'\n and output the result.",
        max_tokens=int(open_ai_tokens) or 200  # you can adjust this based on your needs
    )
    print('reponse choices', response.choices)
    return response.choices[0].text.strip()

def request_changes_from_openai_in_chunks(context, filename, max_chunk_size):
    """
    Request changes from OpenAI by processing the content in chunks.
    """
    # Split the context into chunks
    chunks = split_into_chunks(context, max_chunk_size)

    modified_chunks = []
    for chunk in chunks:
        # Send each chunk to OpenAI
        response = openai.Completion.create(
            model=open_ai_model if len(open_ai_model) else "gpt-3.5-turbo-instruct",
            prompt="Giving the filename:'" + filename + "' and the following content:'" + chunk + "'\n modify the content to provide a solution for this issue:\n'" + question + "'\n and output the result.",
            max_tokens=int(open_ai_tokens) or 200
        )
        modified_chunk = response.choices[0].text.strip()
        modified_chunks.append(modified_chunk)

    # Combine the modified chunks
    return "".join(modified_chunks)


def add_linebreaks(input_list):
    """
    This function takes a list of strings and adds a line break at the end of each string if it's not already there.
    """
    output_list = []
    for item in input_list:
        if not item.endswith('\n'):
            item += '\n'
        output_list.append(item)
    return output_list

def generate_patch(original, modified, filename):
    original_lines = original.splitlines(keepends=True)
    modified_lines = modified.splitlines(keepends=True)
    d = difflib.unified_diff(original_lines, modified_lines, fromfile=filename, tofile=filename)
    return '\n'.join(d)

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
    
    patches = {}

    files_in_prompt = extract_specific_file_path(question)
    files_in_prompt_full_path = []

    for x in files_in_prompt:
        files_in_prompt_full_path.append(directory + x[1:])
    
    for filename, content in all_files.items():
        if filename in files_in_prompt_full_path:
            modified_content = request_changes_from_openai(content, filename) if int(chunks) == 0 else request_changes_from_openai_in_chunks(content, filename, int(chunks))
            print('modified content', modified_content)
            print('original content', content)
            patch = generate_patch(content, modified_content, filename)
            patches[filename] = patch
            print(patch)
    # Saving patches to a file
    with open("changes.patch", "w") as f:
        for filename, patch in patches.items():
            f.write(patch)
            f.write('\n\n')
    subprocess.run(["git", "apply", "changes.patch"], check=True)
