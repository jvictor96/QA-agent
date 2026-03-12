import os

GITHUB_REPOSITORY = os.environ.get("GITHUB_REPOSITORY")
ISSUER_PROMPT = f"""
Analyse the issues in {GITHUB_REPOSITORY} and suggest changes to improve the quality of the issues,
mainly focusing on adding suites of edge cases and which expected external behaviors must be asserted for closing the issues. 
"""