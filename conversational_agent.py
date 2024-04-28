from langchain_experimental.chat_models import Llama2Chat
from langchain.memory import ConversationBufferMemory
from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts.chat import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.runnables.history import RunnableWithMessageHistory
import os
import sys
import time
from chat_memory_store import ChatMemoryStore
class ConversationalAgent:
    def __init__(self, model_name="llama3:8b"):
        self.llm = Ollama(model=model_name)
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You're an assistant who's good at answering user tasks",
                ),
                MessagesPlaceholder(variable_name="history"),
                ("human", "{input}"),
            ]
        )
        self.parser = StrOutputParser()
        self.chain = self.prompt | self.llm | self.parser
        self.memory_store = ChatMemoryStore()
        self.with_message_history = RunnableWithMessageHistory(
            self.chain,
            self.memory_store.get_session_history,
            input_messages_key="input",
            history_messages_key="history",
        )

    def chat(self, user_input, conversation_name):
        start_time = time.time()
        response = ""
        checkpoint_file = os.path.join("checkpoints", f"{conversation_name}.checkpoint")
        try:
            result = self.with_message_history.stream(
                {"input": user_input},
                config={"configurable": {"session_id": conversation_name}},
            )
            for chunk in result:
                sys.stdout.write(chunk)
                sys.stdout.flush()
                response += chunk
                # Save the current response as a checkpoint
                os.makedirs(os.path.dirname(checkpoint_file), exist_ok=True)
                with open(checkpoint_file, "w", encoding="utf-8") as file:
                    file.write(response)
            # Remove the checkpoint file after successful completion
            os.remove(checkpoint_file)
        except KeyboardInterrupt:
            print("\nStreaming interrupted. Saving the partial response.")
        end_time = time.time()
        response_time = end_time - start_time
        print()  # Print a new line after streaming the response

        # Update the session history with the latest user input and assistant response
        session_history = self.memory_store.get_session_history(conversation_name)
        session_history.add_user_message(user_input)
        session_history.add_ai_message(response)
        self.memory_store.update_session_history(conversation_name, session_history)

        return response, response_time
# main.py
if __name__ == "__main__":
    agent = ConversationalAgent()
    conversation_name = input("Enter a name for the conversation: ")

    while True:
        user_input = input("Enter your message (or type 'exit' to quit): ")
        if user_input.lower() == "exit":
            break
        response, response_time = agent.chat(user_input, conversation_name)
        print(f"Assistant: {response}")
        print(f"Response time: {response_time:.2f} seconds")