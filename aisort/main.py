import os
import re
import shutil
import time
import argparse
import datetime
from openai import OpenAI
import importlib.resources as pkg_resources
from typing import List, Tuple
import json
import sys
from . import data  # relative import for your data package
class PCSorter:
    """
    A class to sort files using the OpenAI ChatGPT API.
    """

    def __init__(self, directory, is_backup):
        """
        Init function.

        Args: 
            directory (str): The directory to sort.
            is_backup (bool): Whether the directory is a backup or not.
        """
        self.is_backup = is_backup
        self.directory = directory
        self.client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
        self.chatbot = ""

        with pkg_resources.open_text(data, 'chatbot.txt') as file:
            self.chatbot = file.read()
             
    def list_files(self, include_subdirs: bool=False):
        """
        Scans the specified directory and its subdirectories for files, excluding certain files.
        If include_subdirs is False, only files from the root directory are returned.
        
        Args:
            include_subdirs (bool): Whether to include files from subdirectories.

        Returns:
            List[str]: A list of files in the specified directory.
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


    def chatgpt(self, user_input: str, model: str="gpt-4-1106-preview", temperature: float=0, max_tokens: float=500):
        """
        Calls the OpenAI API to generate a response to the user's input.

        Args:
            user_input (str): The user's input to the chatbot.
            model (str): The model to use for the chat completion.
            temperature (float): The temperature of the chat completion.
            max_tokens (int): The maximum number of tokens to generate for the chat completion.

        Returns:
            str: The response from the chatbot.
        """
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

    def clean_gpt_output(self, input_str: str):
        """
        Cleans up the chatgpt output

        Args:
            input_str (str): The input string to clean.

        Returns:
            str: The cleaned string.
        """
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

    def print_folder_structure(self, json_data: str):
        """
        Prints the folder structure in a human-readable format.

        Args:
            json_data (str): A JSON string that maps folders to files.

        Returns:
            str: A human-readable string representation of the folder structure.
        """
        # Parse the JSON data into a Python dictionary
        data_dict = json.loads(json_data)
        output = ""
        indent = ""
        for folder, files in data_dict.items():
            output += f"{indent}Folder: {folder}\n"
            for file in files:
                output += f"{indent}  - {file}\n"
        return output

    def sort_files(self, json_response: str):
        """
        Sorts files into directories based on the provided JSON response.

        Args:
            json_response (str): A JSON string that maps folders to files.

        Returns:
            None: This function doesn't return anything but creates directories and moves files.
        """
        file_movements: List[str] = []
        # Create folders
        try: 
            json_data = json.loads(json_response)
        except json.decoder.JSONDecodeError:
            print("Invalid JSON response")
            return
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
                file_movements.append(f"{os.path.join(self.directory, original_path)}###{new_path}\n")  # Record the file movement
        try:
            restore_file_path = os.path.join(self.directory, 'restore.txt')
            with open(restore_file_path, 'w') as file:
                for movement in file_movements:
                    file.write(movement)
        except OSError as error:
            print(f"Creation of the file '{self.directory}' failed")
            print(error)
        
def exit_app(args):
    print('Bye')


def sort_files(args):
    # Define default values for various parameters
    default_model: str = 'GPT4'  # Default model to use for text classification
    default_directory: str = os.getcwd()  # Default dirctory to search for files
    default_backup: bool = True  # Default flag indicating whether to include backup files
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
    default_directory: str = os.getcwd()
    default_file: str = 'restore.txt'
    file: str = args.file if args.file else default_file
    
    sorter = PCSorter(default_directory, False)
    sorter.restore_files(file)

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
    restore_parser.add_argument('--file', type=str, help="Restore file name & location (default: Current dir & restore.txt)")
    restore_parser.set_defaults(func=restore_files)

    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

