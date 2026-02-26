import os
import subprocess
from langchain_core.tools import tool


@tool
def run_git_diff_between_branches(
    branch: str
) -> str:
    """
    Read the git diff between branches.
    """
    repo_path = os.getenv("GITHUB_WORKSPACE", os.getcwd())
    cmd = ["git", "diff", "-U6"]

    if branch:
        cmd.append(branch)

    try:
        result = subprocess.run(
            cmd,
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Git error: {e.stderr}"
    except Exception as e:
        return f"Error running diff: {str(e)}"
