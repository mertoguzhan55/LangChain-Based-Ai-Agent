from langchain.chat_models import init_chat_model
from langchain.agents import AgentExecutor, create_react_agent
from langchain.agents import create_tool_calling_agent
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_core.prompts.chat import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate, MessagesPlaceholder
from selenium.webdriver.support import expected_conditions as EC
from dataclasses import dataclass
from app.tools import Tools

@dataclass
class Agent:

    language_model_name: str
    model_provider: str
    logger: any

    def __post_init__(self):
        self.tools_instance = Tools()
        self.tools = [self.tools_instance.get_youtube_link_according_to_the_song]
        self.model = init_chat_model(self.language_model_name, model_provider = self.model_provider)
        self.logger.info("post init worked successsfully!")

    def run_agent(self):
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

        try:
            agent = create_tool_calling_agent(self.model, self.tools, prompt)
            agent_executor = AgentExecutor(agent=agent, tools = self.tools, handle_parsing_errors=True, verbose=True)

            user_input = input("You: ")
            response = agent_executor.invoke({"input": user_input})

            output = response.get("output", "No response found.")
            return output
        except Exception as e:
            self.logger.info(f"Exception executing the agent: {e}")
        

if __name__ == "__main__":
    pass











