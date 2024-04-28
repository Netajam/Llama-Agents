import os
import sys
import json
import time
from datetime import datetime
from simple_agent import SimpleAgent
from conversational_agent import ConversationalAgent

def create_new_conversation(agent):
    # Generate a unique filename based on the current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"conversation_{timestamp}.md"
    
    # Create the conversations directory if it doesn't exist
    os.makedirs("conversations", exist_ok=True)
    
    # Create the new conversation file
    with open(os.path.join("conversations", filename), "w", encoding="utf-8") as file:
        file.write(f"# Conversation {timestamp}\n\n")
    
    # Update the current conversation filename in the config file
    update_config(filename)
    
    return filename

def save_conversation(filename, prompt, response, response_time, interrupted=False):
    with open(os.path.join("conversations", filename), "a", encoding="utf-8") as file:
        file.write(f"## User Prompt:\n{prompt}\n\n")
        if interrupted:
            file.write(f"## Assistant Response (Interrupted, Time: {response_time:.2f} seconds):\n{response}\n\n")
        else:
            file.write(f"## Assistant Response (Time: {response_time:.2f} seconds):\n{response}\n\n")

def load_config():
    if os.path.exists("config.json"):
        with open("config.json", "r") as file:
            return json.load(file)
    return {}

def update_config(filename):
    config = load_config()
    config["current_conversation"] = filename
    with open("config.json", "w") as file:
        json.dump(config, file)

if __name__ == "__main__":
    agent_type = input("Choose the type of agent (simple/conversational): ")

    if agent_type.lower() == "simple":
        agent = SimpleAgent()
    elif agent_type.lower() == "conversational":
        agent = ConversationalAgent()
    else:
        print("Invalid agent type. Exiting.")
        sys.exit(1)

    print(f"Selected agent: {agent_type}")

    continue_conversation = False
    
    if len(sys.argv) > 1 and sys.argv[1] == "-c":
        continue_conversation = True
    
    if continue_conversation:
        config = load_config()
        conversation_file = config.get("current_conversation")
        
        if conversation_file is None or conversation_file == "":
            print("No existing conversation found. Starting a new conversation.")
            conversation_file = create_new_conversation(agent)
        else:
            print(f"Continuing conversation: {conversation_file}")
    else:
        conversation_file = create_new_conversation(agent)
        print(f"New conversation created: {conversation_file}")
    
    while True:
        prompt = input("Enter your prompt (or type 'exit' to quit, 'new' to start a new conversation): ")
        
        if prompt.lower() == "exit":
            break
        elif prompt.lower() == "new":
            conversation_file = create_new_conversation(agent)
            print(f"New conversation created: {conversation_file}")
            
            # Reset the memory of the conversational agent
            if isinstance(agent, ConversationalAgent):
                agent.memory_store.store[conversation_file] = []
            
            continue
        
        response, response_time = agent.chat(prompt, conversation_file)
        
        interrupted = False
        
        if os.path.exists(os.path.join("checkpoints", f"{conversation_file}.checkpoint")):
            interrupted = True
        
        save_conversation(conversation_file, prompt, response, response_time, interrupted)
        print(response)