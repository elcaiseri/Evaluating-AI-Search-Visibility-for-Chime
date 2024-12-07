import os
from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from utils.logging import get_logger

# Initialize logger
logger = get_logger(__name__)

class PromptTemplateFactory:
    @staticmethod
    def create_prompt_template():
        """Define the updated prompt template for evaluating AI search visibility."""
        logger.info("Defining updated prompt template")
        return ChatPromptTemplate(
            input_variables=['context', 'question'],
            messages=[
                HumanMessagePromptTemplate(
                    prompt=PromptTemplate(
                        input_variables=['context', 'question'],
                        template=(
                            "You are a highly skilled assistant specializing in evaluating the AI search visibility "
                            "and discoverability of digital brands. Your task is to assess the visibility of the digital banking "
                            "brand 'Chime' compared to its competitors: Ally Bank, Varo, Capital One, and SoFi Bank. "
                            "Focus on the following objectives:\n\n"
                            "1. Analyze key factors influencing AI search visibility, such as content depth, relevance, "
                            "AI-friendliness, and authority signals.\n"
                            "2. Compare Chime’s visibility to its competitors using the provided context.\n"
                            "3. Propose a ranking or scoring system to measure AI search visibility.\n"
                            "4. Suggest strategies to enhance Chime’s visibility based on the analysis.\n"
                            "5.	Include URLs for each mentioned source to validate and enhance the answer.\n\n"
                            "Additionally, integrate a Retrieval-Augmented Generation (RAG) system to enrich responses "
                            "with accurate and contextual data from the brand’s official website and other reliable sources. "
                            "Use the retrieved context provided below to formulate an insightful and actionable response.\n\n"
                            "Question: {question}\n"
                            "Context: {context}\n"
                            "Answer:\n\n"
                        )
                    )
                )
            ]
        )