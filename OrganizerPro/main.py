import os
import re
import shutil
from extlist import *
import time
import argparse
import datetime
from openai import OpenAI
import importlib.resources as pkg_resources
from typing import List, Tuple
import json
import sys

class PCSorter:
    """
    File/Folder cleaner.
    :param x: restore file name. string
    :return: none
    """


    files = []
    sub_folders = []
    sub_files = []
    tmp_list = []
    dir_containing_files = []


    def __init__(self, directory, is_backup):

        self.is_backup = is_backup
        self.directory = directory
        self.client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
        self.chatbot = ""
        with open("./data/chatbot.txt") as file:
            self.chatbot = file.read()

    

    def _backup(self):
        """
        Backup function
        """
        if not os.path.isdir("Backup"):
            os.mkdir("Backup")
        else:
            print("Folder already created")

        current_files = os.listdir(".")
        for i in current_files:
            try:
                shutil.copy(i, "./Backup")
            except:
                print("File {} couldn't be moved. Unkown reason!".format(i))
        time.sleep(2)

    def _searchfiles(self, filename):
        """
        Search files.
        :param x: filename string
        :return: path of file string
        """

        if len(self.full_list) == 0:
            self.list_files()

        for i in self.full_list:
            x2 = i.split("\\")
            x2 = x2[-1]
            if filename in x2:
                print("We found your file its located, at {}".format(i))
                return i
    def list_files(self, include_subdirs=False):
        """
        Scans the specified directory and its subdirectories for files, excluding certain files.
        If include_subdirs is False, only files from the root directory are returned.
        Returns a tuple of two lists: (all_files, all_directories).
        """
        excluded_files = {'cleaner.py', 'extlist.py', 'main.py'}
        all_files = []
        all_directories = []
        if not os.path.isabs(self.directory):
            self.directory = os.path.abspath(self.directory)
        for root, dirs, files in os.walk(self.directory):
            if root != os.path.normpath(self.directory) and not include_subdirs:
                print("root", files)
                continue  # Skip subdirectories
            all_directories.append(root)
            for file in files:
                if file not in excluded_files:
                    all_files.append(os.path.join(root, file))
        return all_files, all_directories


    def chatgpt(self, user_input, model="gpt-4-1106-preview", temperature=0, max_tokens=500):
        # Prepare messages for the conversation
        formatted_conversation = [{"role": "system", "content": self.chatbot}]
        formatted_conversation.append({"role": "user", "content": user_input})
        print(model)
        # Create the chat completion using the new API method
        completion = self.client.chat.completions.create(
            model=model,
            messages=formatted_conversation,
            temperature=temperature,
            max_tokens=max_tokens
        )

        # Extract the response
        if completion.choices and completion.choices[0].message:
            chat_response = completion.choices[0].message.content
        else:
            chat_response = "No response generated."

        return chat_response    

    def clean_gpt_output(self, input_str):
        # Find the index of the first '{' character
        start_index = input_str.find('{')
        
        # Find the index of the last '}' character
        end_index = input_str.rfind('}')

        if start_index != -1 and end_index != -1:
            # Slice the string to remove text before the first '{' and after the last '}'
            result_str = input_str[start_index:end_index+1]
            return result_str
        else:
            return "No '{' or '}' characters found in the input string."

    def print_folder_structure(self, json_data):
        # Parse the JSON data into a Python dictionary
        data_dict = json.loads(json_data)
        output = ""
        indent = ""
        for folder, files in data_dict.items():
            output += f"{indent}Folder: {folder}\n"
            for file in files:
                output += f"{indent}  - {file}\n"
        return output

    def sort_files(self, json_response):
        file_movements = []
        # Create folders
        json_data = json.loads(json_response)
        for folder, files in json_data.items():
            # Create the folders
            folder_path = os.path.join(self.directory, folder)
            try:
                if os.path.isdir(folder_path): continue
                else: os.makedirs(folder_path)
                print("Folders created")
            except OSError as error:
                print(f"Creation of the folder '{folder_path}' failed")
                print(error)
            for i in files:
                # Move files to corresponding folder
                shutil.move(os.path.join(self.directory, i), folder_path)
            for i in files:
                original_path = i
                new_path = os.path.join(folder_path, os.path.basename(i))
                file_movements.append(f"{original_path}###{new_path}\n")  # Record the file movement
        with open(self.directory, 'w') as file:
            for movement in file_movements:
                file.write(movement)

    def restore_files(self, restore_file='restore.txt'):
        with open(restore_file, 'r') as file:
            for line in file:
                original_path, new_path = line.strip().split('###')
                shutil.move(new_path, original_path)
                print(f"Restored {new_path} to {original_path}")


