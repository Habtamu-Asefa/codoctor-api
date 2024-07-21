from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

class PDFProcessor:
    def __init__(self, file_path, chunk_size=500, chunk_overlap=100):
        self.file_path = file_path
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.docs = None
        self.all_splits = None

    def load_document(self):
        loader = PyMuPDFLoader(self.file_path)
        self.docs = loader.load()

    def split_document(self):
        if not self.docs:
            raise ValueError("Document not loaded. Call load_document() first.")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            add_start_index=True
        )
        self.all_splits = text_splitter.split_documents(self.docs)

    def get_split_count(self):
        if self.all_splits is None:
            raise ValueError("Document not split. Call split_document() first.")
        return len(self.all_splits)

