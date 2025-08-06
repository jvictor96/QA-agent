import logging
import pytest
from unittest.mock import Mock, patch
from langchain_project.agents.chatbot_agent import ChatbotAgent
from langchain_core.runnables import RunnableConfig


@pytest.mark.usefixtures("patch_openai_api_key")
class TestChatbotAgent:
    @pytest.fixture(autouse=True)
    def patch_openai_api_key(self):
        with patch.dict("os.environ", {"OPENAI_API_KEY": "dummy-api-key-for-testing"}):
            yield

    @pytest.fixture(autouse=True)
    def set_caplog_level(self, caplog):
        caplog.set_level(logging.DEBUG)
        yield

    @pytest.fixture
    def mock_output(self):
        return Mock()

    @pytest.fixture
    def agent(self, mock_output):
        with patch(
            "langchain_project.agents.chatbot_agent.create_react_agent"
        ) as mock_create_agent:
            mock_agent_executor = Mock()
            mock_create_agent.return_value = mock_agent_executor
            return ChatbotAgent(
                model="gpt-4.1-nano",
                logger=logging.getLogger("test"),
                output_function=mock_output,
            )

    def test_init_with_valid_params(self, caplog):
        with patch(
            "langchain_project.agents.chatbot_agent.create_react_agent"
        ) as mock_create_agent:
            mock_agent_executor = Mock()
            mock_create_agent.return_value = mock_agent_executor
            agent = ChatbotAgent(model="gpt-4.1-nano", logger=logging.getLogger("test"))
            assert agent.logger is not None
            assert len(agent.tools) > 0
            assert agent.output == print
            assert "ChatbotAgent initialization complete" in caplog.text

    def test_init_fails_with_none_logger(self):
        with pytest.raises(ValueError, match="Logger cannot be None"):
            ChatbotAgent(model="gpt-4.1-nano", logger=None)

    def test_init_fails_with_none_output_function(self):
        with pytest.raises(ValueError, match="Output function cannot be None"):
            ChatbotAgent(
                model="gpt-4.1-nano",
                logger=logging.getLogger("test"),
                output_function=None,
            )

    def test_tools_list_contains_expected_tools(self, agent):
        assert hasattr(agent, "tools")
        assert isinstance(agent.tools, list)
        assert len(agent.tools) >= 7

    def test_stream_response(self, agent, mock_output, caplog):
        mock_agent_message = Mock()
        mock_agent_message.content = "This is an AI response"
        mock_agent_message.text.return_value = "This is an AI response"
        mock_tool_message = Mock()
        mock_tool_message.name = "test_tool"
        mock_tool_message.text.return_value = "Tool response"
        mock_steps = [
            {"agent": {"messages": [mock_agent_message]}},
            {"tools": {"messages": [mock_tool_message]}},
        ]
        agent.agent_executor.stream.return_value = mock_steps
        config: RunnableConfig = {"configurable": {"thread_id": "99999999"}}
        agent.stream_response("This is a test message", config)
        mock_output.assert_called_once_with("AI:", "This is an AI response")
        assert "Calling agent with input: This is a test message" in caplog.text
        assert "AI response: This is an AI response" in caplog.text
        assert "Tool test_tool response: Tool response" in caplog.text
