import os

from modux.executor import (
    execute_intent,
    get_os,
)
from modux.project import (
    read_file,
    write_file,
)


def test_get_os():
    current_os = get_os()

    assert current_os in {
        "Windows",
        "Linux",
        "macOS",
    }


def test_create_directory(tmp_path):
    directory = tmp_path / "test-folder"

    result = execute_intent(
        "CREATE_DIRECTORY",
        {
            "name": str(directory),
        },
    )

    assert result["success"] is True
    assert directory.exists()
    assert directory.is_dir()


def test_create_file(tmp_path):
    filename = tmp_path / "test.txt"

    result = execute_intent(
        "CREATE_FILE",
        {
            "name": str(filename),
        },
    )

    assert result["success"] is True
    assert filename.exists()
    assert filename.is_file()


def test_write_and_read_file(tmp_path):
    filename = tmp_path / "test.txt"

    assert write_file(
        str(filename),
        "Hello Modux",
    )

    content = read_file(
        str(filename),
    )

    assert content == "Hello Modux"


def test_delete_file(tmp_path):
    filename = tmp_path / "delete-me.txt"

    filename.write_text(
        "temporary file",
        encoding="utf-8",
    )

    result = execute_intent(
        "DELETE_FILE",
        {
            "name": str(filename),
        },
    )

    assert result["success"] is True
    assert not filename.exists()


def test_copy_file(tmp_path):
    source = tmp_path / "source.txt"
    destination = tmp_path / "destination.txt"

    source.write_text(
        "Modux",
        encoding="utf-8",
    )

    result = execute_intent(
        "COPY_FILE",
        {
            "source": str(source),
            "destination": str(destination),
        },
    )

    assert result["success"] is True
    assert destination.exists()
    assert destination.read_text(
        encoding="utf-8"
    ) == "Modux"


def test_move_file(tmp_path):
    source = tmp_path / "source.txt"
    destination = tmp_path / "destination.txt"

    source.write_text(
        "Modux",
        encoding="utf-8",
    )

    result = execute_intent(
        "MOVE_FILE",
        {
            "source": str(source),
            "destination": str(destination),
        },
    )

    assert result["success"] is True
    assert not source.exists()
    assert destination.exists()


def test_disk_usage():
    result = execute_intent(
        "DISK_USAGE",
        {},
    )

    assert result["success"] is True
    assert "Total:" in result["stdout"]
    assert "Free:" in result["stdout"]


def test_system_info():
    result = execute_intent(
        "SYSTEM_INFO",
        {},
    )

    assert result["success"] is True
    assert "OS:" in result["stdout"]
    assert "Python:" in result["stdout"]


def test_blocked_intent():
    result = execute_intent(
        "DELETE_SYSTEM_FILES",
        {},
    )

    assert result["success"] is False
    assert "blocked" in result["stderr"].lower()


def test_unknown_intent():
    result = execute_intent(
        "UNKNOWN_INTENT",
        {},
    )

    assert result["success"] is False
    assert "unknown" in result["stderr"].lower()


def test_list_files(tmp_path):
    old_directory = os.getcwd()

    try:
        os.chdir(tmp_path)

        (tmp_path / "file.txt").write_text(
            "hello",
            encoding="utf-8",
        )

        (tmp_path / "folder").mkdir()

        result = execute_intent(
            "LIST_FILES",
            {},
        )

        assert result["success"] is True
        assert "file.txt" in result["stdout"]
        assert "folder" in result["stdout"]

    finally:
        os.chdir(old_directory)


def test_current_directory(tmp_path):
    old_directory = os.getcwd()

    try:
        os.chdir(tmp_path)

        result = execute_intent(
            "SHOW_CURRENT_DIRECTORY",
            {},
        )

        assert result["success"] is True
        assert str(tmp_path) in result["stdout"]

    finally:
        os.chdir(old_directory)