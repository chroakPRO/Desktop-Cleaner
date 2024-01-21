# README for PCSorter Codebase

## Introduction

PCSorter is a Python-based utility designed to organize files in a directory using the OpenAI ChatGPT API. It automates the sorting of files into designated folders, making file management more efficient and user-friendly. This tool is particularly useful for users dealing with cluttered directories, aiming to streamline their digital workspace.

### Dependencies and Prerequisites
- Python 3.x
- OpenAI API key
- External libraries: `os`, `re`, `shutil`, `time`, `argparse`, `datetime`, `json`, `sys`, `openai`
- Additional files: `extlist.py`, `data/chatbot.txt`

## Installation

1. **Clone the Repository:**
   ```bash
   git clone [repository-url]
   ```

2. **Navigate to the Codebase Directory:**
   ```bash
   cd [codebase-directory]
   ```

3. **Install Required Libraries:**
   Ensure Python 3.x is installed on your system. Install additional dependencies using pip:
   ```bash
   pip install openai
   ```

4. **Set Up OpenAI API Key:**
   Export your OpenAI API key as an environment variable:
   Linux
   ```bash
   export OPENAI_API_KEY='your_api_key_here'
   ```
   Windows
   ```bash
  setx OPENAI_API_KEY='your_api_key_here'
   ```

## Usage

### Basic Commands
- **Sorting Files:**
  ```bash
  python main.py sort --dir [directory-path] --model [model-type]
  ```
  - `--dir`: Directory to sort (default: current directory)
  - `--model`: Model type for sorting (default: GPT4)

- **Restoring Files:**
  ```bash
  python main.py restore --file [restore-file-name]
  ```
  - `--file`: Restore file name & location (default: `restore.txt` in current directory)

### Sample Input
To sort files in the current directory using the default GPT4 model:
```bash
python main.py sort
```

## Code Structure

- **Main Components:**
  - `PCSorter`: Main class for sorting files.
  - `main.py`: Entry point of the application, handling command-line arguments.

- **Important Functions:**
  - `list_files`: Lists files in the specified directory.
  - `chatgpt`: Interacts with OpenAI's ChatGPT API.
  - `sort_files`: Organizes files into directories based on ChatGPT's suggestions.
  - `restore_files`: Restores files to their original locations.

- **Directory Structure:**
  - `data/`: Contains data files like `chatbot.txt`.
  - `extlist.py`: A module for listing file extensions.

## Troubleshooting

- **Common Issues:**
  - Invalid API key: Ensure the OPENAI_API_KEY environment variable is correctly set.
  - Missing dependencies: Verify all required Python libraries are installed.

- **Solutions:**
  - Recheck the API key and environment variable setup.
  - Run `pip install -r requirements.txt` to install missing libraries.

- **Limitations:**
  - The tool currently does not support nested directory sorting.

## Contributing

Contributions to PCSorter are welcome. To contribute:
- Report bugs and suggest improvements via GitHub issues.
- Submit pull requests with new features or bug fixes.
- For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---
