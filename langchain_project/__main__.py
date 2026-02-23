"""
This is a simple example of how to use the LangChain library to create a chatbot.
Based on documentation found at https://python.langchain.com/docs/integrations/chat/openai/ etc.
"""

import argparse
import logging
import os

from dotenv import load_dotenv
from langchain_core.runnables import RunnableConfig
from .agents.chatbot_agent import ChatbotAgent

CHATBOT_MODEL = "gpt-5-mini"


def main():
    args = _parse_args()
    _setup_logging(debug=args.debug)
    logger = logging.getLogger("chatbot")
    load_dotenv()
    if not os.environ.get("OPENAI_API_KEY"):
        message = "OPENAI_API_KEY not found in environment. Please set it before running this program."
        logger.error(message)
        print("Error: " + message, flush=True)
        exit(1)
    logger.info("Initializing chatbot with model: %s", CHATBOT_MODEL)
    chatbot = ChatbotAgent(model=CHATBOT_MODEL, logger=logger)
    config: RunnableConfig = {"configurable": {"thread_id": "1"}}
    user_input = input("Absolute path of git project: ")
    base_prompt = ""
    with open("system_prompt.txt") as f:
        base_prompt = f.read()
    base_prompt += "\nAbsolute path to the git folder: f{user_input}"
    chatbot.stream_response(user_input, config)


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    return parser.parse_args()


def _setup_logging(debug=False):
    level = logging.DEBUG if debug else logging.WARNING
    logging.basicConfig(
        filename="chatbot.log",
        format="%(asctime)s [%(levelname)s] %(module)s: %(message)s",
        level=level,
    )


if __name__ == "__main__":
    main()
