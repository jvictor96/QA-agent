import os
from datetime import datetime
from langchain_core.tools import tool


@tool
def list_local_text_files() -> str:
    """
    List all text files in the target directory. Use this first to see what files are available before reading or writing to them.

    Returns:
            A string listing all .txt files in the target directory
    """
    try:
        target_dir = _get_target_dir()
        _create_target_dir_if_not_exists()
        txt_files = [f for f in os.listdir(target_dir) if f.endswith(".txt")]
        if not txt_files:
            return "No text files found in target directory."
        result = "Available text files in target directory:\n"
        for i, filename in enumerate(txt_files, 1):
            file_path = os.path.join(target_dir, filename)
            size = os.path.getsize(file_path)
            result += f"{i}. {filename} ({size} bytes)\n"
        return result
    except Exception as e:
        return f"Error listing files: {str(e)}"


@tool
def read_local_text_file(filename: str) -> str:
    """
    Read the contents of a text file from the target directory.

    Args:
            filename: The name of the file to read (e.g., "assuntos.txt", "notes.txt")

    Returns:
            The contents of the file
    """
    filename = _ensure_txt_extension(filename)
    try:
        target_dir = _get_target_dir()
        file_path = os.path.join(target_dir, filename)
        if not os.path.exists(file_path):
            return f"Error: File '{filename}' not found in target directory."
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        if not content.strip():
            return f"File '{filename}' is empty."
        return f"Contents of {filename}:\n\n{content}"
    except Exception as e:
        return f"Error reading file: {str(e)}"


@tool
def append_note_to_text_file(filename: str, note: str) -> str:
    """
    Append a note with timestamp to a text file in the target directory.

    Args:
            filename: The name of the file to append to (e.g., "topics.txt", "notes.txt")
            note: The note to append (the LLM should provide a brief one-line summary)

    Returns:
            A string confirming the note was saved
    """
    try:
        filename = _ensure_txt_extension(filename)
        target_dir = _get_target_dir()
        _create_target_dir_if_not_exists()
        file_path = os.path.join(target_dir, filename)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_note = f"[{timestamp}] {note.strip()}"
        with open(file_path, "a", encoding="utf-8") as file:
            file.write(formatted_note + "\n")
        return f"Note appended successfully to {filename}: {formatted_note}"
    except Exception as e:
        return f"Error appending note: {str(e)}"


def _get_target_dir() -> str:
    target_dir = os.getenv("FILE_TOOLS_TARGET_DIR")
    if not target_dir:
        raise ValueError(
            "FILE_TOOLS_TARGET_DIR environment variable is not set. "
            "Please set this variable to specify the target directory for file operations."
        )
    return target_dir


def _ensure_txt_extension(filename: str) -> str:
    # ensures filenames have a '.txt' extension (to help agents)
    if not filename.endswith(".txt"):
        return filename + ".txt"
    return filename


def _create_target_dir_if_not_exists():
    target_dir = _get_target_dir()
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
