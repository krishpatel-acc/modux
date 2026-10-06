import os
import platform
import shutil
import subprocess
import sys
import tempfile


BLOCKED_INTENTS = {
    "DELETE_SYSTEM_FILES",
    "FORMAT_DISK",
    "SHUTDOWN_SYSTEM",
    "REBOOT_SYSTEM",
}


def get_os():
    system = platform.system()

    if system == "Windows":
        return "Windows"

    if system == "Darwin":
        return "macOS"

    if system == "Linux":
        return "Linux"

    return system


def execute_intent(intent, arguments=None):
    """
    Execute a safe, platform-independent Modux intent.

    The AI never directly controls the operating-system shell.
    """

    if arguments is None:
        arguments = {}

    if intent in BLOCKED_INTENTS:
        return {
            "success": False,
            "stdout": "",
            "stderr": f"The intent '{intent}' is blocked for safety.",
            "returncode": -1,
        }

    try:
        if intent == "LIST_FILES":
            return list_files()

        if intent == "SHOW_CURRENT_DIRECTORY":
            return show_current_directory()

        if intent == "CREATE_DIRECTORY":
            return create_directory(arguments.get("name"))

        if intent == "CREATE_FILE":
            return create_file(arguments.get("name"))

        if intent == "DELETE_FILE":
            return delete_file(arguments.get("name"))

        if intent == "DELETE_DIRECTORY":
            return delete_directory(arguments.get("name"))

        if intent == "COPY_FILE":
            return copy_file(
                arguments.get("source"),
                arguments.get("destination"),
            )

        if intent == "MOVE_FILE":
            return move_file(
                arguments.get("source"),
                arguments.get("destination"),
            )

        if intent == "DISK_USAGE":
            return disk_usage()

        if intent == "SYSTEM_INFO":
            return system_info()

        if intent == "CLEAR_TEMP":
            return clear_temp()

        if intent == "OPEN_URL":
            return open_url(arguments.get("url"))

        if intent == "PING":
            return ping(arguments.get("host"))

        if intent == "WHICH":
            return find_program(arguments.get("program"))

        if intent == "RUN_COMMAND":
            return run_native_command(
                arguments.get("command")
            )

        return {
            "success": False,
            "stdout": "",
            "stderr": f"Unknown Modux intent: {intent}",
            "returncode": -1,
        }

    except Exception as error:
        return {
            "success": False,
            "stdout": "",
            "stderr": str(error),
            "returncode": -1,
        }


def result(success, stdout="", stderr="", returncode=0):
    return {
        "success": success,
        "stdout": stdout,
        "stderr": stderr,
        "returncode": returncode,
    }


def list_files():
    entries = os.listdir(".")

    if not entries:
        return result(
            True,
            "The current directory is empty.",
        )

    entries.sort()

    lines = []

    for entry in entries:
        full_path = os.path.join(".", entry)

        if os.path.isdir(full_path):
            lines.append(f"[DIR]  {entry}")
        else:
            lines.append(f"[FILE] {entry}")

    return result(
        True,
        "\n".join(lines),
    )


def show_current_directory():
    return result(
        True,
        os.getcwd(),
    )


def create_directory(name):
    if not name:
        return result(
            False,
            stderr="Directory name was not provided.",
            returncode=-1,
        )

    os.makedirs(name, exist_ok=False)

    return result(
        True,
        f"Directory created: {name}",
    )


def create_file(name):
    if not name:
        return result(
            False,
            stderr="File name was not provided.",
            returncode=-1,
        )

    with open(name, "x", encoding="utf-8"):
        pass

    return result(
        True,
        f"File created: {name}",
    )


def delete_file(name):
    if not name:
        return result(
            False,
            stderr="File name was not provided.",
            returncode=-1,
        )

    if os.path.isdir(name):
        return result(
            False,
            stderr=(
                f"'{name}' is a directory. "
                "Use DELETE_DIRECTORY instead."
            ),
            returncode=-1,
        )

    if not os.path.isfile(name):
        return result(
            False,
            stderr=f"File not found: {name}",
            returncode=-1,
        )

    os.remove(name)

    return result(
        True,
        f"File deleted: {name}",
    )


def delete_directory(name):
    if not name:
        return result(
            False,
            stderr="Directory name was not provided.",
            returncode=-1,
        )

    if not os.path.isdir(name):
        return result(
            False,
            stderr=f"Directory not found: {name}",
            returncode=-1,
        )

    shutil.rmtree(name)

    return result(
        True,
        f"Directory deleted: {name}",
    )


