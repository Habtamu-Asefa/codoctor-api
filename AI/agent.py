from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
from AI.rag import Oncology
from langchain.tools.retriever import create_retriever_tool
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv
import os

class Codoctor:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is not set in the environment variables")

        self.model = ChatOpenAI(model="gpt-4o-mini")
        self.search_tool = self.initialize_search_tool()
        self.rag = Oncology()
        self.oncologist_tool = self.create_oncologist_tool()
        self.tools = [self.oncologist_tool]
        self.prompt = self.create_prompt()
        self.agent_executor = self.create_agent_executor()

    def initialize_search_tool(self):
        return TavilySearchResults(
            max_results=2,
            name='medical_web_researcher',
            description="Search for medical resources on web, if it is something you can't find it in other tools only."
        )

    def create_oncologist_tool(self):
        return create_retriever_tool(
            self.rag,
            "oncologist",
            "This is a world-class oncologist who advises doctors on how to best treat patients. This tool has the highest priority.",
        )

    def create_prompt(self):
        return ChatPromptTemplate.from_messages(
            [
                ("system", "You are a world class oncologist who advises doctors on how to best treat patients. You are concise and rich. Don't answer questions if you don't know the answer. You have medical knowledge only and especially about oncology. You only answer to medical professionals"),
                MessagesPlaceholder("chat_history", optional=True),
                ("human", "{input}"),
                MessagesPlaceholder("agent_scratchpad"),
            ]
        )

    def create_agent_executor(self):
        agent = create_openai_tools_agent(self.model, self.tools, self.prompt)
        return AgentExecutor(agent=agent, tools=self.tools)

    def query_agent(self, query):
        return self.agent_executor.invoke({"input": query})

    def run_interactive_session(self):
        # Define ANSI color codes
        RESET = "\033[0m"
        GREEN = "\033[32m"
        RED = "\033[31m"
        
        # Print a message
        print(f"{RED}Start of conversation with CoDoctor.\n\n{RESET}")
        
        while True:
            try:
                query = input("Query: ")
                response = self.query_agent(query)
                print(f"{GREEN}{response['output']}{RESET}\n", end="", flush=True)
            except Exception as e:
                print(f"An error occurred: {e}")

if __name__ == "__main__":
    codoctor = Codoctor()
    codoctor.run_interactive_session()
