import os
import sys
import json
import time
from datetime import datetime
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate

# Load the LLaMA3 model
llm = Ollama(model="llama3:8b")

def call_llma(prompt, conversation_file):
    start_time = time.time()
    response = ""
    checkpoint_file = os.path.join("checkpoints", f"{conversation_file}.checkpoint")
    
    try:
        for chunk in llm.stream(prompt, stop=["<|eot_id|>"]):
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
    
    return response, response_time

def create_new_conversation():
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
    continue_conversation = False
    
    if len(sys.argv) > 1 and sys.argv[1] == "-c":
        continue_conversation = True
    
    if continue_conversation:
        config = load_config()
        conversation_file = config.get("current_conversation")
        
        if conversation_file is None or conversation_file == "":
            print("No existing conversation found. Starting a new conversation.")
            conversation_file = create_new_conversation()
        else:
            print(f"Continuing conversation: {conversation_file}")
    else:
        conversation_file = create_new_conversation()
        print(f"New conversation created: {conversation_file}")
    
    while True:
        prompt = input("Enter your prompt (or type 'exit' to quit, 'new' to start a new conversation): ")
        
        if prompt.lower() == "exit":
            break
        elif prompt.lower() == "new":
            conversation_file = create_new_conversation()
            print(f"New conversation created: {conversation_file}")
            continue
        
        response, response_time = call_llma(prompt, conversation_file)
        interrupted = False
        
        if os.path.exists(os.path.join("checkpoints", f"{conversation_file}.checkpoint")):
            interrupted = True
        
        save_conversation(conversation_file, prompt, response, response_time, interrupted)