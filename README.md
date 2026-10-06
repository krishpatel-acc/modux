# Modux

**Modux** is a cross-platform AI terminal assistant that lets you interact with your computer using natural language.

Instead of remembering operating-system-specific commands, you can simply tell Modux what you want to do.

For example:

```text
Modux > create a folder named projects
```

Modux understands the request and performs the appropriate operation for your operating system.

Modux is designed to work across:

- Windows
- Linux
- macOS

---

# Features

- 🤖 AI-powered terminal assistant
- 💬 Natural-language interaction
- 🖥️ Windows, Linux and macOS support
- 📁 File and directory operations
- 🔍 Code inspection
- 🛠️ AI-assisted code fixing
- ▶️ Python and Bash file execution
- 🐛 Automatic error analysis
- 📊 Project understanding
- 💾 Secure API-key storage
- ✅ Confirmation before system actions
- 🧪 Automated tests

---

# How Modux Works

Modux separates the AI from the operating-system execution layer.

```text
User request
     │
     ▼
   Modux
     │
     ▼
   Groq AI
     │
     ▼
  User intent
     │
     ▼
Modux execution layer
     │
 ┌───┼────┐
 ▼   ▼    ▼
Win Linux macOS
 │   │    │
 ▼   ▼    ▼
Native Python operations
```

The user does **not** need to choose between CMD, PowerShell or Bash for supported operations.

---

# Requirements

Before installing Modux, you need:

- Python 3.10 or newer
- Internet connection
- A Groq account
- A Groq API key

Check your Python installation:

```bash
python --version
```

You should see Python 3.10 or newer.

---

# Installation

## Recommended: pipx

`pipx` is recommended because Modux is a command-line application.

### Windows

Install pipx:

```powershell
python -m pip install --user pipx
python -m pipx ensurepath
```

Close and reopen PowerShell after running `ensurepath`.

Then install Modux:

```powershell
pipx install modux
```

### Linux

```bash
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```

Restart your terminal, then:

```bash
pipx install modux
```

### macOS

```bash
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```

Restart your terminal, then:

```bash
pipx install modux
```

---

# Alternative: pip

You can also install Modux directly using pip:

```bash
python -m pip install modux
```

After installation, verify it:

```bash
modux
```

---

# First-Time Setup

After installing Modux, simply run:

```bash
modux
```

If Modux has not been configured, it will automatically ask whether you want to configure it.

You can also explicitly start setup:

```bash
modux setup
```

You will see something similar to:

```text
================================
          MODUX SETUP
================================

Modux requires a Groq API key.

1. Open:
   https://console.groq.com/keys

2. Create a Groq API key.

3. Paste the key below.

Groq API Key:
```

Paste your API key and press Enter.

The API key is not displayed while you type it.

---

# Getting a Groq API Key

You need your own Groq API key to use Modux.

Open:

https://console.groq.com/keys

Then:

1. Sign in to your Groq account.
2. Create a new API key.
3. Copy the key.
4. Run:

```bash
modux setup
```

5. Paste the key when Modux asks for it.

Your API key is stored using the operating system's credential storage through Python Keyring.

**Never publish your API key on GitHub.**

---

# API Key Management

## Configure or change your API key

```bash
modux setup
```

This allows you to add a new key or replace the existing key.

---

## Check configuration

```bash
modux config
```

Example:

```text
Groq API key: configured
```

Modux never displays your actual API key.

---

## Remove your stored API key

```bash
modux logout
```

This removes the API key stored by Modux.

---

# Starting Modux

After installation and setup:

```bash
modux
```

You will see:

```text
================================
          MODUX 0.1.0
================================
Operating System: Windows

Type 'help' for commands.

Modux >
```

---

# Modux Commands

## Exit Modux

```text
Modux > exit
```

---

## Show files

```text
Modux > show my files
```

Modux automatically performs the appropriate operation for your operating system.

---

## Show current directory

```text
Modux > show my current directory
```

---

## Create a directory

```text
Modux > create a folder named projects
```

---

## Create a file

```text
Modux > create a file named hello.txt
```

---

## Delete a file

```text
Modux > delete hello.txt
```

Modux asks for confirmation before performing the operation.

---

## Copy a file

```text
Modux > copy app.py to backup.py
```

---

## Move a file

```text
Modux > move app.py to backup/app.py
```

---

## Check disk space

```text
Modux > check disk space
```

---

## System information

```text
Modux > what operating system am I using
```

---

## Clean temporary files

```text
Modux > clean temporary files
```

Modux uses the appropriate temporary directory for the operating system.

