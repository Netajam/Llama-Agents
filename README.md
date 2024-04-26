# Llama-Agents

This repository aims to create a collection of LLaMA 3 agents using LangChain. The ultimate goal is to develop a suite of agents that can be used for various tasks and have access to different tools. The LLM will be self-hosted.

**Agents Developed:**

0. **Simple Agent**: Simple Llama 3 agent accessible from the command line with answers recorded in markdown files.
1. **Conversational Agent**: A conversational agent that can engage with users in natural language, answering questions and providing helpful responses and saving the conversations in files when requested.
2. **Orchestrator Agent**: An orchestration agent that can manage multiple tasks and workflows, streamlining processes and automating repetitive tasks.
3. **RAG (Rule-based Action Generator) Agent**: A rule-based agent that can generate actions based on predefined rules and conditions.

**Features:**

* Generate LLaMA 3 agents using LangChain
* Develop a conversational agent for customer service or technical support
* Create an orchestrator agent to manage workflows and automate tasks
* Design RAGs to generate actions based on rules and conditions
* Interact with system files and integrate with other systems

**Getting Started:**

1. Clone this repository to your local machine.
2. Install the required dependencies, including Ollama, Llama3, and Python.
3. Run the `main.py` script to interact with the Simple Agent.

**Using the Simple Agent (`main.py`):**

1. Open a terminal and navigate to the project directory.
2. Run the following command to start a new conversation:
   ```
   python main.py
   ```
   This will create a new conversation file in the `conversations` directory with the current timestamp.

3. To continue an existing conversation, run the following command:
   ```
   python main.py -c
   ```
   This will load the conversation from the last used conversation file.

4. Enter your prompt or question when prompted. The agent will process your input and generate a response, which will be displayed in the terminal and saved to the conversation file.

5. To start a new conversation at any point, type `new` and press Enter. This will create a new conversation file and switch to it.

6. To exit the program, type `exit` and press Enter.

**Conversation Files:**

The conversations are saved in markdown format in the `conversations` directory. Each conversation is stored in a separate file named `conversation_<timestamp>.md`.

The conversation files contain the user prompts and the assistant's responses, along with the response time. If a response is interrupted due to early stoppage, it will be marked as "Interrupted" in the conversation file.

**Note:**

- The Simple Agent uses the LLaMA 3 model, which needs to be set up and configured separately.
- Make sure to have the necessary dependencies installed before running the script.
- The conversation files are encoded in UTF-8 to ensure proper display of special characters.

... 

[1] LangChain documentation: <https://docs.langchain.com/>
[2] LLaMA 3 documentation: <https://www.llama3.ai/docs/>