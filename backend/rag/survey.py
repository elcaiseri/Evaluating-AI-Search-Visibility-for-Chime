import os
from rag.document import DocumentLoader
from rag.vector import VectorStore
from rag.prompt import PromptTemplateFactory

from utils.logging import get_logger

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from time import time
from glob import glob


# Set your OpenAI API Key
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY


logger = get_logger(__name__)

class SurveyAnalysisRAGSystem:
    def __init__(self, file_path, embedding_model="text-embedding-3-large", llm_model="gpt-4o-mini"):
        logger.info("Initializing SurveyAnalysisRAGSystem")
        self.file_paths = glob(file_path + "*.xlsx")
        self.embedding_model = embedding_model
        self.llm_model = llm_model
        
        # Load documents
        self.documents = DocumentLoader(self.file_paths).load_documents()

        # Create vector embeddings and store them in FAISS
        self.vectorstore = VectorStore(self.documents, self.embedding_model).create_vectorstore()

        # Initialize the language model for generating insights
        self.llm = ChatOpenAI(model=self.llm_model, temperature=0.25, max_tokens=1024)

        # Setup prompt template for query generation
        self.prompt = PromptTemplateFactory.create_prompt_template()

    @staticmethod
    def format_docs(docs):    
        return "\n\n".join(str(doc.metadata["filename"]) + "\n\n" + doc.page_content for doc in docs) 

    def generate_answer(self, query, dataset_id, k=16):
        """Generate an answer for the given query using the specified dataset."""
        logger.info(f"Generating answer for query: {query} with dataset_id: {dataset_id}")
        st = time()
        self.retriever = self.vectorstore.as_retriever(
            search_type="mmr", # mmr
            search_kwargs={'k': k, 'lambda_mult': 0.25, 'filter': {'dataset_id': dataset_id}}
        )
        self.qa_chain = (
            {
                "context": self.retriever | self.format_docs,
                "question": RunnablePassthrough(),
            }
            | self.prompt
            | self.llm
            | StrOutputParser()
        )
        
        logger.info("Invoking QA chain...")
        output = {"result" : self.qa_chain.invoke(query)}
        output["time_taken"] = time() - st
        return output
