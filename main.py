from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate

# Load the LLaMA3 model
llm  = Ollama(model="llama3:8b")

def call_llma(prompt):
  
    #for chunks in llm.stream(prompt, stop=["<|eot_id|>"]):
      #  print(chunks)
    try:
        # Use the invoke method to get a response, handling the stop condition
            response = llm.invoke(prompt, stop=["<|eot_id|>"])
            return response
    except Exception as e:
        print("An error occurred:", e)
        return None
    

# Example usage:
prompt = "What is the capital of France?"
response = call_llma(prompt)
print(response)