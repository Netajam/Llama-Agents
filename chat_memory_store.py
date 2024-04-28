# chat_memory_store.py
import json
import os
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.chat_message_histories import ChatMessageHistory

class ChatMemoryStore:
    def __init__(self, store_file="chat_memory/store.json"):
        self.store_file = store_file
        self.store = self.load_store()

    def load_store(self):
        if os.path.exists(self.store_file):
            with open(self.store_file, "r") as file:
                data = json.load(file)
                return {
                    k: [self.deserialize_message(msg) for msg in v]
                    for k, v in data.items()
                }
        return {}

    def save_store(self):
        serialized_data = {
            k: [self.serialize_message(msg) for msg in v]
            for k, v in self.store.items()
        }
        with open(self.store_file, "w") as file:
            json.dump(serialized_data, file)

    def get_session_history(self, session_id: str) -> ChatMessageHistory:
        if session_id not in self.store:
            self.store[session_id] = []
        return ChatMessageHistory(messages=self.store[session_id])

    def update_session_history(self, session_id: str, history: ChatMessageHistory):
        self.store[session_id] = history.messages
        self.save_store()

    @staticmethod
    def serialize_message(message):
        return {"type": message.__class__.__name__, "data": message.dict()}

    @staticmethod
    def deserialize_message(message_data):
        message_type = message_data["type"]
        if message_type == "HumanMessage":
            return HumanMessage(**message_data["data"])
        elif message_type == "AIMessage":
            return AIMessage(**message_data["data"])
        else:
            raise ValueError(f"Unknown message type: {message_type}")
        
if __name__ == "__main__":
    # Test case
    store_file = "chat_memory/test_store.json"
    memory_store = ChatMemoryStore(store_file)

    # Create test messages
    human_message = HumanMessage(content="Hello, how are you?")
    ai_message = AIMessage(content="I'm doing well, thank you!")

    # Create a test conversation
    session_id = "test_conversation"
    memory_store.update_session_history(
        session_id, ChatMessageHistory(messages=[human_message, ai_message])
    )

    # Retrieve the session history
    session_history = memory_store.get_session_history(session_id)

    # Print the retrieved messages
    print("Retrieved messages:")
    for message in session_history.messages:
        print(f"Type: {message.__class__.__name__}, Content: {message.content}")

    # Load the stored data from the JSON file
    with open(store_file, "r") as file:
        stored_data = json.load(file)

    # Print the stored data
    print("\nStored data:")
    print(json.dumps(stored_data, indent=2))

    # Clean up the test store file
    #os.remove(store_file)