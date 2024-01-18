import os
import shutil
from extlist import *
import time
import argparse
import datetime
from openai import OpenAI
import importlib.resources as pkg_resources

# Delete folders after sorting.
# And delete files.
# Threading and mutliprocessor.



# Add more printing features. 

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


    def __init__(self, model, directory, is_backup):

        self.is_backup = is_backup
        self.directory = directory
        self.model = model
        self.client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
        self.chatbot = open("./data/chatbot.txt")
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
            self._listfiles()

        for i in self.full_list:
            x2 = i.split("\\")
            x2 = x2[-1]
            if filename in x2:
                print("We found your file its located, at {}".format(i))
                return i


    def _listfiles(self):

        files = []
        sub_folders_main = []
        sub_folders = []
        sub_files = []

        print("Scanning for files...")
        #Lists that hold, directory/file names.
        current_files = os.listdir(self.current_path)

        # This loop the files in the current dir.
        # Where the py file is located.
        for i in current_files:
            # If its a dir, or the main file.
            if not os.path.isdir(i):
                if i not in ['cleaner.py', 'extlist.py']:
                    current_dir = os.path.join(self.current_path, i)
                    files.append(current_dir)
            
            # If its a dir.

            elif os.path.isdir(i):
                subdir_file_list = []
                # This checks if its the first time we run this elif
                first_time = True
                sub_folders_main.append(os.path.join(self.current_path, i))
                
                while True:

                    if not len(subdir_file_list) and first_time:

                        first_time = False
                        first_sub_path = os.path.join(self.current_path, i)
                        sub_dir_wo_file = os.path.join(self.current_path, i)
                        sub_folders.append(first_sub_path)

                        sub_files = os.listdir(first_sub_path)
                        for j in sub_files:
                            sub_path = os.path.join(self.current_path, i, j)
                            if not os.path.isdir(sub_path):
                                files.append(sub_path)
                            if os.path.isdir(sub_path):
                                subdir_file_list.append(sub_path)
                    
                    elif not len(subdir_file_list):
                        first_time = False
                        break

                    else:
                        for l1, l in enumerate(subdir_file_list):
                            sub_files = os.listdir(os.path.join(l))
                            for p in sub_files:
                                sub2_file_path = os.path.join(l, p)
                                if not os.path.isdir(sub2_file_path):
                                    files.append(sub2_file_path)
                                if os.path.isdir(sub2_file_path):
                                    sub_folders.append(sub2_file_path)
                                    subdir_file_list.append(sub2_file_path)
                            subdir_file_list.pop(l1)                                                                                                 
                else:
                    continue

        print("Scan finished, found {} files..".format(len(files)))
        time.sleep(1)
        self.full_list = files
        return files, sub_folders_main, sub_folders


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



    def _clean_dirs(self):
        
        today = time.strftime('%Y-%m-%d', time.localtime())
        today = today.split("-")
        today_days = ((int(today[0]) * 365 ) + (int(today[1]) * 30) + int(today[2])) 

        for i in self.full_list:
            epoch_time = os.path.getatime(i)
            last_accessed = time.strftime('%Y-%m-%d', time.localtime(epoch_time))
            last_accessed = last_accessed.split("-")

            last_accessed_days = ((int(last_accessed[0]) * 365 ) + (int(last_accessed[1]) * 30) + int(last_accessed[2]))

            diff = today_days - last_accessed_days

            # Meaning the file is older then 90 days.
            if diff > 90:
                print("delete file.")

    def _chatgpt(self, conversation, chatbot, user_input, model="gpt-4-0613", temperature=0, max_tokens=500):
        # Prepare messages for the conversation
        formatted_conversation = [{"role": "system", "content": chatbot}]
        for message in conversation:
            if isinstance(message, dict) and "role" in message and "content" in message:
                formatted_conversation.append(message)
            else:
                formatted_conversation.append({"role": "user", "content": message})

        formatted_conversation.append({"role": "user", "content": user_input})

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



def exit_app(args):
    print('Bye')

def sort_files(args):
    default_model = 'GPT4'
    default_directory = os.getcwd()
    default_backup = False

    model = args.model if args.model else default_model
    directory = args.dir if args.dir else default_directory
    # Corrected handling for is_backup
    is_backup = default_backup if args.backup is None else args.backup.lower() == 'true'

    #sorter = PCSorter(model=model, directory=directory, is_backup=is_backup)

    # Your additional logic
    print(f'Sorting files in directory: {directory}, using model: {model}, with backup: {is_backup}')


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
    sort_parser.add_argument('--model', type=str, help='Model type for sorting (default: GPT4)')
    sort_parser.add_argument('--dir', type=str, help='Directory to sort (default: None)')
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

