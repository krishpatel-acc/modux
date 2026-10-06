import os


IGNORED_DIRS = {
    ".git",
    ".venv",
    "venv",
    "env",
    "__pycache__",
    "node_modules",
    ".idea",
    ".vscode",
    "build",
    "dist",
}


def read_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()

    except FileNotFoundError:
        return None

    except PermissionError:
        return "PERMISSION_DENIED"

    except UnicodeDecodeError:
        return "BINARY_FILE"


def write_file(filename, content):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(content)

        return True

    except PermissionError:
        return False


def get_project_files():
    files = []

    for root, dirs, filenames in os.walk("."):

        dirs[:] = [
            directory
            for directory in dirs
            if directory not in IGNORED_DIRS
        ]

        for filename in filenames:
            files.append(os.path.join(root, filename))

    return files


def get_project_content():
    project_data = []

    for filename in get_project_files():

        content = read_file(filename)

        if content is None:
            continue

        if content == "PERMISSION_DENIED":
            project_data.append(
                f"\n===== {filename} =====\n[Permission denied]"
            )
            continue

        if content == "BINARY_FILE":
            project_data.append(
                f"\n===== {filename} =====\n[Binary file]"
            )
            continue

        if len(content) > 12000:
            content = content[:12000]
            content += "\n[File truncated]"

        project_data.append(
            f"\n===== {filename} =====\n{content}"
        )

    return "\n".join(project_data)