def exit_app(args):
    print('Bye')


def sort_files(args):
    # Define default values for various parameters
    default_model: str = 'GPT4'  # Default model to use for text classification
    default_directory: str = os.getcwd()  # Default directory to search for files
    default_backup: bool = False  # Default flag indicating whether to include backup files
    default_include: bool = False  # Default flag indicating whether to include subdirectories

    # Assign values to parameters based on provided arguments
    model: str = args.model if args.model else default_model  # Assign model parameter if provided, otherwise use default
    if model == "custom":
        model = input("select custom model.")   

    directory: str = args.dir if args.dir else default_directory  # Assign directory parameter if provided, otherwise use default
    is_backup: bool = default_backup if args.backup is None else args.backup.lower() == 'true'  # Convert 'backup' argument to boolean value    '
    include_subdirs: bool = default_include if args.include is None else args.include.lower() == 'true'  # Convert 'include_subdirs' argument to boolean value
    if re.match(r"^gpt\-?3", model.lower()): model = "gpt-3.5-turbo"
    else: model = "gpt-4-1106-preview"
    # Create a PCSorter object using the assigned parameters
    sorter: PCSorter = PCSorter(directory=directory, is_backup=is_backup)

    # List all files and directories in the specified directory
    list_files_result = sorter.list_files(include_subdirs)

    # Unpack the result into files and dirs
    files: list[str] = list_files_result[0]
    dirs: list[str] = list_files_result[1]

    # Do the backup: PLACEHOLDER

    # Extract only filenames from the list of files
    only_filename: list[str] = [os.path.basename(i) for i in files]  # Extract base filenames from full filepaths
    print(only_filename)
    
    # Assuming 'only_filename' is a list of filenames and 'model' is a predefined model object
    response: str = sorter.chatgpt(",".join(only_filename), model=model)  # Calling the chatgpt method with a comma-separated string of filenames and the specified model

    clean_response: str = sorter.clean_gpt_output(response)

    print(f"This is the suggested folder structure.\n{sorter.print_folder_structure(clean_response)}")
    while True:
        user_input = input("Is this okay? (y/n): ")
        if user_input.lower() == 'y':
            print("User confirmed the structure.")
            break
        elif user_input.lower() == 'n':
            print("User did not confirm the structure.")
            sys.exit()
        else:
            print("Invalid input. Please enter 'y' for yes or 'n' for no.")

    sorter.sort_files(clean_response) 

def restore_files(args):
    sorter = PCSorter.getInstance()
    sorter._restore()


def main():
    parser = argparse.ArgumentParser(description="File management utility")
    subparsers = parser.add_subparsers(dest='command')

    # Exit command
    exit_parser = subparsers.add_parser('exit')
    exit_parser.set_defaults(func=exit_app)

    # Sort command
    sort_parser = subparsers.add_parser('sort')
    sort_parser.add_argument('--model', type=str, help='Model type for sorting, (Avail: gpt3, gpt4, custom) (default: GPT4)')
    sort_parser.add_argument('--dir', type=str, help='Directory to sort (default: None)')
    sort_parser.add_argument('--include', type=str, help='Include files in subdirectories (default: False)')
    sort_parser.add_argument('--backup', type=str, help='Backup directory for sorted files (default: False)')
    sort_parser.set_defaults(func=sort_files)

    # Restore command
    restore_parser = subparsers.add_parser('restore')
    restore_parser.set_defaults(func=restore_files)

    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

