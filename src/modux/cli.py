import json
import platform

from .ai import ModuxAI
from .config import (
    delete_api_key,
    get_api_key,
    setup_api_key,
)
from .executor import (
    execute_intent,
    get_os,
    run_file,
)
from .project import (
    get_project_content,
    read_file,
    write_file,
)


INTENT_SYSTEM_PROMPT = """
You are the intent engine for Modux, a cross-platform AI terminal assistant.

The current operating system is:

{os_name}

Do NOT generate shell commands for normal operating-system tasks.

Instead classify the user's request into one of these intents:

LIST_FILES
SHOW_CURRENT_DIRECTORY
CREATE_DIRECTORY
CREATE_FILE
DELETE_FILE
DELETE_DIRECTORY
COPY_FILE
MOVE_FILE
DISK_USAGE
SYSTEM_INFO
CLEAR_TEMP
OPEN_URL
PING
WHICH
CHAT

Return ONLY valid JSON.

Examples:

User:
show my files

Response:
{{"type":"intent","intent":"LIST_FILES","arguments":{{}}}}

User:
show the current directory

Response:
{{"type":"intent","intent":"SHOW_CURRENT_DIRECTORY","arguments":{{}}}}

User:
create a folder named test

Response:
{{"type":"intent","intent":"CREATE_DIRECTORY","arguments":{{"name":"test"}}}}

User:
create a file named hello.txt

Response:
{{"type":"intent","intent":"CREATE_FILE","arguments":{{"name":"hello.txt"}}}}

User:
delete test.txt

Response:
{{"type":"intent","intent":"DELETE_FILE","arguments":{{"name":"test.txt"}}}}

User:
delete the folder test

Response:
{{"type":"intent","intent":"DELETE_DIRECTORY","arguments":{{"name":"test"}}}}

User:
remove directory test

Response:
{{"type":"intent","intent":"DELETE_DIRECTORY","arguments":{{"name":"test"}}}}

User:
remove the folder named project

Response:
{{"type":"intent","intent":"DELETE_DIRECTORY","arguments":{{"name":"project"}}}}

User:
copy a.txt to backup.txt

Response:
{{"type":"intent","intent":"COPY_FILE","arguments":{{"source":"a.txt","destination":"backup.txt"}}}}

User:
move a.txt to backup/a.txt

Response:
{{"type":"intent","intent":"MOVE_FILE","arguments":{{"source":"a.txt","destination":"backup/a.txt"}}}}

User:
check disk space

Response:
{{"type":"intent","intent":"DISK_USAGE","arguments":{{}}}}

User:
what operating system am I using

Response:
{{"type":"intent","intent":"SYSTEM_INFO","arguments":{{}}}}

User:
clean temporary files

Response:
{{"type":"intent","intent":"CLEAR_TEMP","arguments":{{}}}}

User:
open https://github.com

Response:
{{"type":"intent","intent":"OPEN_URL","arguments":{{"url":"https://github.com"}}}}

User:
ping google.com

Response:
{{"type":"intent","intent":"PING","arguments":{{"host":"google.com"}}}}

User:
where is git installed

Response:
{{"type":"intent","intent":"WHICH","arguments":{{"program":"git"}}}}

For normal questions:

{{"type":"chat"}}

Important rules:

- Return ONLY valid JSON.
- Do not include markdown.
- Do not include explanations outside the JSON.
- Do not generate shell commands.
- Do not invent intents.
- Use DELETE_FILE only for files.
- Use DELETE_DIRECTORY only for directories.
"""


CHAT_SYSTEM_PROMPT = """
You are Modux, a helpful AI terminal assistant.

Answer the user's question clearly and practically.

The user's operating system is:

{os_name}

Do not pretend to have performed an action unless
Modux actually performed it.
"""


