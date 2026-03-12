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
from reviewer import REVIEW_PROMPT
from tester import TEST_PROMPT
from issuer import ISSUER_PROMPT

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
        temperature=0.1,
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