---

## Ping a host

```text
Modux > ping google.com
```

---

## Find an installed program

```text
Modux > where is git installed
```

---

## Open a website

```text
Modux > open https://github.com
```

---

# Code Assistance

Modux can also work with source code.

## Inspect a file

```text
Modux > inspect test.py
```

Modux reads the file and explains:

- What the code does
- Possible problems
- Possible improvements

---

## Fix a file

```text
Modux > fix test.py
```

Modux generates a corrected version of the code and shows it before making changes.

You must explicitly confirm the changes.

```text
Apply these changes? [y/N]:
```

---

## Run a Python file

```text
Modux > run test.py
```

Modux executes the Python program and displays its output.

If the program fails, Modux automatically analyzes the error.

Example:

```text
Program failed.

Error:
ZeroDivisionError: division by zero

Modux Analysis:

The program attempted to divide by zero...
```

---

## Run a Bash script

```text
Modux > run script.sh
```

Bash must be installed and available on the system.

---

# Understand a Project

From inside a project directory:

```text
Modux > understand this project
```

Modux scans the project files and provides an overview of:

- Project structure
- Important files
- What files do
- Technologies detected from the source
- How components connect
- Possible improvements

Generated directories such as:

```text
.git
venv
.venv
__pycache__
node_modules
```

are excluded from project analysis.

---

# Confirmation System

Modux does not silently perform supported system actions.

For example:

```text
Modux > create a folder named test

Action:
CREATE_DIRECTORY

Arguments:
  name: test

Execute this action? [y/N]:
```

You must confirm the action.

Use:

```text
y
```

to execute it.

Use:

```text
n
```

or simply press Enter to cancel it.

---

# Supported Operating Systems

## Windows

Modux automatically detects Windows and uses Windows-compatible behavior internally.

Users do not need to choose CMD or PowerShell.

## Linux

Modux detects Linux and uses Linux-compatible behavior.

## macOS

Modux detects macOS and uses macOS-compatible behavior.

The goal is for the Modux user experience to remain the same across all three platforms.

---

# Security

Modux is designed to avoid exposing operating-system shell syntax to the AI for supported operations.

The AI first identifies the user's intent.

For example:

```text
create a folder named test
```

becomes an internal intent:

```text
CREATE_DIRECTORY
```

Modux then performs that operation itself.

This is safer than blindly executing arbitrary commands generated by an AI model.

### API Keys

Your Groq API key belongs to your own Groq account.

Modux does not provide a shared API key.

Never:

- Put your API key in source code
- Commit your API key to Git
- Upload your API key to GitHub
- Share your API key publicly

Use:

```bash
modux setup
```

to configure your key.

---

# Troubleshooting

## `modux` is not recognized

Try reinstalling:

```bash
python -m pip install modux
```

If using pipx:

```bash
pipx install modux
```

Then restart your terminal.

---

## Modux says the API key is not configured

Run:

```bash
modux setup
```

Then enter your Groq API key.

---

## Check whether the key is configured

Run:

```bash
modux config
```

You should see:

```text
Groq API key: configured
```

---

## Modux cannot connect to Groq

Check:

1. Your internet connection
2. Your Groq account
3. Your API key
4. Whether your Groq API key is still active

Run:

```bash
modux setup
```

to replace the stored key.

---

# Developer Setup

If you want to work on the Modux source code:

Clone the repository:

```bash
git clone https://github.com/krishpatel-acc/modux.git
```

Enter the project:

```bash
cd modux
```

Install in editable mode:

```bash
python -m pip install -e .
```

Install testing tools:

```bash
python -m pip install pytest
```

Run the test suite:

```bash
python -m pytest
```

Expected result:

```text
13 passed
```

---

# Project Structure

```text
modux/
│
├── src/
│   └── modux/
│       ├── __init__.py
│       ├── ai.py
│       ├── cli.py
│       ├── config.py
│       ├── executor.py
│       └── project.py
│
├── tests/
│   └── test_modux.py
│
├── .gitignore
├── LICENSE
├── README.md
└── pyproject.toml
```

---

# Development

Install the project:

```bash
python -m pip install -e .
```

Run Modux:

```bash
modux
```

Run tests:

```bash
python -m pytest
```

Build the package:

```bash
python -m pip install build
python -m build
```

The generated packages will appear inside:

```text
dist/
```

---

# GitHub

Source code:

https://github.com/krishpatel-acc/modux

Modux is open source and welcomes contributions.

---

# License

Modux is released under the MIT License.

See [LICENSE](LICENSE) for the complete license.