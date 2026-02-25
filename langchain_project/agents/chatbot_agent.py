import logging
from langchain.chat_models import init_chat_model
from langchain_community.tools import WikipediaQueryRun
from langchain_community.tools.openai_dalle_image_generation import (
    OpenAIDALLEImageGenerationTool,
)
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from ..tools import (
    run_git_diff_in_other_directory,
    run_git_diff_between_branches_in_other_directory
)


class ChatbotAgent:
    def __init__(
        self,
        model: str = "gpt-4.1-nano",
        logger: logging.Logger = None,
        output_function=print,
    ):
        """
        Initialize the ChatbotAgent.

        Args:
            model: The model to use for the chatbot (as per LangChain's specification)
            logger: The logger to use for standard system logging
            output_function: The function to use for outputting the chatbot's response (default is Python's `print()`)
        """
        if logger is None:
            raise ValueError("Logger cannot be None")
        if output_function is None:
            raise ValueError("Output function cannot be None")
        self.logger = logger
        self.output = output_function
        self.logger.info("Initializing ChatbotAgent with model: %s", model)
        self.model = init_chat_model(model=model)
        self.tools = [
            run_git_diff_in_other_directory,
            run_git_diff_between_branches_in_other_directory
        ]
        self.memory = MemorySaver()
        self.agent_executor = create_react_agent(
            self.model, self.tools, checkpointer=self.memory
        )
        self.logger.debug("ChatbotAgent initialization complete")

    def stream_response(self, user_input: str, config: RunnableConfig):
        """
        Stream the chatbot's response step by step.

        Args:
            user_input: The user's input message
            config: The configuration for the agent execution
        """
        self.logger.debug("Calling agent with input: %s", user_input)
        for step in self.agent_executor.stream(
            {"messages": [user_input]}, config, stream_mode="updates"
        ):
            if step.get("agent"):
                message = step["agent"]["messages"][0]
                if message.content != "":
                    self.logger.info("AI response: %s", message.text())
                    self.output("AI:", message.text())
            if step.get("tools"):
                message = step["tools"]["messages"][0]
                self.logger.debug("Tool %s response: %s", message.name, message.text())
