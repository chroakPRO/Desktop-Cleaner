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

    def _restore(self):
        """
        Restore previous cleaning session
        :return: none
        """
        try:
            with open(self.resetname, "r") as f:
                print("Opening restore file...")
                lines = f.readlines()
                for i in lines:
                    restore_dir = i
                    restore_dir = restore_dir.split("###")

                    program_name = r"{}".format(restore_dir[0].replace("\n", ""))
                    restore_path = r"{}".format(restore_dir[1].replace("\n", ""))
                    curry_path = r"{}".format(restore_dir[2].replace("\n", ""))
                    restore_path = os.path.join(restore_path.strip())
                    cur_path = os.path.join(curry_path)
                    if os.path.exists(cur_path):
                        res_path = restore_path.replace(program_name, "")
                        res_path = os.path.join(res_path)
                        if os.path.exists(res_path):
                            shutil.move(cur_path, restore_path)
                        else:
                            os.makedirs(res_path)
                            shutil.move(cur_path, restore_path)
                print("All files have been restored...")
            # Delete old folders after restorting. 
            for i in ext_dir:
                cur_path = os.path.join(self.current_path, i)
                if os.path.isdir(cur_path):
                    shutil.rmtree(cur_path)
                else:
                    pass
                    #print("Couldnt delete directory.")
            os.remove(self.resetname)
            print("All old sort folders have been deleted...")
            time.sleep(2)
        except FileNotFoundError:
            print("The file was not found..")
        except:
            print("Unkown Error.")

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
        excluded_files = {'cleaner.py', 'extlist.py'}
        all_files = []
        all_directories = []

        for root, dirs, files in os.walk(self.directory):
            if root != os.path.normpath(self.directory) and not include_subdirs:
                continue  # Skip subdirectories
            all_directories.append(root)
            for file in files:
                if file not in excluded_files:
                    all_files.append(os.path.join(root, file))

        return all_files, all_directories


    def _create_sort_folders(self, ext_dict):
            print("Creating folders...")
            for i in ext_dict:
                ext_path_dir = ext_dict[i]
                if os.path.isdir("./{}".format(ext_path_dir)):
                    print("Folder -> {} already exists".format(ext_path_dir))
                    continue
                else:
                    print("Created Folders -> {}".format(ext_path_dir))    
                    os.makedirs("{}".format(ext_path_dir))
            return True


    def _write_restore_file(self, lists):
        try:
            with open(self.resetname, "w") as f:
                for i in lists:
                    f.write(i)
                f.close()
        except:
            print("_write_restore_file ERROR")


    def _sort_files(self, filenames):

        tmp_list = []
        dir_containing_files = []   
        print("Sorting Files...")
        for i in filenames:
            file_ext = os.path.splitext(i)
            for ext_key in extension_paths:               
                if file_ext[1] == ext_key:   
                    spec_dir = extension_paths["{}".format(ext_key)]

                    file_name = i.split("\\")
                    file_name = file_name[-1]

                    file_path = os.path.join(self.current_path, spec_dir, file_name)               
                    path = os.path.join(self.current_path, spec_dir)
                    old_path = os.path.join(i)
                    if not os.path.exists(file_path):
                        tmp_list.append("{}###{}###{} \n".format(file_name, old_path, file_path))
                        time.sleep(0.01)
                        try:
                            shutil.move(i, path)
                        except:
                            #print("Couldnt move the file.")
                            dir_containing_files.append(os.path.join(file_ext[0]))
                        break
        print("Writing files to restore.txt")
        return dir_containing_files, tmp_list

    def _delete_sorted_folders(self, none_sorted, sub_folders):
        for i in sub_folders:
            if i in none_sorted:
                continue
            else:
                try:
                    shutil.rmtree(os.path.join(i))
                except:
                    print("Couldnt delete folder")


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
    is_backup: bool = default_backup if args.backup is None else args.backup.lower() == 'true'  # Convert 'backup' argument to boolean value
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

