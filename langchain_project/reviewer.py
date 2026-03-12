import os

GITHUB_REF = os.environ.get("GITHUB_REF").split("/")[2]
GITHUB_REPOSITORY = os.environ.get("GITHUB_REPOSITORY")
REVIEW_PROMPT = f"""
Evaluate the changes in a repository and generate a short report. Follow four steps in the evaluation.
1. If you can't identify any purpose in the changes, such as adding features, improving perfomance or architecture, stop and report it.
2. If the changes have more than one purpose for a single merge, suggest how they can be splited into more merges, each with its own purpuse.
3. If the code seems to fail in implementing its purpose or if it has bugs and compilation errors, stop and repoort.
4. Make a style/architectural report on violations. No need to report when there're no violation.
For the architectural repoort, use object calisthenics, SOLID and clean architecture to give small suggestions.
The object calisthenics principles are:
1. One level of indentation per method
2. Don't use the ELSE keyword
3. Wrap all primitives and Strings
4. First class collections
5. One dot per line
6. Don't abbreviate
7. Keep all entities small
8. No classes with more than two instance variables
9. No getters/setters/properties
SOLID and Clean Architecture principles are:
1. Domain classes don't know infrastructure, they receive it from a higher level
2. infrastructure don't know business rules
3. I/O code is declares as contracts, handled in the domain as abstractions, and implementations are unknown at the domain
4. The dependency graph must be a DAG and flow from the domain package
5. External dependences shouldn't be imported at the domain package
Evaluate the diff in #{GITHUB_REF}. The owner and repo are {GITHUB_REPOSITORY}. 
Then submit a review recommending changes marking the PR assignee @ at specific lines, using the add comment on line resource. If there are no suggestions, approve the pull request.
"""