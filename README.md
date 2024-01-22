# README for PCSorter

## Introduction

PCSorter is a Python-based utility designed to intelligently organize files in a directory using the OpenAI ChatGPT API. This tool scans a specified directory (including subdirectories if desired), classifies files based on content and type, and reorganizes them into a more structured format. It leverages the advanced capabilities of OpenAI's GPT models to understand and categorize file contents, making file management more efficient and intuitive.

Key Features:
- File sorting using AI-driven insights.
- Customizable directory and file type handling.
- Backup and restore functionality for sorted files.
- Cross-platform compatibility with detailed setup instructions.

## Requirements

- Python 3.6 or higher
- `openai` Python package
- Additional Python libraries: `os`, `re`, `shutil`, `time`, `argparse`, `datetime`, `json`, `sys`
- An active OpenAI API key

## Installation Instructions

1. Ensure Python 3.6+ is installed on your system.
2. Install AiSort via pip
   ```
   pip install aisort 
   ```
5. Set up an environment variable for your OpenAI API key (instructions in the next section).

### Setting Up Environment Variables

#### Windows

1. **Command Prompt:**
   - Use `setx OPENAI_API_KEY "Your-API-Key"` to set the API key.
2. **PowerShell:**
   - Apply `$env:OPENAI_API_KEY = "Your-API-Key"` to set the key.
3. **Editing System Properties:**
   - Open System Properties -> Advanced -> Environment Variables.
   - Add a new System variable named `OPENAI_API_KEY` with your API key as its value.

#### macOS

1. **Using Terminal:**
   - Add `export OPENAI_API_KEY="Your-API-Key"` to your `.bash_profile` or `.zshrc`.
2. **Editing `.bash_profile` or `.zshrc`:**
   - Open these files in a text editor and add the export line as above.

#### Linux

1. **Using Terminal:**
   - Similar to macOS, use `export OPENAI_API_KEY="Your-API-Key"` in `.bashrc` or equivalent.
2. **Editing `.bashrc` or equivalent:**
   - Open the file in an editor and add the export command.

## Configuration

Before running PCSorter, ensure the `OPENAI_API_KEY` environment variable is set.

## Usage Instructions

1. **Running the script:**
   - Execute `AiSort` in your terminal.
   - Use command-line arguments to specify options like `--model`, `--dir`, `--include`, `--backup`.
2. **Common use cases:**
   - Sorting files in the current directory: `AiSort sort --dir ./my_directory`
   - Using a specific GPT model: `AiSort sort --model gpt-3.5-turbo`

## Troubleshooting

- **API Key Not Recognized:** Ensure the environment variable `OPENAI_API_KEY` is correctly set.
- **Permission Errors:** Run the script with appropriate permissions or from a non-restricted directory.
- **Invalid Model Specified:** Check that the model name is correct and supported.

## FAQs

- **Can PCSorter handle large directories?**
  Yes, but performance may vary based on the number and size of files.

## Contributing

Contributions to PCSorter are welcome. Please submit issues and pull requests through GitHub, adhering to the project's coding standards and guidelines.

## License

PCSorter is released under the MIT License. See the LICENSE file for more details.

## Acknowledgments

Thanks to the contributors and to OpenAI for the API that powers this project. Special thanks to [list any special contributors or resources].