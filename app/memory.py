# app/memory.py
from langchain_community.llms.ollama import Ollama
from langchain.memory import ConversationSummaryBufferMemory

# Initialize the Language Model and Memory
llm_model = Ollama(model="llama3")
memory = ConversationSummaryBufferMemory(
    llm=llm_model, max_token_limit=2500
)
