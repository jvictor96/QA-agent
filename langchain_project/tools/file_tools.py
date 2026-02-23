import subprocess
from langchain_core.tools import tool


@tool
def run_git_diff_in_other_directory(directory: str) -> str:
    """
    Read the git diff from the target directory.

    Args:
            directory: the absolute path to the directory

    Returns:
            The git diff
    """
    try:
        return subprocess.run(f"git -C {directory} diff", capture_output=True, text=True, shell=True)
    except Exception as e:
        return f"Error running diff: {str(e)}"
