# CODOCTOR AI

import os
from dotenv import load_dotenv

# Set your OpenAI API key as an environment variable
os.environ["OPENAI_API_KEY"] = "sk-proj-r8Wz0Ujr3YEIY2t300q5T3BlbkFJSZMXtGZNbMwBGkH7BZnk"
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, trim_messages
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from operator import itemgetter

# Load environment variables from the .env file
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("No OPENAI_API_KEY found in environment variables")


class CoDoctor:
    def __init__(self, model_name="gpt-4o-mini"):
        self.model = ChatOpenAI(model=model_name, api_key=api_key)
        self.trimmer = trim_messages(
            max_tokens=65,
            strategy="last",
            token_counter=self.model,
            include_system=True,
            allow_partial=False,
            start_on="human",
        )
        self.store = {}
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful oncology assistant. Answer all questions to the best of your ability. If you don't know the answer, say that you don't know. You have medical knowledge only and especially about oncology.",
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )
        chain = (
            RunnablePassthrough.assign(messages=itemgetter("messages") | self.trimmer)
            | self.prompt
            | self.model
        )
        self.with_message_history = RunnableWithMessageHistory(chain, self.get_session_history, input_messages_key="messages")

    def get_session_history(self, session_id: str):
        if session_id not in self.store:
            self.store[session_id] = InMemoryChatMessageHistory()
        return self.store[session_id]

    def invoke(self, content: str, session_id: str) -> str:
        config = {"configurable": {"session_id": session_id}}
        response_content = ""
        for r in self.with_message_history.stream(
            {
                "messages": [HumanMessage(content=content)],
            },
            config=config,
        ):
            response_content += r.content
        return response_content

    def stream(self, content: str, session_id: str):
        config = {"configurable": {"session_id": session_id}}
        for r in self.with_message_history.stream(
            {
                "messages": [HumanMessage(content=content)],
            },
            config=config,
        ):
            yield r.content
