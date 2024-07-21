from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from load_and_split import PDFProcessor

import os
from dotenv import load_dotenv

class Embedder:
    def __init__(self, pdf_path, persist_directory, chunk_size=4000, chunk_overlap=100):
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.pdf_path = pdf_path
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.persist_directory = persist_directory

        self.processor = PDFProcessor(file_path=self.pdf_path, chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
        self.processor.load_document()
        self.processor.split_document()
        self.all_splits = self.processor.all_splits

        # Create and persist embeddings
        self.vectorstore = Chroma.from_documents(documents=self.all_splits, embedding=OpenAIEmbeddings(api_key=self.api_key), persist_directory=self.persist_directory)

    def get_vectorstore(self):
        return self.vectorstore

# Adding test embeddings
if __name__ == "__main__":
    test = Embedder("AI\data\Sinners in the Hands of an Angry God.pdf", "test_embeddings")
    print(test.get_vectorstore())
    print('Done adding test embeddings.')