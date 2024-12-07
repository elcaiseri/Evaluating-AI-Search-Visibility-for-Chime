import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from utils.logging import get_logger
import json

# Initialize logger
logger = get_logger(__name__)

class DocumentLoader:
    def __init__(self, data_path, file2url_path='data/file2url.json'):
        self.data_path = data_path
        self.file2url = json.load(open(file2url_path))
        logger.info(f"Initialized DocumentLoader with data_path: {data_path} and file2url_path: {file2url_path}")
        
    def load_documents(self):
        """
        Loads and processes documents from the specified data path.
        """
        logger.info(f"Loading documents from {self.data_path}")
        loader = DirectoryLoader(self.data_path, glob="**/*.txt", loader_cls=TextLoader, use_multithreading=True, show_progress=True)
        documents = loader.load_and_split() # RecursiveCharacterTextSplitter
        
        for document in documents:
            self._process(document)

        logger.info(f"Loaded {len(documents)} documents")
        
        return documents
    
    def _process(self, document):
        """
        Updates the document's metadata with a URL based on its source.
        """
        key = "backend/" + document.metadata['source']
        document.metadata['url'] = self.file2url[key]
