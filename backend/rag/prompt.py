import os
from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from utils.logging import get_logger

# Initialize logger
logger = get_logger(__name__)

class PromptTemplateFactory:
    @staticmethod
    def create_prompt_template():
        """Define the prompt template for querying the model with relevant context."""
        logger.info("Defining prompt template")
        return ChatPromptTemplate(
            input_variables=['context', 'question'],
            messages=[
                HumanMessagePromptTemplate(
                    prompt=PromptTemplate(
                        input_variables=['context', 'question'],
                        template=(
                            "You are an assistant for question-answering tasks. "
                            "Specialized in data analysis and interpreting survey data. "
                            "Use the following pieces of retrieved context to answer the question. "
                            "If you don't know the answer, just say that you don't know. "
                            "Use three sentences maximum and keep the answer concise.\n"
                            "Question: {question} \n"
                            "Context: {context} \n"
                            "Answer:"
                        )
                    )
                )
            ]
        )
