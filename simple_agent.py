from langchain_community.llms import Ollama
import os
import sys
import time

class SimpleAgent:
    def __init__(self, model_name="llama3:8b"):
        self.llm = Ollama(model=model_name)

    def chat(self, prompt, conversation_file):
        start_time = time.time()
        response = ""
        checkpoint_file = os.path.join("checkpoints", f"{conversation_file}.checkpoint")

        try:
            for chunk in self.llm.stream(prompt, stop=["<|eot_id|>"]):
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