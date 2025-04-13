from langchain_core.messages import HumanMessage
from langchain.chat_models import init_chat_model
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools.retriever import create_retriever_tool
from langchain import hub
from langchain.agents import create_tool_calling_agent
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_core.prompts.chat import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate, MessagesPlaceholder
import requests
import http.client
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@tool
def get_youtube_link_according_to_the_song(song: str) -> str:
    """
    Retrieves the YouTube link for a given song name by searching it on YouTube.

    Parameters:
    - song (str): The name of the song or artist to search for on YouTube.

    Returns:
    - str: The URL of the first video result on YouTube for the given song name.

    Example:

    Note:
    - This tool is useful for returning a YouTube video link that best matches the input song title.
    - It assumes that the first result in the YouTube search is the most relevant.
    - If YouTube API is not used, scraping logic is applied instead.
    """
    from youtube_search import YoutubeSearch
    import webbrowser

    results = YoutubeSearch(f'{song}', max_results=1).to_dict()

    if not results:
        return "No video found for the given song."

    video_id = results[0]["id"]
    link = f"https://www.youtube.com/watch?v={video_id}"
    webbrowser.open(link)
    
    return link





tools = [get_youtube_link_according_to_the_song]
model = init_chat_model("llama-3.3-70b-versatile", model_provider="groq") # llama3-8b-8192


prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(
        "You are a helpful assistant that can use tools to answer questions. "
        "Your task is to examine the description of the available tools based on the input you are given, choose the appropriate tool, extract the necessary parameter(s) from the input, and then call the selected tool accordingly."
        "If you don't know the answer, say you don't know. "
        "If you could not find any tool to call, say 'I could not find any tool to call'"
    ),
    HumanMessagePromptTemplate.from_template("{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])


agent = create_tool_calling_agent(model, tools, prompt)


agent_executor = AgentExecutor(agent=agent, tools=tools, handle_parsing_errors=True, verbose=True)

chat_history = []

user_input = input("You: ")
response = agent_executor.invoke({"input": user_input})

output = response.get("output", "No response found.")
