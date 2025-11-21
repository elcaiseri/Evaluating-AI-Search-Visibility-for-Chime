import os
from time import time

from datasets import Dataset
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from rag.document import DocumentLoader
from rag.prompt import PromptTemplateFactory
from rag.vector import VectorStore
from ragas import evaluate
from utils.logging import get_logger

# Set your OpenAI API Key
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

logger = get_logger(__name__)


class RAGSystem:
    def __init__(
        self,
        file_path,
        json_path,
        embedding_model="text-embedding-3-large",
        llm_model="gpt-4o-mini",
        **kwargs,
    ):
        logger.info("Initializing RAGSystem")
        self.embedding_model = embedding_model
        self.llm_model = llm_model

        # Load documents
        self.documents = DocumentLoader(file_path, json_path).load_documents()

        # Create vector embeddings and store them in FAISS
        self.vectorstore = VectorStore(
            self.documents, self.embedding_model
        ).create_vectorstore()

        self.retriever = self.vectorstore.as_retriever(
            search_type="mmr", search_kwargs={"k": kwargs.get("k", 5)}
        )

        # Initialize the language model for generating insights
        self.llm = ChatOpenAI(
            model=self.llm_model,
            temperature=kwargs.get("temperature", 0.1),
            max_tokens=kwargs.get("max_tokens", 512),
        )

        # Setup prompt template for query generation
        self.prompt = PromptTemplateFactory.create_prompt_template()

        self.qa_chain = (
            {
                "context": self.retriever | self.format_docs,
                "question": RunnablePassthrough(),
            }
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

    @staticmethod
    def format_docs(docs):
        return "\n\n".join(
            "Brand Page URL: ( "
            + str(doc.metadata["url"])
            + " )"
            + "\n"
            + doc.page_content
            for doc in docs
        )

    def search(self, query):
        """Generate an answer for the given query."""
        logger.info(f"Generating answer for query: {query}")
        st = time()
        logger.info("Invoking QA chain...")
        output = {"result": self.qa_chain.invoke(query)}
        output["time_taken"] = str(time() - st)
        return output

    def evaluate_w_ragas(self, query, contexts, answer, ground_truth):
        examples = [
            {
                "question": query,
                "contexts": [contexts],
                "answer": answer,
                "ground_truth": ground_truth,
            }
        ]

        dataset = Dataset.from_list(examples)
        metrics = evaluate(dataset)

        return metrics