def copy_file(source, destination):
    if not source or not destination:
        return result(
            False,
            stderr="Source and destination are required.",
            returncode=-1,
        )

    shutil.copy2(source, destination)

    return result(
        True,
        f"Copied '{source}' to '{destination}'.",
    )


def move_file(source, destination):
    if not source or not destination:
        return result(
            False,
            stderr="Source and destination are required.",
            returncode=-1,
        )

    shutil.move(source, destination)

    return result(
        True,
        f"Moved '{source}' to '{destination}'.",
    )


def disk_usage():
    usage = shutil.disk_usage(os.getcwd())

    total_gb = usage.total / (1024 ** 3)
    used_gb = (usage.total - usage.free) / (1024 ** 3)
    free_gb = usage.free / (1024 ** 3)

    output = (
        f"Total: {total_gb:.2f} GB\n"
        f"Used:  {used_gb:.2f} GB\n"
        f"Free:  {free_gb:.2f} GB"
    )

    return result(True, output)


def system_info():
    output = (
        f"OS: {platform.system()}\n"
        f"OS Version: {platform.version()}\n"
        f"Machine: {platform.machine()}\n"
        f"Python: {platform.python_version()}"
    )

    return result(True, output)


def clear_temp():
    temp_directory = tempfile.gettempdir()

    removed = 0
    failed = 0

    for name in os.listdir(temp_directory):

        path = os.path.join(temp_directory, name)

        try:

            if os.path.isfile(path) or os.path.islink(path):
                os.remove(path)
                removed += 1

            elif os.path.isdir(path):
                shutil.rmtree(path)
                removed += 1

        except (PermissionError, OSError):
            failed += 1

    output = (
        f"Temporary directory: {temp_directory}\n"
        f"Items removed: {removed}\n"
        f"Items skipped: {failed}"
    )

    return result(True, output)


def open_url(url):
    if not url:
        return result(
            False,
            stderr="URL was not provided.",
            returncode=-1,
        )

    if not (
        url.startswith("http://")
        or url.startswith("https://")
    ):
        return result(
            False,
            stderr="Only HTTP and HTTPS URLs are supported.",
            returncode=-1,
        )

    if platform.system() == "Windows":
        os.startfile(url)

    elif platform.system() == "Darwin":
        subprocess.Popen(
            ["open", url],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    else:
        subprocess.Popen(
            ["xdg-open", url],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    return result(
        True,
        f"Opened: {url}",
    )


def ping(host):
    if not host:
        return result(
            False,
            stderr="Host was not provided.",
            returncode=-1,
        )

    if platform.system() == "Windows":
        command = ["ping", "-n", "4", host]
    else:
        command = ["ping", "-c", "4", host]

    process = subprocess.run(
        command,
        capture_output=True,
        text=True,
    )

    return result(
        process.returncode == 0,
        process.stdout,
        process.stderr,
        process.returncode,
    )


def find_program(program):
    if not program:
        return result(
            False,
            stderr="Program name was not provided.",
            returncode=-1,
        )

    path = shutil.which(program)

    if path:
        return result(
            True,
            path,
        )

    return result(
        False,
        stderr=f"Program not found: {program}",
        returncode=1,
    )


def run_native_command(command):
    """
    Escape hatch for commands that are not yet represented
    by a dedicated Modux intent.
    """

    if not command:
        return result(
            False,
            stderr="Command was not provided.",
            returncode=-1,
        )

    system = platform.system()

    if system == "Windows":

        process = subprocess.run(
            [
                "powershell.exe",
                "-NoProfile",
                "-Command",
                command,
            ],
            capture_output=True,
            text=True,
        )

    else:

        process = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
        )

    return result(
        process.returncode == 0,
        process.stdout,
        process.stderr,
        process.returncode,
    )


def run_file(filename):
    if not os.path.isfile(filename):
        return result(
            False,
            stderr="File not found.",
            returncode=-1,
        )

    if filename.endswith(".py"):

        command = [
            sys.executable,
            filename,
        ]

    elif filename.endswith(".sh"):

        if shutil.which("bash") is None:
            return result(
                False,
                stderr=(
                    "Bash is not installed or "
                    "not available in PATH."
                ),
                returncode=-1,
            )

        command = [
            "bash",
            filename,
        ]

    else:

        return result(
            False,
            stderr=(
                "Unsupported file type. "
                "Currently supported: .py and .sh"
            ),
            returncode=-1,
        )

    process = subprocess.run(
        command,
        capture_output=True,
        text=True,
    )

    return result(
        process.returncode == 0,
        process.stdout,
        process.stderr,
        process.returncode,
    )