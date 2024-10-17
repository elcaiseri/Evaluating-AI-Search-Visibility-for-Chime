import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from utils.logging import get_logger

# Initialize logger
logger = get_logger(__name__)

# Set your OpenAI API Key
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

class VectorStore:
    def __init__(self, documents, embedding_model):
        self.documents = documents
        self.embedding_model = embedding_model

    def create_vectorstore(self):
        """Generate embeddings for the documents and create a FAISS vectorstore for retrieval."""
        logger.info("Generating embeddings for documents")
        embeddings = OpenAIEmbeddings(model=self.embedding_model)
        vectorstore = FAISS.from_documents(self.documents, embeddings)
        logger.info(f"Vectorstore created successfully with {len(self.documents)} documents")
        return vectorstore
