"""
This is a simple example of how to use the LangChain library to create a chatbot.
Based on documentation found at https://python.langchain.com/docs/integrations/chat/openai/ etc.
"""

import os

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain.messages import HumanMessage
from langchain_project.tools import tools

REASONING_MODEL = os.environ.get("REASONING_MODEL", "gpt-5-mini")
TARGET_BRANCH = os.environ.get("REASONING_MODEL", "main")
PROMPT = """
Evaluate the changes in a repository and generate a report.Follow four steps in the evaluation.
1. If you can't identify any purpose in the changes, such as adding features, improving perfomance or architecture, stop and report it.
2. If the changes have more than one purpose for a single merge, suggest how they can be splited into more merges, each with its own purpuse.
3. If the code seems to fail in implementing its purpose or if it has bugs and compilation errors, stop and repoort.
4. Make a style/architectural report
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
Changes must be tested, every PR must make sure the changes are implemented or the issue fixed.
The answer must highlight problems and possible solutions or missing code design that solves the issue:
1. To use good named method to wrap behaviour instead of manually getting and setting properties
2. To use map, filter and reduce to work with collections instread of using branching and manual aggregation
3. To use polymorphism instead of branching
4. To user linters and automated style checks
"""


def main():
    model = ChatOpenAI(
        model=REASONING_MODEL,
        temperature=0.1,
        max_tokens=1000,
    )
    agent = create_agent(model, tools=tools)
    base_prompt = PROMPT

    parts = [
        base_prompt,
        f"Compare the HEAD with {TARGET_BRANCH}"
    ]

    prompt = "\n".join(parts)
    print("\n\nReview:")
    agent.invoke({"messages": [HumanMessage(prompt)]})

if __name__ == "__main__":
    main()
