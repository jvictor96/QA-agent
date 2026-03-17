"""
This is a simple example of how to use the LangChain library to create a chatbot.
Based on documentation found at https://python.langchain.com/docs/integrations/chat/openai/ etc.
"""

import asyncio
import os

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain.messages import HumanMessage
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools

GITHUB_REF = os.environ.get("GITHUB_REF").split("/")[2]
GITHUB_REPOSITORY = os.environ.get("GITHUB_REPOSITORY")
REVIEW_PROMPT = f"""
Evaluate the changes in a repository and generate a short report. Follow four steps in the evaluation.
1. If you can't identify any purpose in the changes, such as adding features, improving performance or architecture, stop and report it.
2. If the changes have more than one purpose for a single merge, suggest how they can be split into more merges, each with its own purpose.
3. If the code seems to fail in implementing its purpose or if it has bugs and compilation errors, stop and report.
4. Make a style/architectural report on violations. No need to report when there are no violations.
For the architectural report, use object callisthenics, SOLID and clean architecture to give small suggestions.
The object callisthenics principles are:
1. Wrap all primitives and Strings
2. One dot per line
3. Don't abbreviate
4. Keep all entities small
SOLID and Clean Architecture principles are:
1. Domain classes don't know infrastructure; they receive it from a higher level
2. Infrastructure doesn't know business rules
3. I/O code is declared as contracts, handled in the domain as abstractions, and implementations are unknown at the domain
4. The dependency graph must be a DAG and flow from the domain package
5. External dependencies shouldn't be imported at the domain package
Evaluate the diff in #{GITHUB_REF}. The owner and repo are {GITHUB_REPOSITORY}.
Be assertive and avoid redundant outputs. Stop getting information about the code as soon as some reviews can be made. Don't dig the code more than necessary.
Decision rule:
- If the tool will significantly improve correctness → use it.
- If the tool only slightly improves the answer → do NOT use it.
- Prefer answering directly when confident.
Then submit a review recommending changes, marking the PR assignee @ in comments. Use small comments instead of a single report. Use one comment per issue found at the diff.
Please pay attention to the API parameters when using tools, as even small misuses can cause your job to fail. Fill every argument accordingly, respecting pre-established options when necessary..
"""

TEST_PROMPT = f"""
Analyse actions and tests in {GITHUB_REPOSITORY} and generate issues to improve test coverage and CI configuration.
Tests must include edge cases and boundary conditions and contain assertions to verify expected behavior,
so issues must be created both to implement tests to cover untested code and improve existing test suites with additional tests.
Issues must be created with a title and a description. 
The title should be a short summary of the issue, while the description should provide a list of changes to improve test coverage and CI configuration.
CI code must be such that it runs all unit tests and exits with a failure status code when a test fails or the coverage doesn't reach a given threshold.
Black box testing is also a requirement for the automated test suite, so issues must be created to implement it when it's not present.
Black box tests must assert expected behavior based on the specification of the code, without relying on its implementation details.
Other tools such as static analysis, check style, linters and vulnerability scanners must be used in every CI run to identify potential issues in the codebase.
Such tools might be suggested in the issues when they're not present in the CI configuration.
"""

ISSUER_PROMPT = f"""
Analyse the issues in {GITHUB_REPOSITORY} and suggest changes to improve the quality of the issues,
mainly focusing on adding suites of edge cases and which expected external behaviors must be asserted for closing the issues. 
"""

REASONING_MODEL = os.environ.get("REASONING_MODEL", "gpt-5-mini")
MODE = os.environ.get("MODE", "review")

PROMPT = {
    "review": REVIEW_PROMPT,
    "issue_checker": ISSUER_PROMPT,
    "test_analysis": TEST_PROMPT,
}[MODE]

TOOLS = {
    "review": "pull_requests",
    "issue_checker": "issues",
    "test_analysis": "actions,issues,repos",
}[MODE]

def main():
    asyncio.run(call_agent())

async def call_agent():
    model = ChatOpenAI(
        model=REASONING_MODEL,
        temperature=0,
    )
    server_params = StdioServerParameters(
        command="./github-mcp-server",
        args=["--toolsets", TOOLS, "stdio"],
        env={
            **os.environ,
        }
    )
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)

            agent = create_agent(model, tools=tools)
            print("\n\nReview:")
            result = await agent.ainvoke({"messages": [HumanMessage(PROMPT)]})
            print(result)
