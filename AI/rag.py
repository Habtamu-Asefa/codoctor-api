from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain import hub
from langchain_core.messages import HumanMessage

import os
from dotenv import load_dotenv

class Oncology:
    def __init__(self, config={}):
        self.config=config
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is not set in the environment variables")
        
        self.persist_directory = "..\AI\oncology"
        
        try:
            # Load persisted embeddings
            self.vectorstore = Chroma(persist_directory=self.persist_directory, embedding_function=OpenAIEmbeddings(api_key=self.api_key))
        except Exception as e:
            raise ValueError(f"Error loading vectorstore: {e}")

        # Initialize retriever
        try:
            self.retriever = self.vectorstore.as_retriever()
        except Exception as e:
            raise ValueError(f"Error initializing retriever: {e}")

        # Initialize the language model
        try:
            self.llm = ChatOpenAI(model="gpt-4o-mini")
        except Exception as e:
            raise ValueError(f"Error initializing language model: {e}")

        # Load the RAG prompt from hub
        try:
            self.prompt = hub.pull("rlm/rag-prompt")
        except Exception as e:
            raise ValueError(f"Error loading prompt from hub: {e}")

    @staticmethod
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    # For testing purposes, create the RAG chain
    def create_rag_chain(self):
        try:
            return (
                {"context": self.retriever | self.format_docs, "question": RunnablePassthrough()}
                | self.prompt
                | self.llm
                | StrOutputParser()
            )
        except Exception as e:
            raise ValueError(f"Error creating RAG chain: {e}")

    def stream(self, query):
        try:
            return self.retriever.stream(query)
        except Exception as e:
            raise ValueError(f"Error streaming query: {e}")

    def invoke(self, query, config=None):
        try:
            return self.retriever.invoke(query)
        except Exception as e:
            raise ValueError(f"Error invoking query: {e}")
        

if __name__ == "__main__":
    # Testing rag
    onco = Oncology()
    RESET = "\033[0m"
    GREEN = "\033[32m"
    RED = "\033[31m"
        
        # Print a message
    print(f"{RED}Start of conversation with CoDoctor.\n{RESET}")
    while True:
        try:
            query = input("\n Query: ")
            for chunk in onco.create_rag_chain().stream(query):
                print(f"{GREEN}{chunk}{RESET}", end="", flush=True)
        except Exception as e:
            print(f"An error occurred: {e}")
