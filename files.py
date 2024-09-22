import os
import subprocess

# Define the directory structure
structure = {
    "app.py": "",
    "config.py": "",
    "requirements.txt": "",
    ".gitignore": "",
    "README.md": "",
    "static/css/custom.css": "",
    "templates/base.html": "",
    "templates/home.html": "",
    "templates/signup.html": "",
    "templates/login.html": "",
    "templates/homework.html": ""
}

# Create the files and directories
for path, content in structure.items():
    directory = os.path.dirname(path)
    if directory:  # Only create directories if the path is not at the root level
        os.makedirs(directory, exist_ok=True)
    with open(path, 'w') as file:
        file.write(content)

# Create a virtual environment
subprocess.run(['python3', '-m', 'venv', 'venv'])

# Activate the virtual environment
# Note: Activation is shell-specific and can't be done within a script.
# You need to run the following command manually in your terminal:
# source venv/bin/activate

# Install necessary packages (if any)
# subprocess.run(['venv/bin/pip', 'install', '-r', 'requirements.txt'])