def analyze_error(
    ai,
    filename,
    error,
):
    return ai.chat(
        """
You are a coding debugging assistant.

Analyze the program error.

Explain:

1. What caused the error
2. Where the error occurred
3. How to fix it

Only make claims supported by the error.

Keep the explanation practical and concise.
""",
        f"""
File: {filename}

Program error:

{error}
""",
    )


def inspect_file(
    ai,
    filename,
):
    content = read_file(filename)

    if content is None:
        print("\nFile not found.")
        return

    if content == "PERMISSION_DENIED":
        print("\nPermission denied.")
        return

    if content == "BINARY_FILE":
        print("\nThis appears to be a binary file.")
        return

    response = ai.chat(
        """
You are a coding assistant.

Analyze the provided source code.

Explain:

1. What the code does
2. Possible errors
3. Improvements

Only make claims supported by the code.

Keep the explanation practical and concise.
""",
        f"File: {filename}\n\n{content}",
    )

    print("\n" + response)


def clean_ai_code(code):
    code = code.strip()

    if code.startswith("```"):
        lines = code.splitlines()

        if lines and lines[0].startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        code = "\n".join(lines)

    return code.strip()


def fix_file(
    ai,
    filename,
):
    content = read_file(filename)

    if content is None:
        print("\nFile not found.")
        return

    if content == "PERMISSION_DENIED":
        print("\nPermission denied.")
        return

    if content == "BINARY_FILE":
        print("\nThis appears to be a binary file.")
        return

    fixed_code = ai.chat(
        """
You are a coding assistant.

Fix the provided source code.

Return ONLY the complete corrected source code.

Do not provide explanations.
Do not use markdown code fences.
""",
        f"File: {filename}\n\n{content}",
    )

    fixed_code = clean_ai_code(fixed_code)

    print("\nProposed corrected code:\n")
    print(fixed_code)

    confirm = input(
        "\nApply these changes? [y/N]: "
    )

    if confirm.lower() == "y":
        if write_file(filename, fixed_code):
            print("\nFile updated successfully.")
        else:
            print(
                "\nPermission denied. "
                "File was not changed."
            )
    else:
        print("\nChanges cancelled.")


def understand_project(ai):
    print("\nScanning project...")

    project_content = get_project_content()

    if not project_content:
        print("\nNo readable project files found.")
        return

    response = ai.chat(
        """
You are Modux, a software project analysis assistant.

You are given the ACTUAL files and contents from
the current project directory.

Analyze ONLY the information provided.

Do NOT guess technologies, files, libraries,
frameworks, or project purposes.

Explain:

1. Project type
2. Important files
3. What each important file does
4. Technologies actually detected
5. How the components connect
6. Possible improvements

If something cannot be determined from the files,
say:

"Not determined from the available files."

Be practical and concise.
""",
        project_content,
    )

    print("\n" + response)


def run_file_command(ai, filename):
    print(f"\nRunning: {filename}")

    confirm = input("\nRun this file? [y/N]: ")

    if confirm.lower() != "y":
        print("Execution cancelled.")
        return

    result = run_file(filename)

    if result["stdout"]:
        print("\nOutput:")
        print(result["stdout"])

    if result["success"]:
        return

    print("\nProgram failed.")

    if result["stderr"]:
        print("\nError:")
        print(result["stderr"])

        print("\nModux Analysis:")

        analysis = analyze_error(
            ai,
            filename,
            result["stderr"],
        )

        print(analysis)


def execute_intent_with_confirmation(
    intent,
    arguments,
):
    print("\nAction:")
    print(intent)

    if arguments:
        print("Arguments:")

        for key, value in arguments.items():
            print(f"  {key}: {value}")

    confirm = input(
        "\nExecute this action? [y/N]: "
    )

    if confirm.lower() != "y":
        print("Action cancelled.")
        return

    result = execute_intent(
        intent,
        arguments,
    )

    if result["stdout"]:
        print("\nOutput:")
        print(result["stdout"])

    if result["stderr"]:
        print("\nError:")
        print(result["stderr"])


