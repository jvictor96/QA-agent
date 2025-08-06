# langchain-project

## Prerequisites
- Python 3
- An OpenAI API key

## Running through the CLI

### 1. Clone the project

```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Set Up a Virtual Environment and Install Dependencies

```bash
uv sync
```

### 3. Set up .env file with the API keys from each service

```
OPENAI_API_KEY="sk-proj-hL...8A"
WEATHERSTACK_API_KEY="588...f20"
```

The `OPENAI_API_KEY` is mandatory; others may be optional.

### 4. Run the Chatbot

```bash
python -m langchain_project
```

The chatbot will start in the terminal and prompt you for your OpenAI API key if it's not set in the `.env` file. You can then interact with the chatbot by typing messages. Type `exit` to quit.

## Available Tools

- Dice rolling
- Math operations (square root, power)
- Weather info
- Simple file operations (list, read, append notes)
- Image generation (DALL-E)
- Wikipedia search
- ... and more.
