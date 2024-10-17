import os
from langchain_community.document_loaders import UnstructuredExcelLoader
from utils.logging import get_logger

# Initialize logger
logger = get_logger(__name__)

class DocumentLoader:
    def __init__(self, file_paths):
        self.file_paths = file_paths

    def load_documents(self):
        """Load and split the documents from the Excel files using the UnstructuredExcelLoader."""
        logger.info(f"Loading documents from {len(self.file_paths)} files: {self.file_paths}")
        docs = [self._process(file_path) for file_path in self.file_paths]
        documents = sum(docs, [])  # Flatten the list of lists
        logger.info(f"Total documents loaded: {len(documents)}")
        return documents

    def _process(self, file_path):
        logger.info(f"Processing file: {file_path}")
        docs = UnstructuredExcelLoader(file_path, mode='elements').load_and_split()
        for doc in docs:
            dataset_id = file_path.split("/")[-1].split("_")[0]
            doc.metadata['dataset_id'] = dataset_id
        logger.info(f"Loaded {len(docs)} documents from {file_path}")
        return docs
