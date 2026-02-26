"""
This is a simple example of how to use the LangChain library to create a chatbot.
Based on documentation found at https://python.langchain.com/docs/integrations/chat/openai/ etc.
"""

import os

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain.messages import HumanMessage
from tools import tools

REASONING_MODEL = os.environ.get("REASONING_MODEL", "gpt-5-mini")
TARGET_BRANCH = os.environ.get("REASONING_MODEL", "main")

def main():
    model = ChatOpenAI(
        model=REASONING_MODEL,
        temperature=0.1,
        max_tokens=1000,
    )
    agent = create_agent(model, tools=tools)
    base_prompt = ""
    with open("system_prompt.txt") as f:
        base_prompt = f.read()

    parts = [
        base_prompt,
        f"Compare the HEAD with {TARGET_BRANCH}"
    ]

    prompt = "\n".join(parts)
    print("\n\nReview:")
    agent.invoke({"messages": [HumanMessage(prompt)]})

