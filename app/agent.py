from langchain_groq import ChatGroq

import os
from langchain.agents import AgentType, initialize_agent
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.tools import tool
from langchain.agents import AgentExecutor
from langchain.memory import ConversationBufferMemory


# Initialize an LLM model supported by Groq
llm = ChatGroq(model_name="llama3-8b-8192")

# Define custom tools using the @tool decorator
@tool
def calculate_square(number: str) -> str:
    """Calculates the square of a given number."""
    try:
        num = int(number)
        return f"The square of {num} is: {num ** 2}"
    except ValueError:
        return "Please enter a valid number."

@tool
def reverse_text(text: str) -> str:
    """Reverses the given text."""
    return text[::-1]

custom_tools = [calculate_square, reverse_text]

# Add memory
memory = ConversationBufferMemory(memory_key="chat_history")

# Initialize the agent
agent = initialize_agent(
    tools=custom_tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    memory=memory
)

# Run the agent
prompt = input("prompt giriniz..")
response = agent.run(prompt)
print(response)

# Memory içinde saklanan geçmiş konuşmaları görmek için
print(memory.chat_memory.messages)