def parse_intent(
    ai,
    question,
):
    response = ai.chat(
        INTENT_SYSTEM_PROMPT.format(
            os_name=get_os(),
        ),
        question,
    )

    return response


def setup():
    if setup_api_key():
        print("Modux setup completed.")
    else:
        print("Modux setup was not completed.")


def show_config():
    if get_api_key():
        print("\nGroq API key: configured")
    else:
        print("\nGroq API key: not configured")


def show_help():
    print(
        """
================================
          MODUX HELP
================================

General commands:

  help
      Show this help message.

  exit
      Exit Modux.

Configuration:

  setup
      Configure or replace your Groq API key.

  config
      Check whether a Groq API key is configured.

  logout
      Remove the stored Groq API key.

Project commands:

  understand this project
      Analyze the current project.

  inspect <file>
      Analyze a source file.

  fix <file>
      Ask Modux to fix a source file.

  run <file>
      Run a supported source file.

Natural language commands:

  show my files
  show the current directory
  create a folder named test
  create a file named hello.txt
  delete hello.txt
  delete the folder test
  copy a.txt to backup.txt
  move a.txt to backup/a.txt
  check disk space
  what operating system am I using
  clean temporary files
  ping google.com
  where is git installed
  open https://github.com

All system actions require confirmation before execution.
"""
    )


def handle_question(
    ai,
    question,
):
    lowered = question.lower().strip()

    if not lowered:
        return True

    if lowered == "exit":
        return False

    if lowered == "help":
        show_help()
        return True

    if lowered == "setup":
        setup()
        return True

    if lowered == "config":
        show_config()
        return True

    if lowered == "logout":
        if delete_api_key():
            print("\nStored Groq API key removed.")
        else:
            print("\nNo stored API key was removed.")
        return True

    if lowered == "understand this project":
        understand_project(ai)
        return True

    if lowered.startswith("inspect "):
        filename = question[8:].strip()
        inspect_file(ai, filename)
        return True

    if lowered.startswith("fix "):
        filename = question[4:].strip()
        fix_file(ai, filename)
        return True

    if lowered.startswith("run "):
        filename = question[4:].strip()
        run_file_command(ai, filename)
        return True

    response = parse_intent(
        ai,
        question,
    )

    try:
        data = json.loads(response)
    except json.JSONDecodeError:
        print("\nModux:")
        print(response)
        return True

    if data.get("type") == "chat":
        response = ai.chat(
            CHAT_SYSTEM_PROMPT.format(
                os_name=get_os(),
            ),
            question,
        )

        print("\n" + response)
        return True

    if data.get("type") == "intent":
        intent = data.get("intent")
        arguments = data.get("arguments", {})

        execute_intent_with_confirmation(
            intent,
            arguments,
        )

        return True

    print("\nModux could not understand the request.")
    return True


def main():
    print("================================")
    print("          MODUX 0.1.0")
    print("================================")
    print(
        f"Operating System: "
        f"{platform.system()}"
    )

    if not get_api_key():
        print()
        print("Modux has not been configured yet.")

        answer = input(
            "\nWould you like to configure "
            "Modux now? [Y/n]: "
        )

        if answer.lower() != "n":
            if not setup_api_key():
                print(
                    "\nModux cannot start without "
                    "a Groq API key."
                )
                print(
                    "\nRun 'modux setup' later "
                    "to configure it."
                )
                return
        else:
            print(
                "\nRun 'modux setup' when you "
                "are ready to configure Modux."
            )
            return

    try:
        ai = ModuxAI()
    except RuntimeError as error:
        print(f"\nError:\n{error}")
        return

    print("\nType 'help' for commands.")

    while True:
        try:
            question = input("\nModux > ")
        except KeyboardInterrupt:
            print("\n")
            break
        except EOFError:
            print("\n")
            break

        if not handle_question(ai, question):
            break


if __name__ == "__main__":
    main()