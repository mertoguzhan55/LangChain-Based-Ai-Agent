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



@tool
def get_kandilli():
    """
    A tool for fetching the latest earthquake data in Turkey.

    This function sends a request to an API that provides real-time earthquake data from Kandilli Observatory and AFAD. 
    It retrieves information about the most recent earthquake in Turkey. If the user asks anything related to earthquakes, 
    this tool will be automatically triggered to provide the latest available earthquake data.

    Usage Scenarios:
    - "Where was the last earthquake in Turkey?"
    - "How many earthquakes happened in Turkey today?"
    - "Did any earthquake just happen?"

    Returned Data Includes:
    - `date`: The time when the earthquake occurred.
    - `latitude`: The latitude coordinate of the earthquake's epicenter.
    - `longitude`: The longitude coordinate of the earthquake's epicenter.
    - `depth`: The depth of the earthquake in kilometers.
    - `magnitude`: The magnitude of the earthquake (Richter scale).
    - `location`: The location where the earthquake took place.
    - `source`: The organization that provided the earthquake data (e.g., Kandilli Observatory, AFAD).

    API URL: https://api.orhanaydogdu.com.tr/deprem/kandilli/live
    """
    url = "https://api.orhanaydogdu.com.tr/deprem/kandilli/live"
    x = requests.get(url)

    data = x.json()
    print(data["result"][0])
    return data["result"][0]


@tool
def get_job():
    """
    A tool for fetching the latest job postings.

    This function sends a request to an API that provides real-time job listings and retrieves the most recently posted job.
    If the user asks anything related to job listings, this tool will be automatically triggered to provide the latest job post.

    Usage Scenarios:
    - "What are the latest job openings?"
    - "Show me the most recent job posting."
    - "Are there any new job opportunities available?"

    Returned Data Includes:
    - `company_name`: The name of the company offering the job.
    - `title`: The job title.
    - `location`: The location where the job is based.
    - `remote`: Indicates whether the job is remote or not.
    - `url`: A direct link to the job posting.
    - `created_at`: The date when the job was posted.

    API URL: https://www.arbeitnow.com/api/job-board-api
    """
    url = "https://www.arbeitnow.com/api/job-board-api"
    x = requests.get(url)

    data = x.json()
    print(data["data"][0])
    return data["data"][0]

    

# @tool
# def weather(city: str):
#     """
#     Retrieves the current weather information for the specified city.

#     Args:
#         city (str): The name of the city for which the weather information is requested.

#     Returns:
#         str: A string describing the current weather conditions in the specified city, including the temperature.
#              Example: "The {city} has 27C and is sunny now."
#     """
#     response = f"the {city} has 27C and sunny now."
#     return response


tools = [get_job, get_kandilli]
model = init_chat_model("llama3-8b-8192", model_provider="groq")


prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(
        "You are a helpful assistant that can use tools to answer questions. "
        "Use the tools provided to gather information and respond accurately. "
        "If you don't know the answer, say you don't know. "
        "If you could not find any tool to call, say 'I could not find any tool to call'"
    ),
    HumanMessagePromptTemplate.from_template("{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])


agent = create_tool_calling_agent(model, tools, prompt)


agent_executor = AgentExecutor(agent=agent, tools=tools, handle_parsing_errors=True, verbose=True)

chat_history = []

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("Chat History:")
        for message in chat_history:
            print(f"{message['role']}: {message['content']}")
        break

    try:
        response = agent_executor.invoke({"input": user_input})
        output = response.get("output", "No response found.")

        chat_history.append({"role": "user", "content": user_input})
        chat_history.append({"role": "assistant", "content": output})

        print(f"Assistant: {output}")
    except Exception as e:
        print(f"HATA: {e}")